# Architecture Decisions

This document records decisions already made. Coding agents and team members should preserve these unless the team explicitly decides to change them.

## 1. MOSAIC Is A Knowledge Engine, Not Just A Flashcard App

MOSAIC should be built around the pipeline:

```text
ingest -> extract -> verify -> canonicalize -> teach
```

Do not reduce the architecture to raw note storage plus AI flashcard generation.

## 2. Raw Notes Are Not Canonical Truth

User notes are input/evidence. They are not automatically trusted.

Preserve separation between:

```text
raw uploaded note
source document
extracted claim
evidence
canonical claim
flashcard
```

Do not build features that mix raw notes directly into canonical knowledge without verification.

## 3. Upload Is Core, Note Library Is Gated

All authenticated users should be able to upload notes because uploads feed MOSAIC's knowledge-building process.

However:

```text
Seeing upload history
Viewing note details
Inspecting personal uploaded-note records
```

are premium/contributor-gated features.

Do not block note upload behind premium/contributor permissions. Block only note list/detail access.

## 4. Store Note Owner Even If User Cannot View Note History

Every uploaded note must keep an owner.

Reason:

```text
privacy
auditing
abuse prevention
future premium features
reward/contributor scoring
data deletion requests
```

Do not make uploaded notes anonymous at the database level.

## 5. Use A Modular Monolith First

Start with Django apps inside one backend project:

```text
users
notes
knowledge
verification
learning
```

Do not split into microservices during the MVP.

## 6. Use PostgreSQL Later, SQLite Is Fine Locally For Now

SQLite is acceptable for early local development.

The intended production database is PostgreSQL. pgvector should be introduced later when embeddings/vector search become necessary.

Do not introduce a separate graph database in the MVP.

## 7. Use Django REST Framework

MOSAIC is API-first because it will have a mobile frontend.

Use DRF serializers, views/viewsets, permissions, and routers instead of manually hand-writing JSON parsing everywhere.

## 8. Use JWT For API Authentication

Mobile/API auth should use SimpleJWT.

Frontend requests should use:

```http
Authorization: Bearer ACCESS_TOKEN
```

Do not rely on Django browser sessions for the mobile API.

## 9. Google Auth Must Still Create A Local Django User

Google is an identity provider, not the main user database.

Google sign-in flow:

```text
frontend gets Google ID token
backend verifies Google ID token
backend creates/fetches local Django User
backend creates/fetches UserProfile
backend returns MOSAIC JWT tokens only through backend auth flow
```

Do not trust Google tokens without backend verification.

## 10. Profile Completion Must Be Immediate

If Google does not provide all MOSAIC-required profile details, the missing fields must be collected immediately after sign-in before the user enters the app.

Do not postpone this through a passive "complete profile later" option.

## 11. Evidence Verifies Extracted Claims

Evidence should attach to `ExtractedClaim`.

Conceptually:

```text
ExtractedClaim -> Evidence -> verification status
```

`CanonicalClaim` is created after verification/correction.

## 12. Flashcards Come From Canonical Knowledge

Flashcards should point to `CanonicalClaim`, not directly to raw notes or unverified extracted claims.

Reason:

```text
flashcards teach users
teaching content must be verified/canonical
```

## 13. OCR And Claim Extraction Are Separate Services

Do not merge OCR and claim extraction into one hardcoded provider-specific function.

Target interface:

```python
ocr_text = ocr_provider.extract_text(note.file)
claims = claim_extractor.extract_claims(ocr_text)
```

This keeps provider switching possible.

## 14. Use FileField And Storage Configuration

Keep file storage behind Django's storage system.

Current local storage:

```text
MEDIA_ROOT = backend/media
MEDIA_URL = /media/
```

Future production storage should be added through Django storage settings, not provider-specific code inside upload views.

## 15. Admin Review Is Part Of The MVP Foundation

Django admin should support:

```text
source review
evidence review
claim review
flashcard creation/review
processing job inspection
```

Human review is especially important for uncertain, contradicted, or high-stakes claims.

## 16. Use `curl.exe` On Windows

In PowerShell, `curl` is often an alias and behaves differently.

Use:

```powershell
curl.exe
```

Also use raw URLs, not Markdown links.

## 17. Do Not Commit Generated/Local Files

Never commit:

```text
.env
.venv/
db.sqlite3
media/
__pycache__/
*.pyc
```

Commit `.env.example`, migrations, source files, docs, and requirements.

