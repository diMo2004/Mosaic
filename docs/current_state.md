# Current State

This document describes where MOSAIC currently stands. Update it after each meaningful milestone.

## Project Status

The backend MVP through **flashcards (tasks category 7)** is largely implemented. Category 8 (mobile) is partially implemented, Category 9 (Real RAG) is complete, **Category 10 (External Ingestion)** is complete, and **Category 12 (Concept Mastery Badges & Questionnaire Engine)** is implemented. Production-shaped infrastructure exists for **local Docker Postgres**, **pgvector**, **Celery/Redis evidence embedding**, **GitHub Actions CI**, and **Render deploy**. OCR/note-processing workers and S3/R2 remain future work.

First product audience: **CSE students**.

Completed or in place:

```text
Django + DRF + SimpleJWT
users, notes, knowledge, verification, learning apps
Email/password register + login + token refresh
Google auth endpoint + complete-profile endpoint
Note upload (all authenticated users)
Gated note list/detail (can_view_own_notes)
NoteProcessingJob + synchronous process_note_placeholder after upload
Hybrid OCR (Gemini primary, Azure fallback, placeholder if no keys)
LLM/fallback claim extraction
Source, SourceDocument, ExtractedClaim, Evidence, Concept,
ConceptRelationship, UnmappedConceptReview, CanonicalClaim
Claim verification with authority/relevance scoring
CanonicalClaim + Flashcard only for SUPPORTED claims
Concept assignment via Postgres taxonomy + NetworkX 1-hop cache
Flashcard APIs: feed, detail, playlist save/unsave, feedback, progress
Playlist list/create/detail
Citation-aware RAG explanation endpoint using semantic evidence retrieval
Asynchronous evidence embedding with Celery and Redis
External source ingestion (GitHub, arXiv, Wikimedia, StackExchange, Reddit)
License and policy validation engine for external ingestion
CLI management command: ingest_external
Questionnaires & 5-tier MCQ engine (Easy to Expert) with dynamic capped quotas & ratchet rule
Concept MasteryBadge & Superset MasteryBadge (10 subtopics) models and services
Learning, verification, and ingestion tests
CI (pytest-equivalent: python manage.py test) + Docker image build + Render hook
README local-setup section
```

Not started or incomplete:

```text
Expo / mobile app (scaffold and screen shells exist; styling & full wiring in progress)
IsProfileComplete enforced on app APIs
Auto-verify claims at the end of note processing (job often stops at CLAIMS_EXTRACTED)
Personal vs public flashcard environments
LLM flashcard copy
S3/R2 media storage
Celery workers for OCR/note processing, production retries, and monitoring
Understood action endpoint (task 49)
Recommendations and social
```

## Authentication

Implemented:

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/
POST /api/auth/google-auth/
POST /api/auth/complete-profile/
UserProfile auto-create signal
Google ID token verified on the backend
Missing Google profile fields returned as profile_required
```

Still needed:

```text
IsProfileComplete permission on protected app APIs
Mobile Google sign-in + immediate profile form
```

Login still returns:

```json
{
  "refresh": "...",
  "access": "..."
}
```

## Notes

Implemented:

```text
POST /api/notes/upload/
GET  /api/notes/
GET  /api/notes/{id}/
Owner stored on every note
Upload triggers process_note_placeholder(note.id) in-process
Note.status + extracted_text + processing_error
```

Access:

```text
Any authenticated user can upload.
Only users with profile.can_view_own_notes can list/detail their notes.
That flag stays gated until a later reward/contributor system.
```

Still needed:

```text
Hardening file validation
Async OCR/note-processing workers (Celery) instead of blocking the upload request
Wire verification into the processing job so status can become VERIFIED
Fix NoteProcessingJob.failed_at if the fail path still writes a field that is not on the model
```

## Knowledge

Implemented:

```text
Source, SourceDocument, ExtractedClaim, Evidence
Concept, ConceptRelationship, UnmappedConceptReview
CanonicalClaim
Admin for sources, evidence, claims, concepts, relationships, unmapped review
APIs:
  /api/knowledge/sources/
  /api/knowledge/source-documents/
  /api/knowledge/extracted-claims/
  /api/knowledge/canonical-claims/
  /api/knowledge/evidence/
```

Graph strategy (category 6):

```text
Taxonomy lives in PostgreSQL (Concept + ConceptRelationship).
NetworkX DiGraph is an in-memory cache for assignment.
assign_concept: keyword anchors → 1-hop candidates → Gemini pick or UnmappedConceptReview.
Admin approve_and_add_to_graph creates a Concept and invalidates the cache.
Approved concepts do not yet get parent/related edges automatically.
```

External Ingestion (category 10):

```text
BaseExternalAdapter & IngestionItem DTO
LicenseChecker policy enforcement (AI extraction rights, redistribution, scraping permissions)
Reddit safety gate: strictly restricted to community evidence after legal review approval
Adapters:
  - GitHubAdapter (README/docs, auto license detection, rate-limit handling)
  - ArxivAdapter (CS preprints, academic authority)
  - WikimediaAdapter (Wikipedia CS definitions, CC-BY-SA 4.0)
  - StackExchangeAdapter (Stack Overflow / CSE technical answers)
  - RedditAdapter (Community discussion evidence only)
