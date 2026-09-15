Team Build Order (historical)

Phases 0–6 below were the original team split. Backend Phases 0–5 are largely done. Frontend/mobile in those phases is still TODO. Prefer the Precise Implementation Order (status-tagged) for what to do next.

Phase 0: Repo And Team Setup
Everyone does this first:
1. Create GitHub repo
2. Add all team members as collaborators
3. Set up SSH keys
4. Create project board/issues
5. Agree branch naming
6. Agree commit/PR rules
7. Add README and docs folder
Suggested branches:
main
develop
feature/backend-auth
feature/backend-notes
feature/mobile-shell
feature/ocr-pipeline
Rules:
main = stable only
develop = integration branch
feature branches = individual work
PR required before merge
At least 1 review before merging
Phase 1: Scaffold In Parallel
Frontend Developer:
* Scaffold Expo app in /mobile
* Create basic navigation
* Create placeholder screens:
  - Login
  - Register
  - Upload Note
  - Processing Status
  - Flashcard Feed
  - In-depth Explanation

Backend Developer 1:
* Scaffold Django + DRF in /backend
* Configure settings
* Add users app
* Add JWT auth
* Add environment variables

Backend Developer 2:
* Design initial database models:
  - SourceDocument
  - ExtractedClaim
  - Evidence
  - Concept
  - CanonicalClaim
  - Flashcard
* Create knowledge/verification apps

Flexible Beginner:
* Write setup docs
* Create `.env.example`
* Test setup steps on their machine
* Create sample user stories/issues
Phase 2: First Working Vertical Slice
Goal: user can register/login, upload a note, and see it listed.
Frontend Developer:
* Connect login/register screens to backend
* Build upload note screen
* Build notes list screen

Backend Developer 1:
* Build auth endpoints
* Build note upload endpoint
* Build note list/detail endpoints
* Add per-user access control

Backend Developer 2:
* Add NoteProcessingJob model
* Add status states:
  - UPLOADED
  - PROCESSING
  - OCR_DONE
  - CLAIMS_EXTRACTED
  - VERIFIED
  - FAILED
* Add placeholder processing task

Flexible Beginner:
* Test APIs manually
* Write basic API docs
* Create sample note files
* Report bugs through GitHub issues
Phase 3: Processing Pipeline MVP
Goal: uploaded note becomes text, then claims.
Frontend Developer:
* Add processing status UI
* Add claim review screen
* Show extracted claims

Backend Developer 1:
* Improve file validation
* Add media/object storage abstraction
* Add permissions and error handling

Backend Developer 2:
* Add OCR provider integration
* Add claim extraction service
* Store extracted text and claims
* Add retry/failure handling

Flexible Beginner:
* Collect sample handwritten/typed notes
* Run test uploads
* Compare OCR output manually
* Document known OCR/claim extraction issues
Phase 4: Verification And Canonical Knowledge
Goal: claims get verification status and verified knowledge is stored separately.
Frontend Developer:
* Build claim status UI
* Show:
  - Supported
  - Contradicted
  - Partially supported
  - Uncertain
* Build corrected-claim display

Backend Developer 1:
* Add source registry APIs
* Add evidence APIs
* Add admin tools for reviewing claims

Backend Developer 2:
* Build verification service
* Add evidence retrieval placeholder first
* Store confidence, status, provenance
* Create canonical knowledge records only after verification

Flexible Beginner:
* Add source metadata manually for test sources
* QA claim statuses
* Check that raw notes and canonical knowledge stay separate
Phase 5: Flashcards And Learning UI
Goal: verified knowledge turns into usable learning cards.
Frontend Developer:
* Build flashcard feed
* Build swipe sequence UI
* Build in-depth explanation screen

Backend Developer 1:
* Build flashcard API
* Build save/feedback endpoints
* Add user progress basics

Backend Developer 2:
* Generate flashcards from canonical claims
* Add grounded explanation endpoint
* Retrieve supporting evidence for explanations

Flexible Beginner:
* Create sample flashcard test cases
* Review card quality manually
* Test mobile flows
Phase 6: Polish, Testing, Demo
Frontend Developer:
* Improve UI polish
* Loading/error/empty states
* Mobile responsiveness

Backend Developer 1:
* Add tests for auth, notes, permissions
* Harden API validation

Backend Developer 2:
* Add tests for claim/verification pipeline
* Improve prompt templates and confidence logic

