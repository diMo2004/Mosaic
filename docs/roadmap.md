# MOSAIC Roadmap

This roadmap separates current work from future work so the team stays focused.

## Current Work

Backend categories 0–7 are largely done. Immediate focus:

```text
Close remaining pipeline gaps (verify after extraction, profile-complete gate, Source model cleanup).
Start Category 8: Expo mobile MVP against the existing APIs.
Keep CI green on main.
```

Do not start recommendations, social, Celery, or microservices until the mobile vertical slice works.

## Audience And Product Split

```text
First users: CSE students.
Public feed: flashcards from shared canonical knowledge (implemented).
Personal environment: cards from the user's own verified notes (not implemented).
Note library list/detail: gated on can_view_own_notes until a later reward system.
Save: playlists, not a flat saved-flag table.
```

## App Status

### Users — mostly done

Done: register, login, JWT refresh, UserProfile signal, Google auth, complete-profile endpoint.

Next:

```text
Enforce IsProfileComplete on app APIs
Google + profile screens on mobile
```

### Notes — pipeline wired, still synchronous

Done: upload, owner, gated list/detail, job after upload, in-process OCR + claim extraction.

Next:

```text
Call verification from NoteProcessingService
Celery later
Stronger file validation
```

### Knowledge — models and admin in place

Done: source/evidence/claim/concept/canonical APIs and admin; CSE taxonomy + NetworkX assignment.

Next:

```text
Deduplicate Source fields
Edges when approving UnmappedConceptReview
knowledge tests
```

### Verification — service done, orchestrator incomplete

Done: scoring verifier, placeholder evidence, verify endpoint, concept assignment.

Next:

```text
After claims_extracted, verify each claim and set job VERIFIED
Human review queue UX (admin exists; no dedicated API)
```

### Learning — category 7 done

Done: generate from canonical, provenance on API, feed/detail/feedback/progress, playlists.

Next:

```text
Personal vs public flashcard environments
Understood action
Real LLM explanation
Mobile feed + playlist UI
```

## Sprint Status

### Sprints 1–4 (backend foundation through verification/flashcards)

Treat as **done enough to build mobile**, except:

```text
Note job does not auto-verify
Profile completion is not enforced on APIs
Source model still has duplicated field declarations
```

### Sprint 5: Mobile MVP Shell — next

```text
Expo scaffold
Auth screens (email + Google)
Mandatory profile form
Flashcard feed + detail
Playlist save/unsave + feedback
Upload note + processing status
```

Definition of done:

```text
Mobile can login, complete profile, fetch public flashcards, save to playlist,
submit feedback, upload a note, and see processing status.
```

### Sprint 6: Personal environment + pipeline closeout

```text
Flashcard.environment = public | personal
Personal feed from the user's verified notes
Note processing runs verification and can reach VERIFIED
IsProfileComplete on APIs
```

## Future Work (unchanged intent, updated order)

Do these only after Sprint 5–6.

### Real RAG

```text
Embeddings + pgvector
Retrieve canonical claims + evidence
LLM explanation with citations
```

### Production jobs and storage

```text
Celery + Redis
S3/R2 for media
Retry / dead-letter / worker monitoring
```

Production **hosting** (Render + GitHub Actions) is already in place; this section is workers and object storage, not “first deploy.”

### External ingestion

```text
Source adapters (GitHub, official docs, Stack Exchange, arXiv)
License/policy registry enforcement
Reddit only as community evidence after legal review
```

### Recommendations, mastery, contributors

```text
Topic / prerequisite / history recommendations
Understood + concept mastery
Contributor scores; can_view_own_notes from rewards
```

### Social and scale

```text
Friends, chat, comments, sharing — later only
OpenSearch, graph DB, microservices — only if Postgres + NetworkX is not enough
```
