# External source policy

Enforced by `backend/knowledge/ingestion/license_checker.py` for **every** ingested item. These are summaries of each provider's published terms as reviewed on 2026-10-22. They are not legal advice. Re-check the linked terms before a commercial launch.

## How enforcement works

- Each adapter tags its items with a `policy_key`. If an item has no key, its domain is matched against the registry. Either way, the item's declared license must be one that the policy accepts. A domain alone never grants permission.
- Ingestion **fails closed** in these cases:
  - the source is unknown;
  - no license is declared;
  - the license is not on the policy's list;
  - AI use or automated retrieval is not permitted;
  - attribution is disabled for a CC BY-style license;
  - the policy has status `requires_review` and has not been cleared.
- Permissions are tracked separately for each dimension: retrieval, AI processing, commercial use, redistribution, and attribution. The decision is stored on the `SourceDocument` in `metadata.policy`. The feed API returns it as `attribution` on each card, and the card UI shows it.
- Per-item overrides (the old `manual_license_override` metadata flag) are **no longer honoured**. Clearing a source is a deployment decision:
  - `INGESTION_REVIEWED_SOURCES` clears a `requires_review` policy;
  - `REDDIT_LEGAL_REVIEW_APPROVED` clears Reddit.
- `INGESTION_REQUIRE_COMMERCIAL_USE=True` also rejects any item whose license does not permit commercial use.

## Policy registry

| Policy key | Content license | AI use | Commercial | Redistribution / attribution | Self-attestation | Status |
|---|---|---|---|---|---|---|
| `wikimedia` | CC BY-SA 4.0 ([ToU](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use)) | yes | yes | share-alike, credit "Wikipedia contributors" + link | yes | approved |
| `arxiv` | Abstracts/metadata CC0 ([API ToU](https://info.arxiv.org/help/api/tou.html)). Full text is **never fetched**. | yes | yes | public domain; do not imply arXiv endorsement | **no** (preprints) | approved |
| `github` | Per-repo SPDX license. Only permissive ones are accepted: MIT, Apache-2.0, BSD-2/3, ISC, 0BSD, Unlicense, CC0, CC-BY-4.0, CC-BY-SA-4.0 | yes | per license | per license | **no** (READMEs describe projects) | approved |
| `stackexchange` | CC BY-SA 2.5, 3.0 or 4.0, depending on when the post was written ([licensing](https://stackoverflow.com/help/licensing)) | yes | yes | share-alike; show Stack Exchange, author, and link | no (authority < 0.70) | approved |
| `official_docs:python` | PSF License v2 ([license](https://docs.python.org/3/license.html)) | yes | yes | attribution | yes | approved |
| `official_docs:javascript` | MDN prose CC BY-SA 2.5 ([MDN](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Attrib_copyright_license)) | yes | yes | share-alike, credit "Mozilla Contributors" | yes | approved |
| `official_docs:typescript` | CC BY 4.0 ([TypeScript-Website](https://github.com/microsoft/TypeScript-Website)) | yes | yes | attribution | yes | approved |
| `official_docs:java` | Oracle, "all rights reserved" ([notice](https://docs.oracle.com/en/java/javase/21/docs/legal/copyright.html)) | — | no | link only | — | **requires_review** (blocked) |
| `official_docs:cpp` | isocpp.org has no public reuse license ([terms](https://isocpp.org/home/terms-of-use)) | — | no | link only | — | **requires_review** (blocked) |
| `reddit` | Reddit Data API terms ([terms](https://redditinc.com/policies/data-api-terms)) | **no** (AI-model training prohibited) | **no** (separate agreement required) | link only | — | blocked until `REDDIT_LEGAL_REVIEW_APPROVED=True` |

**Self-attestation:** for curated reference sources, a claim extracted from a document counts as *supported by that document*. This only applies if the claim passes a grounding check: at least `INGESTION_GROUNDING_MIN_COVERAGE` (default 0.75) of its content words must appear in one passage of the source. Claims that fail the check go through normal verification (evidence retrieval → Gemini fact-check). arXiv, GitHub and Stack Exchange never self-attest.

## Reddit

Reddit stays on the **evidence-only** path:

- Items have `evidence_only=True` and `ai_use_allowed=False`.
- They never become canonical claims or flashcards.
- They are never sent to an LLM or the embedding API.
- Access uses OAuth (`REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`). Unauthenticated `.json` scraping was removed because it falls outside the Data API terms.
- Reddit is excluded from scheduled discovery unless the legal flag is set.

## Open items for legal sign-off

- Stack Exchange: the API terms contain no AI clause. Stack Overflow's public statements on LLM training are not reflected in the API terms. Confirm this before a commercial launch.
- Wikimedia: high-volume commercial reuse may be steered to Wikimedia Enterprise.
- Java / C++: enable only after written permission or a documented fair-use review. Then add the keys to `INGESTION_REVIEWED_SOURCES`.
