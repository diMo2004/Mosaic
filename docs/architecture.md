# MOSAIC Architecture

This document explains how MOSAIC is currently being built. It is intended for team members and coding agents so they can continue work without losing the product and technical context.

## Product Definition

MOSAIC is a personal knowledge engine. It accepts user-uploaded learning material, extracts claims, verifies them against evidence, stores corrected/canonical knowledge, and uses that knowledge to teach through flashcards and explanations.

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

The project is being built as a monorepo:

```text
Mosaic/
  backend/      Django + DRF API
  mobile/       React Native + Expo app, later/currently planned
  docs/         architecture, decisions, roadmap, team context
  infra/        Docker/deployment, later/currently planned
  .github/      CI/CD, later/currently planned
```

## Backend Stack

Current backend direction:

```text
Django
Django REST Framework
SimpleJWT
SQLite for local development
PostgreSQL planned
pgvector planned later
Celery + Redis planned later
```

DRF is used because the frontend/mobile app will consume JSON APIs. JWT is used because the app is mobile/API-first rather than a traditional cookie-session website.

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
CanonicalClaim
```

Evidence should verify extracted claims. Flashcards should be generated from canonical claims, not directly from raw uploaded notes.

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

The planned pipeline status values are:

```text
UPLOADED
PROCESSING
OCR_DONE
CLAIMS_EXTRACTED
VERIFIED
FAILED
```

The `Note` model may keep a summary status, while `NoteProcessingJob` keeps the actual processing workflow record.

### learning

Responsible for:

```text
Flashcard API
Flashcard details
Saved flashcards
Flashcard feedback
Basic user progress
```

Current intended endpoints:

```text
GET    /api/learning/flashcards/
GET    /api/learning/flashcards/{id}/
POST   /api/learning/flashcards/{id}/save/
DELETE /api/learning/flashcards/{id}/save/
POST   /api/learning/flashcards/{id}/feedback/
GET    /api/learning/progress/
```

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
- can view flashcards
- can save flashcards
- can submit feedback
- can view their own progress

Premium/contributor users:
- can list their own uploaded notes
- can view their own note details

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

Suggested service layout:

```text
verification/services/ocr/base.py
verification/services/ocr/gemini.py
verification/services/ocr/azure.py
verification/services/claim_extraction.py
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
/api/learning/
```

Use app-level `urls.py` files and include them in `config/urls.py`. Keep `config/urls.py` as the project router, not a place for all endpoint definitions.

