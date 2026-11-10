# Continuous external ingestion and the flashcard feed

## Pipeline

```
Celery Beat (INGESTION_SCHEDULE_ENABLED=True)
  knowledge.schedule_external_discovery          every INGESTION_DISCOVERY_INTERVAL_MINUTES
    └─ knowledge.discover_adapter(adapter)       one per adapter enabled by config + source policy
         TopicPlanner: CSE taxonomy concepts with the fewest active cards (official_docs: per language)
         SourceDiscoveryCheckpoint: leased, holds the provider cursor (sroffset / start / page / index offset)
         adapter.discover() → IngestionJob per record (unique adapter + external_id)
    └─ knowledge.process_ingestion_job(job)      enqueued on commit
         claim job (conditional UPDATE + lease) → adapter.fetch()
         ExternalIngestionPipeline.ingest_item(defer_flashcards=True)
           LicenseChecker.evaluate (every item, fail closed)
           content checks (INGESTION_MIN_DOCUMENT_CHARS), normalized content hash
           SourceDocument: new | unchanged (skip) | changed (new current version) | interrupted (resume)
           ClaimExtractionService (LLM, outside transactions)
           grounded self-attestation evidence (policy-dependent)
           ClaimVerificationService.verify_claim(defer_flashcard=True)
             evidence → status → Gemini fact-check → concept assignment (LLM, outside transactions)
             atomic: claim status + CanonicalClaim (deduplicated by normalized text hash)
             on commit → learning.generate_flashcard_for_claim(canonical_claim)
  knowledge.recover_ingestion_jobs               every 10 min: expired leases, lost dispatches, due retries
  learning.backfill_missing_flashcards            every 15 min: supported claims still without a card
```

The feed (`GET /api/learning/flashcards/`) serves eligible cards straight from the database. A card is eligible when the card is active and has an active canonical claim. New cards show up on the next page request.

### Adapters (`knowledge/ingestion/adapters/`, registry in `registry.py`)

| Adapter | Discovery mechanism | Stable ID | Checkpoint cursor |
|---|---|---|---|
| `wikimedia` | `w/api.php?action=query&list=search` | `enwiki:<pageid>` | `sroffset` |
| `arxiv` | `export.arxiv.org/api/query`: abstract/title match within CS categories, newest first | `arxiv:<id without version>` | `start` |
| `github` | `search/repositories` (stars ≥ `INGESTION_GITHUB_MIN_STARS`; repos without a permissive license are skipped) | `github:<repo id>` | `page` |
| `stackexchange` | `/2.3/search/advanced` (accepted answers, sorted by votes) | question `se:<site>:q:<id>`; answers `se:<site>:a:<id>` | `page` |
| `official_docs` | Python `objects.inv` (std:doc entries), MDN `sitemap.xml`, TypeScript `sitemap-index.xml`; Java and C++ are blocked by policy | `docs:<lang>:<path>` | cached URL index + `offset` (refreshed weekly) |
| `reddit` | OAuth `r/<sub>/search` (evidence only; disabled by default) | `reddit:<id>` | `sub_index` + `after` |

All HTTP calls go through `knowledge/ingestion/http.py`, which handles:

- **User-Agent:** a descriptive one from `INGESTION_USER_AGENT`.
- **Request spacing:** a per-domain minimum interval (arXiv 3 s, GitHub 2.5 s with a token / 6.5 s without, Stack Exchange 0.5 s).
- **Cool-downs:** HTTP 429/503 `Retry-After`, Stack Exchange `backoff`, and `throttle_violation` all put the domain into a cool-down.
- **Error classes:** transient (retry) or permanent (record).
- **robots.txt:** checked for documentation page fetches.

Official-doc fetches must stay on the allow-listed domain and path prefix.

### Idempotency and incremental updates

- `IngestionJob(adapter, external_id)` is unique, so re-discovering a record creates no new work. A completed job is re-queued after `INGESTION_REVISIT_DAYS` to check for changes.
- `SourceDocument` gets `content_hash` (SHA-256 of whitespace-normalized text), `external_id`, `is_current` and `superseded_by`. At most one current document is allowed per `(source, url)` (DB constraint).
  - Unchanged content is skipped without calling the LLM.
  - Changed content becomes a new current version. The old version and its claims and cards are **retained** for provenance; nothing is deleted.
  - A document interrupted mid-pipeline (`metadata.ingestion_state` is not complete) is resumed rather than re-extracted.
