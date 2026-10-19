# MOSAIC Architecture

This document explains how MOSAIC is currently being built. It is intended for team members and coding agents so they can continue work without losing the product and technical context.

## Product Definition

MOSAIC is a personal knowledge engine. First users are CSE students. It accepts user-uploaded learning material, extracts claims, verifies them against evidence, stores corrected/canonical knowledge, and teaches through flashcards (public shared feed today; personal note-derived feed later) and explanations.

The core loop is:

```text
Upload knowledge material
-> OCR / parsing
-> claim extraction
-> evidence retrieval
-> verification
-> canonical knowledge
-> flashcards and explanations
-> user feedback and progress
```

## Core Principle

Raw notes are not truth.

MOSAIC must keep these layers separate:

```text
Raw user upload
External/source document
Extracted claim
Evidence
Verified/canonical claim
Learning content
User progress/feedback
```

This separation is important for correctness, privacy, attribution, future reward systems, and preventing unverified user content from becoming trusted knowledge.

## Repository Shape

```text
Mosaic/
  backend/      Django + DRF API
  docs/         architecture, decisions, roadmap, tasks, CSE taxonomy
  docker-compose.yml
  backend/Dockerfile
  .github/workflows/ci-cd.yml
  mobile/       Expo + React Native client (NativeWind and Lucide)
```

## Backend Stack

```text
Django + DRF + SimpleJWT
Local: SQLite for non-vector development or Docker Postgres 16 with pgvector
CI and Render: PostgreSQL
pgvector for evidence embeddings and semantic retrieval
Celery + Redis for asynchronous evidence embedding
OCR: Gemini + Azure fallback
LLM: Gemini for extraction/assignment
```

DRF is used because the Expo mobile app consumes JSON APIs. JWT is used because the app is mobile/API-first rather than a traditional cookie-session website.

## Mobile navigation and learning delivery

The primary mobile navigation has three tabs: **Feed**, **Upload**, and
**Search**. Profile is opened from the upper-right profile control. Its adjacent
library menu provides Notes, Progress, Playlists, and Knowledge; Profile is not
duplicated in that menu.

The feed is backed by persisted `FlashcardFeedEvent` records. Each feed request
has a session UUID, excludes cards served earlier in that session, and ranks
unseen or least-recently viewed cards first. This makes vertical Reel-style
sessions repeat-resistant across launches without storing the feed on the
device.

Topic search resolves exact CSE taxonomy concepts first. For a missing topic it
returns close taxonomy suggestions and cards for the best available match, while
explicitly marking the topic as absent from the taxonomy.

External adapter ingestion persists its `SourceDocument`, extracted claims,
canonical claims, and generated flashcards through the same verification
pipeline used by uploaded notes. Approved adapters are Wikimedia, arXiv,
GitHub, StackExchange, Reddit evidence, and an allow-listed official
documentation adapter for C++, Java, Python, JavaScript/MDN, and TypeScript.

## Apps

Current or planned Django apps:

```text
users
notes
knowledge
verification
learning
```

### users

Responsible for:

```text
User registration
Email/password login
Google sign-in flow
JWT auth
UserProfile
Profile completion
Role/capability flags
```

Authentication has two intended paths:

```text
1. Signup/signin using Django auth
2. Signup/signin using Google account
```

Both paths must create or use a local Django user. Google is only an identity provider; MOSAIC still owns its local user/profile records.

If Google does not provide all required MOSAIC profile fields, those fields must be collected immediately after sign-in and before the user enters the main app.

### notes

Responsible for:

```text
User note uploads
File metadata
Upload validation
Upload status summary
Premium/contributor-gated personal note library
```

Important product decision:

```text
All authenticated users can upload notes.
Only eligible premium/contributor users can list/view their uploaded notes.
```

Uploaded notes feed the MOSAIC knowledge pipeline. They are not only a private storage feature.

### knowledge

Responsible for:

```text
Source registry
Source documents
Extracted claims
Evidence
Concepts
Canonical claims
Admin/review tools
```

Current concepts:

```text
Source
SourceDocument
ExtractedClaim
Evidence
Concept
ConceptRelationship
UnmappedConceptReview
CanonicalClaim
```

Evidence verifies extracted claims (`related_name=evidence_items`). Flashcards point at canonical claims. Concepts are assigned through `ConceptAssignmentService` (NetworkX 1-hop + Gemini, unmapped review in admin).

### verification

Responsible for:

```text
NoteProcessingJob
Pipeline status
OCR provider integration
Claim extraction service
Verification service
Placeholder processing task during MVP wiring
```

Pipeline status values (on both `Note` and `NoteProcessingJob`):

```text
UPLOADED
PROCESSING
OCR_DONE
CLAIMS_EXTRACTED
VERIFIED
FAILED
```

`Note` holds summary status and `extracted_text`. `NoteProcessingJob` is the workflow record.

Upload currently runs `process_note_placeholder` **synchronously** in the request. Orchestration stops after claim extraction; verification is a separate `POST /api/verification/claims/{id}/verify/`.

### learning

Responsible for:

```text
Flashcard API (public canonical feed)
Provenance: Flashcard → CanonicalClaim → ExtractedClaim → Evidence → Source
Playlists (default "Saved" + named lists)
Flashcard feedback
User progress (view counts)
Citation-aware RAG explanation backed by semantically retrieved evidence
Questionnaires & Tiered MCQs (Easy, Moderate, Intermediate, Advanced, Expert)
MasteryBadges (Concept & Superset)
```

Endpoints:

```text
GET    /api/learning/flashcards/
GET    /api/learning/flashcards/{id}/
POST   /api/learning/flashcards/{id}/save/
DELETE /api/learning/flashcards/{id}/save/
POST   /api/learning/flashcards/{id}/feedback/
GET    /api/learning/playlists/
POST   /api/learning/playlists/
GET    /api/learning/playlists/{id}/
PATCH  /api/learning/playlists/{id}/
DELETE /api/learning/playlists/{id}/
GET    /api/learning/progress/
GET    /api/learning/canonical-claims/{id}/explain/
GET    /api/learning/concepts/{id}/mastery-status/
POST   /api/learning/concepts/{id}/questionnaires/start/
POST   /api/learning/questionnaires/{id}/submit/
GET    /api/learning/badges/
```

Save writes `PlaylistItem`. Personal-environment feed is not implemented.

#### Flashcard card types

Flashcard records carry a `card_type` field with three values:

```text
concept_visual  — question + explanation + visual hint + concept tags
recall          — question with progressive answer reveal + optional key points
quick_quiz      — multiple-choice question with correct-answer feedback

quiz_options    — nullable JSON array; [{text, is_correct, explanation}]; quick_quiz cards only
key_points      — nullable JSON array of strings; recall cards only
visual_hint     — nullable char(100); short label or emoji; concept_visual cards only

#### Mobile type layer (Phase 2)

TypeScript types mirroring the serializer live in `mobile/src/types/flashcard.ts`:

```text
FlashcardDTO        — full serializer response shape
FlashcardListResponse — plain array | paginated DRF envelope
CardViewState       — per-card local UI state (reveal, quiz selection, save, understood)
QuizOption          — one multiple-choice option ({text, is_correct, explanation})
initialCardViewState(card) — factory function returning default CardViewState

useFlashcardFeed()  — returns { cards, status, error, currentIndex, viewStates,
                       onCardVisible, revealAnswer, selectOption,
                       toggleSave, markUnderstood, refresh, sessionComplete }


#### Card Template Architecture (Phase 3)
Cards are modular and data-driven, located under `mobile/src/components/cards/`:
```text
CardShell          — Shared viewport container: top badges, middle content, bottom action bar
ConceptVisualCard  — Question, visual icon/hint, explanation, verified claim quotation
RecallCard         — Active-recall prompt with progressive tap-to-reveal answer and key points
QuickQuizCard      — Multiple-choice options with immediate color-coded feedback & explanation
CardRenderer       — Router component rendering the appropriate template based on card_type

  

## Auth Architecture

DRF defaults to authenticated APIs:

```text
DEFAULT_PERMISSION_CLASSES = IsAuthenticated
```

Public endpoints explicitly allow anonymous access:

```text
register
login
Google auth
token refresh
```

Most app APIs should require a valid JWT:

```http
Authorization: Bearer ACCESS_TOKEN
```

## Access Rules

Current access design:

```text
Authenticated users:
- can upload notes
- can view public flashcards
- can save flashcards into playlists
- can submit feedback
- can view their own progress

All authenticated users with a complete profile can list and view their own uploaded notes. Access remains owner-scoped. The premium/contributor gate will be enabled after the project presentation.

Admins:
- can manage source registry
- can manage evidence
- can review claims
- can create/manage flashcards in Django admin
```

Users should never see another user's private uploaded notes.

## Storage Architecture

Current local development storage:

```text
MEDIA_ROOT = backend/media
MEDIA_URL = /media/
```

The app should continue using Django `FileField` instead of manually writing provider-specific storage code in views.

Future production storage should be configured through Django storage settings, probably S3 or S3-compatible object storage.

## OCR And Claim Extraction Architecture

OCR and claim extraction should be separate services:

```text
OCR provider
-> returns extracted text

Claim extraction service
-> receives text
-> returns atomic claims
```

Current service layout:

```text
verification/services/ocr/base.py
verification/services/ocr/factory.py   (HybridOCRProvider, Gemini + Azure)
verification/services/ocr/placeholder.py
verification/services/claim_extraction.py
verification/services/note_processing.py
verification/services/claim_verification.py
verification/services/concept_assignment.py
verification/services/evidence_retrieval.py
verification/tasks.py                  (process_note_placeholder, still in-process)
```

The pipeline should call an interface, not a provider directly:

```python
ocr_text = ocr_provider.extract_text(note.file)
claims = claim_extractor.extract_claims(ocr_text)
```

This keeps provider switching possible.

## API Style

Use `/api/` for all app APIs:

```text
/api/auth/
/api/notes/
/api/knowledge/
/api/verification/
/api/learning/
```

Use app-level `urls.py` files and include them in `config/urls.py`. Keep `config/urls.py` as the project router, not a place for all endpoint definitions.