Flexible Beginner:
* Prepare demo script
* Update README
* Record bugs
* Test full flow from fresh install
Best First Sprint
Backend first milestone is done: register → login → upload a note → store it.
Second milestone (OCR → claims) is done on the backend.
Third milestone (verify → canonical → flashcards) is done for the API; mobile UI is not.

Next team milestone: Expo app talks to those APIs (playlists, public feed, upload status).
_______________________________________________________________

Status key:

```text
DONE      implemented and in use
PARTIAL   code exists but a gap remains
TODO      not built
NEXT      do this next
```

Product decisions not in the original task list (now first-class):

```text
First users: CSE students
Public flashcards from shared canonical knowledge (DONE)
Personal flashcards from the user's notes (TODO)
Save/unsave = playlists, default list "Saved" (DONE)
Note library gated on can_view_own_notes until rewards (DONE as a flag)
Postgres taxonomy + NetworkX cache, not Neo4j (DONE)
Hybrid OCR: Gemini then Azure (DONE)
CI (GitHub Actions) + Render deploy (DONE)
Local .env from .env.example; team API keys in a password manager (DONE as process)
```

MOSAIC — Precise Implementation Order

Category 0 — Backend foundation — DONE

```text
DONE  GitHub repo, Django + DRF apps (users, notes, knowledge, verification, learning)
DONE  JWT, .env.example, README local setup
DONE  Basic tests (auth, notes, verification, learning)
DONE  Docker Compose Postgres + optional backend
DONE  GitHub Actions test/lint/image + Render deploy hook
```

Category 1 — Stabilize the backend

1. PostgreSQL — PARTIAL
   CI and Render use Postgres. Local recommended path is `docker compose up db`. SQLite still works if DATABASE_ENGINE is not postgres. No further "migration project" unless dropping SQLite entirely.

2. Knowledge model relationships — DONE
   DONE: Evidence → ExtractedClaim (`evidence_items`), Flashcard → CanonicalClaim.
   DONE: remove duplicated Source.source_type / access_method declarations.

3. Profile completion — DONE
   DONE: UserProfile signal, POST /api/auth/complete-profile/, Google auth returns profile_required.
   DONE: IsProfileComplete on protected app APIs.

4. Tests/validation — PARTIAL
   DONE: auth, notes permissions, verification supported/contradicted, learning playlist tests.
   DONE: knowledge tests, Google auth tests, note-processing integration tests.

Category 2 — Note processing pipeline — PARTIAL

5. NoteProcessingJob — DONE (states including VERIFIED/FAILED).
6. Job after upload — DONE (`process_note_placeholder(note.id)` in NoteUploadView).
7. Orchestration service — DONE
   DONE: OCR → SourceDocument → ExtractedClaim.
   DONE: call ClaimVerificationService per claim; set job VERIFIED.
   DONE: job.failed_at is written in the fail path; confirm the field exists on the model.
8. Placeholder task — DONE but still synchronous (blocks the upload request). Celery is Category 13.

Category 3 — OCR — DONE (enough for MVP)

9. OCR interface/factory — DONE (HybridOCRProvider, placeholder).
10. Provider choice — DONE for now: Gemini primary, Azure Document Intelligence fallback. Textract/OpenAI not required.
11. Store OCR output — PARTIAL: original file kept; extracted_text + status stored. Rich OCR metadata JSON is TODO.

Category 4 — Claim extraction — DONE (MVP)

12. ClaimExtractionService — DONE (LLM with sentence fallback).
13. Persist ExtractedClaim — DONE.
14. Claim review API — DONE (`/api/knowledge/extracted-claims/` + admin). Mobile review UI is Category 8.

Category 5 — Evidence and verification — DONE

15. Source registry — DONE (models + API; duplicate fields; license workflow is light).
16. Evidence model/API — DONE (`/api/knowledge/evidence/`).
17. Evidence retrieval placeholder — DONE (creates RELATED placeholder if none exist).
18. Verification service — DONE (`POST /api/verification/claims/{id}/verify/`).
19. Confidence scoring — DONE (authority × relevance, corroboration, support vs contradict).
    DONE: auto-run verification from NoteProcessingService.

Category 6 — Canonical knowledge — DONE (MVP)