ExternalIngestionPipeline: adapter -> license check -> SourceDocument -> ClaimExtraction -> Verification -> Canonical Knowledge / Evidence
Management CLI: python manage.py ingest_external <adapter> <target>
```

Still needed:

```text
Remove duplicated Source.source_type / access_method field declarations if still in models
Attach taxonomy edges when approving unmapped concepts
Additional end-to-end integration tests for high-volume batch ingestion
```

## Verification

Implemented:

```text
NoteProcessingJob
NoteProcessingService (OCR → SourceDocument → ExtractedClaim)
OCR interface + HybridOCRProvider + placeholder
ClaimExtractionService (LLM with fallback)
EvidenceRetrievalService placeholder
ClaimVerificationService (SUPPORTED / CONTRADICTED / PARTIALLY_SUPPORTED / UNCERTAIN)
Authority × relevance scoring + corroboration
POST /api/verification/claims/{id}/verify/
CanonicalClaim + Flashcard only when SUPPORTED
ConceptAssignmentService
verification tests for supported vs contradicted
```

Pipeline gap:

```text
Upload processing currently stops at CLAIMS_EXTRACTED.
It does not call verify_claim on each extracted claim.
VERIFIED job status is defined but not reached by the orchestrator.
```

## Learning

Implemented:

```text
FlashcardGenerationService from CanonicalClaim (placeholder copy)
Flashcard.source_claim → CanonicalClaim
Feed/detail include canonical text, concept, evidence provenance
Playlists + PlaylistItems (default playlist name "Saved")
POST/DELETE /api/learning/flashcards/{id}/save/ writes playlist items, not SavedFlashcard
GET/POST /api/learning/playlists/
GET/PATCH/DELETE /api/learning/playlists/{id}/
Feedback, progress summary, view_count on detail
GET /api/learning/canonical-claims/{id}/explain/ (semantic evidence retrieval + citation-validated Gemini explanation)
learning/tests.py for feed, detail, playlist save, permissions
```

RAG implementation:

```text
Evidence.embedding is a 768-dimensional pgvector field.
EmbeddingService uses Gemini gemini-embedding-001 with output_dimensionality=768.
EvidenceRetrievalService performs cosine-distance semantic search.
RAGExplanationService builds grounded prompts from canonical claim text and evidence.
Citations are validated and provider/retrieval failures return controlled errors.
```

Product rules already decided, not fully modeled:

```text
Public environment: flashcards from shared canonical knowledge (current feed).
Personal environment: flashcards derived from that user's notes (not implemented).
Save/unsave is playlist membership.
```

Mastery and Questionnaire engine (category 12 - implemented):

```text
Models: Questionnaire, QuestionnaireQuestion, MasteryBadge
Dynamic Tier Quotas: Easy 20% (cap 15), Moderate 35% (cap 30), Intermediate 50% (cap 50), Advanced 65% (cap 75), Expert 80% (cap 100).
Ratchet Rule: Monotonic non-decreasing progression. Unlocked tiers remain permanently unlocked.
5 Difficulty Questionnaires: 10 MCQs each. Pass at 8/10 (Easy-Intermediate) and 5/10 (Advanced-Expert).
Retakes exclude previously asked questions for that user.
Expert mode features zero process-of-elimination scope with subtle technical distractors.
Concept MasteryBadge awarded upon passing all 5 tiers.
Superset MasteryBadge awarded when 10 subtopics (or all child subtopics if < 10) are mastered.
Note access (can_view_own_notes) is decoupled from badge rewards.
```

Still needed:

```text
environment/owner fields on Flashcard
GET personal feed
LLM-written cards
Understood action endpoint (task 49)
Swipe sequences
```

## Infra And Local Dev

Implemented:

```text
backend/.env.example + copy to .env
settings load backend/.env
docker-compose.yml: Postgres 16 + optional backend container
GitHub Actions: tests on Postgres 16, flake8, Docker build, Render deploy hook on main
Render hosts the deployed backend
Celery + Redis configuration and asynchronous evidence embedding task
PostgreSQL pgvector migration for evidence embeddings
```

Local run rule:

```text
Option A: docker compose up db -d, then venv + runserver (recommended).
Option B: docker compose up for the API container.
Do not run both (port 8000 clash).
Compose backend does not read backend/.env unless env_file is added.
```

Celery local development:

```text
Worker: python -m celery -A config worker --loglevel=INFO --pool=solo
Broker: redis://127.0.0.1:6379/0
Results: redis://127.0.0.1:6379/1
```

Celery currently handles evidence embedding only. OCR and note processing remain synchronous.

Secrets:

```text
Local .env is gitignored.
Team Gemini/Google/Azure *dev* keys live in a password manager vault.
Render environment tab holds production secrets.
```

## Tests

Covered:

```text
users: register, login tokens
notes: upload, gated list
verification: supported → canonical + flashcard; contradicted → none
learning: generator provenance, feed, detail progress, playlist save/unsave, foreign playlist 404, feedback, progress counts, RAG citations and provider failures
RAG: embedding validation, semantic retrieval, citation validation, API serialization, controlled failures
ingestion: policy & license enforcement, adapter integration, source document creation and claim extraction
```

Empty or thin:

```text
knowledge/tests.py
Google auth / complete-profile tests
Note processing integration tests
```

Run:

```text
cd backend
python manage.py test
```

CI runs the same command with DATABASE_URL pointing at the Actions Postgres service.

## Git Hygiene

Do not commit:

```text
backend/db.sqlite3
backend/media/
backend/.env
__pycache__/
*.pyc
.venv/
```

Commit:

```text
source files
migrations
requirements.txt
.env.example
docs (including docs/tasks.md)
```