- `CanonicalClaim.text_hash` deduplicates identical facts across sources. The second source is recorded as corroborating `SUPPORTS` evidence on the original claim.
- `Flashcard`: at most one active card per canonical claim (partial unique constraint). `FlashcardGenerationService` checks for an existing card *before* calling the LLM, and handles insert races.
- `Flashcard.generation_method` is `gemini`, `fallback` or `unknown` (legacy). `created_by_ai` is true only for real Gemini output.

## Running it

Every deployment needs:

1. **Migrations:** `python manage.py migrate` (knowledge 0008–0010, learning 0009–0011). Migration `learning.0010` *deactivates* (does not delete) duplicate active cards that share a canonical claim.
2. **Taxonomy:** `python manage.py seed_cse_concepts`. Topic planning and concept assignment both use it.
3. **A worker consuming the ingestion queue:**
   `celery -A config worker -Q ocr,embeddings,celery,ingestion --concurrency=2 --loglevel=INFO`
4. **Exactly one Beat process:** `celery -A config beat --loglevel=INFO`. On Render, either run a separate background worker with this command, or add `-B` to the single worker command, but only if that worker has exactly one instance.
5. **Environment:**
   - `INGESTION_SCHEDULE_ENABLED=True`
   - `INGESTION_USER_AGENT` with a real contact address
   - `CACHE_URL=redis://…/2`, so rate limits are shared across worker processes
   - optionally `GITHUB_TOKEN` and `STACKEXCHANGE_API_KEY`

The scheduled ingestion is not running anywhere until steps 3–5 are done in the target environment.

### Manual, bounded runs

```powershell
python manage.py run_ingestion --adapter wikimedia --topic "binary search tree" --limit 3 --sync   # no worker needed
python manage.py run_ingestion --limit 5                                                         # enqueue for workers
python manage.py ingestion_status            # jobs, failures, checkpoints, inventory, feed repetition
python manage.py ingestion_status --json
python manage.py ingest_external wikimedia "Binary search tree"                                  # single record (unchanged CLI)
```

Staff-only API:

- `GET /api/knowledge/ingestion/status/`
- `POST /api/knowledge/ingestion/run/` with body `{"adapter": "wikimedia", "topic": "heap", "limit": 3}`. The limit is capped at 10.

Django admin has two new models:

- **Ingestion jobs:** filter by status; the "Retry selected jobs now" action re-queues them.
- **Discovery checkpoints:** the "Reset cursor" action restarts a query.

### Configuration

| Variable | Default | Purpose |
|---|---|---|
| `INGESTION_SCHEDULE_ENABLED` | `False` | Registers the Beat schedule |
| `INGESTION_TASK_QUEUE` | `ingestion` | Queue for ingestion and card-generation tasks |
| `INGESTION_DISCOVERY_INTERVAL_MINUTES` | `60` | Discovery cadence |
| `INGESTION_ENABLED_ADAPTERS` | `wikimedia,official_docs,stackexchange,arxiv,github` | Adapters to schedule. Source policy can still disable one. |
| `INGESTION_TOPICS_PER_RUN` | `3` | Taxonomy topics per adapter per run |
| `INGESTION_MAX_CANDIDATES_PER_RUN`, `INGESTION_<ADAPTER>_MAX_PER_RUN` | `5` | New jobs per adapter per run |
| `INGESTION_MAX_ATTEMPTS` | `4` | Attempts before a job is `failed` |
| `INGESTION_REVISIT_DAYS` | `7` | Change-detection revisit window and exhausted-query restart |
| `INGESTION_REQUEUE_PENDING_MINUTES` | `30` | Age at which a pending job counts as a lost dispatch |
| `INGESTION_MIN_DOCUMENT_CHARS` | `30` | Below this length a document is rejected as insufficient content |
| `INGESTION_GROUNDING_MIN_COVERAGE` | `0.75` | Grounding threshold for self-attestation |
| `INGESTION_LOW_INVENTORY_THRESHOLD` | `200` | `ingestion_status` warns below this many eligible cards |
| `INGESTION_GITHUB_MIN_STARS`, `INGESTION_STACKEXCHANGE_MIN_ANSWER_SCORE` | `500`, `5` | Quality floors |
| `INGESTION_USER_AGENT` | placeholder | **Set it.** Wikimedia requires contact details. |
| `CACHE_URL` | empty (per-process memory) | Shared Redis cache for rate limits and the taxonomy graph |
| `INGESTION_REVIEWED_SOURCES`, `INGESTION_REQUIRE_COMMERCIAL_USE`, `REDDIT_LEGAL_REVIEW_APPROVED`, `REDDIT_CLIENT_ID/SECRET` | off | Policy switches; see [source_policy.md](source_policy.md) |
| `FLASHCARD_GENERATION_MAX_ATTEMPTS`, `FLASHCARD_BACKFILL_BATCH_SIZE`, `FLASHCARD_BACKFILL_GRACE_MINUTES` | `4`, `50`, `5` | Bounds for async card generation |
| `LOG_LEVEL` | `INFO` | Level for the `knowledge`, `learning` and `verification` loggers |