20. Layer separation — DONE.
21. CanonicalClaim only if SUPPORTED — DONE. PARTIALLY_SUPPORTED correction workflow is TODO.
22. Concept assignment — DONE (NetworkX 1-hop, Gemini pick, UnmappedConceptReview, admin approve).
    DONE: creating ConceptRelationship edges on approve; seed CSE taxonomy from docs/cse_tech_concepts.md.

Category 7 — Flashcards — DONE (MVP) + playlist addition

23. FlashcardGenerationService from CanonicalClaim — DONE (placeholder copy).
24. Provenance on API — DONE (canonical text, concept, evidence, source).
25. Flashcard API — DONE: feed, detail, feedback, progress.
25a. Playlists — DONE (was not in the original list):
     POST/DELETE .../save/ → PlaylistItem
     GET/POST /api/learning/playlists/
     GET/PATCH/DELETE /api/learning/playlists/{id}/
     default playlist "Saved"; cannot save into another user's playlist.
25b. Placeholder explain — DONE: GET /api/learning/canonical-claims/{id}/explain/
25c. Personal vs public environments — TODO (not originally listed; decided in product).

Category 7b — Pipeline closeout — NEXT (backend)

Before or in parallel with mobile:

```text
DONE  Verify each ExtractedClaim inside NoteProcessingService; set VERIFIED
DONE  IsProfileComplete permission
DONE  Fix Source duplicate fields
DONE  knowledge tests + processing-job tests
TODO  Flashcard.environment public|personal + personal feed
DONE  Attach parent/related edges when approving unmapped concepts
```

Category 8 — Mobile MVP — PARTIAL (frontend)

26. Expo + TypeScript scaffold — DONE
27. Login, register, Google sign-in — PARTIAL (backend google-auth exists)
28. Mandatory profile completion screen — DONE
29. Note upload — DONE
30. Processing-status screen (uploaded → failed) — DONE
31. Claim review screen — DONE
32. Public flashcard feed (swipe sequences later) — DONE
33. Flashcard detail — DONE
34. Playlist save/unsave + feedback — DONE (do not build a single "saved" flag UI)
35. In-depth explanation screen (consume placeholder explain API) — DONE
35a. Playlist list / named playlists UI — DONE
35b. Styling of the UI for great UX - TODO

Category 9 — Real RAG — TODO

36–39: embeddings, pgvector, semantic retrieval, LLM explanation with citations.
Current explain endpoint is not RAG.

Category 10 — External ingestion — TODO

40–43: adapters (GitHub, Stack Exchange, arXiv, Wikimedia), license checks, pipeline.
Reddit: evidence only, after legal review. Prefer official CSE/docs sources first.

Category 11 — Recommendations — TODO

44–48 after mobile + personal feed exist. Can use ConceptRelationship (prerequisite/related) later.

Category 12 — Mastery and contributors — TODO

49. Understood action (UserProgress.understood exists; no endpoint) — TODO
50–53. Concept mastery, history, scoring, rewards that set can_view_own_notes.

Category 13 — Production workers and storage — PARTIAL

Hosting is DONE (Render + GH Actions). Still TODO:
54. S3/R2 for media
55–57. Celery + Redis, retries, worker monitoring (replace in-process OCR)

Category 14 — Scale — TODO

58–62. OpenSearch, dedicated graph DB only if NetworkX+Postgres fails, microservices, partnerships, observability.

Category 15 — Social — TODO (do not start)

Friends, chat, comments, likes, sharing, community reputation.

Implementation queue (updated)

```text
DONE   01–04 foundation, relationships (except Source dupes), tests core
DONE   05–08 job + placeholder task (sync)
DONE   09–15 OCR, claims, source/evidence MVP
DONE   16–23 verify, score, canonical, concepts, flashcards
DONE   25a playlists, 25b placeholder explain
DONE   CI/CD + Render + local setup docs

DONE   A. NoteProcessingService → verify_claim → VERIFIED
DONE   B. IsProfileComplete
NEXT   C. Expo mobile against public feed + playlists + upload
NEXT   D. Personal flashcard environment
NEXT   E. Unmapped-concept edges + CSE taxonomy seed

TODO   RAG / pgvector
TODO   Celery + S3
TODO   External ingestion
TODO   Recommendations / mastery / rewards
TODO   Social / scale
```

Order to keep:

```text
Pipeline closeout
      ↓
Mobile (public feed + playlists)
      ↓
Personal environment
      ↓
pgvector/RAG
      ↓
Celery/S3
      ↓
Recommendations/mastery
      ↓
Scale / social
```