## Feed API contract

`GET /api/learning/flashcards/?session_id=<uuid>&limit=<1..50>`. `cursor` is accepted as an alias for `session_id`.

```json
{
  "results": [FlashcardDTO...],          // now includes "attribution": {source, title, url, license, license_url, attribution, retrieved_at} | null
  "session_id": "uuid", "cursor": "uuid",
  "has_more": true, "session_exhausted": false,
  "repeated_count": 0,                    // cards from a recent session, served because inventory is short
  "retry_after_seconds": null             // set when exhausted: when to ask again for newly generated cards
}
```

- **Session cursor.** Every card served or viewed in a session is excluded from later pages of that session. Pages never repeat, and inserts never shift the pagination. A new card persisted after the session started is returned on the session's next request.
- **Ranking** happens in the database:
  - tier 0: never seen, and not served in the last 24 h; newest first;
  - tier 1: last seen more than 7 days ago; least recent first;
  - tier 2: seen recently; returned only when inventory is short.
  - Within a page, cards are interleaved across concepts.
- **Eligibility:** the card is active, has a canonical claim, and that claim is active.
- Responses carry `Cache-Control: no-store`. The server has no feed cache, so there is nothing to invalidate.

Mobile (`useFlashcardFeed`, `FeedScreen`):

- Prefetches when the user is three cards from the end.
- When the session is exhausted, it re-checks the same session every `retry_after_seconds`. The re-check runs only while the Feed is focused and the app is in the foreground.
- Returning to the Feed, or bringing the app back to the foreground, fetches new cards without resetting the scroll position. Pull-to-refresh starts a new session.
- If a page request fails, the cards already loaded stay on screen and a hint appears.

## Observability

Log lines use stable prefixes:

- `ingestion.discovery.completed` / `.failed`
- `ingestion.job.finished` (status, error, counts)
- `ingestion.job.retry`
- `ingestion.http.cooldown`
- `ingestion.recovery`
- `ingestion.attestation.ungrounded`
- `verification.canonical.deduplicated`
- `flashcard.generation.persisted` / `.failed` / `.exhausted`
- `flashcard.dispatch.failed`
- `feed.page.empty`

No secrets or user identifiers are logged.

`ingestion_status` reports:

- jobs per adapter and status, and the last 24 h of document, claim and canonical counts;
- failing checkpoints and recent failures with their reasons;
- eligible inventory, with a low-inventory warning;
- cards per generation method;
- claims missing cards, and how many have exhausted their retries;
- the median and maximum time from discovery to card;
- the 24 h cross-session repeat rate in the feed.

## Troubleshooting

| Symptom | Check |
|---|---|
| No new jobs | `INGESTION_SCHEDULE_ENABLED`; is a Beat process running? `ingestion_status` → "Adapters enabled" is empty if config or policy disables everything. Checkpoints with `next_run_at` in the future are backing off. |
| Jobs stuck `pending` | No worker consumes `INGESTION_TASK_QUEUE`. Add `-Q …,ingestion` to the worker. |
| Many `policy_rejected` | The job's `last_error` names the rule. Fix the adapter metadata; do not bypass the checker. |
| Many `skipped` | Documents are empty or too short (e.g. a README missing, disambiguation pages). |
| Jobs `succeeded` but no cards | `last_24h.claims_supported` is 0: claims are not being verified (no evidence or Gemini). Or `canonical_claims_missing_cards` is greater than 0: card tasks are not running. |
| `generation_method=fallback` dominates | Gemini key, quota, or model errors. See the `Flashcard generation LLM error` logs. |
| GitHub/arXiv 429s | Set `GITHUB_TOKEN`; set `CACHE_URL` so all processes share one rate limit. |
| Feed repeats cards | `repeated_count > 0` means eligible inventory is below what the user has consumed. Watch `inventory.low_inventory`. |
