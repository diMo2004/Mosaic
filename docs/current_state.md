# Current State

This document describes where the MOSAIC backend currently stands. It should be updated whenever a meaningful project milestone is completed.

## Project Status

The project is in early backend MVP development.

Completed or partially completed:

```text
Phase 0 repo setup
Django + DRF backend scaffold
JWT login/refresh working
Basic users app
Basic notes app
Basic knowledge app
Basic learning app
Verification app and service layer started
Local media settings exist
Backend tests started for auth, notes, permissions, and verification
```

## Authentication

Implemented:

```text
Email/password registration
Email/password login
JWT access and refresh token response
Token refresh route
UserProfile model
UserProfile auto-create signal for newly created users
```

Known working endpoint:

```text
POST /api/auth/login/
```

Expected login response:

```json
{
  "refresh": "...",
  "access": "..."
}
```

Planned but not fully completed:

```text
Google sign-in
Immediate mandatory profile completion after Google sign-in
Profile-completion permission blocking
```

Recent test-related correction:

```text
Tests must use /api/auth/register/ and /api/auth/login/, not /api/users/register/ or /api/users/login/.
RegisterSerializer should not create duplicate UserProfile rows now that the post_save signal creates profiles automatically.
Use UserProfile.objects.get_or_create(...) when registration needs to update profile fields.
```

## Notes

Implemented:

```text
Note model
Authenticated upload endpoint
Local media storage
Owner field
Basic file metadata
Basic upload status
Premium/contributor permission for viewing own notes
Owner-filtered list/detail views
Notes admin registration
Tests started for upload and note-library permissions
```

Important product state:

```text
All authenticated users should be allowed to upload notes.
Only eligible users should list or view their uploaded note history/details.
```

Current intended note endpoints:

```text
POST /api/notes/upload/
GET  /api/notes/
GET  /api/notes/{id}/
```

Still needs:

```text
Continue hardening file validation
Processing job creation after upload
OCR integration
Claim extraction from uploaded note
Real async/background processing
```

## Knowledge

Implemented or being shaped:

```text
Source model
SourceDocument model
ExtractedClaim model
Evidence model
Concept model
CanonicalClaim model
Admin/API foundation for source and evidence review
```

Important model direction:

```text
The earlier Claim model should be treated as the extracted-claim concept or replaced by ExtractedClaim while the project is still young.
Evidence should point to ExtractedClaim.
Flashcard should point to CanonicalClaim.
```

Known cleanup needed:

```text
Remove duplicated fields in Source if present.
Fix related_name typo if still present: evidences_items should become evidence_items.
Make model names line up with the architecture before the database becomes costly to change.
```

Recent test-related correction:

```text
SourceDocument currently uses DOCUMENT_TYPE_WEBPAGE, not DOCUMENT_TYPE_WEB_PAGE.
Tests should either use SourceDocument.DOCUMENT_TYPE_WEBPAGE or the model constant should be renamed consistently.
```

## Learning

Implemented or partially implemented:

```text
Flashcard model
SavedFlashcard model
FlashcardFeedback model
UserProgress model
Flashcard feed/detail views
Save/unsave endpoint
Feedback endpoint
Progress summary endpoint
Admin registrations
Tests started around flashcard creation through verification
```

Current intended learning endpoints:

```text
GET    /api/learning/flashcards/
GET    /api/learning/flashcards/{id}/
POST   /api/learning/flashcards/{id}/save/
DELETE /api/learning/flashcards/{id}/save/
POST   /api/learning/flashcards/{id}/feedback/
GET    /api/learning/progress/
```

Recently encountered fixes:

```text
Use get_or_create, not get_or_created.
Use aggregate(total=Sum("view_count")).get("total") or 0.
Use SavedFlashcard.objects.filter(user=request.user), not flashcard=request.user.
Use raw URLs with curl.exe, not Markdown links.
```

## Verification

Current state:

```text
verification app exists
claim verification service started
evidence retrieval placeholder planned/started
verification tests started
prompt template module started
NoteProcessingJob still needs to be finalized if not already added
placeholder note-processing task still needs to be finalized if not already added
```

Planned model:

```text
NoteProcessingJob
- note
- status
- error_message
- started_at
- completed_at
- created_at
- updated_at
```

Planned status states:

```text
UPLOADED
PROCESSING
OCR_DONE
CLAIMS_EXTRACTED
VERIFIED
FAILED
```

Current verification rule:

```text
CanonicalClaim should be created only after an ExtractedClaim is verified as supported.
Flashcards should be generated from CanonicalClaim, not raw notes or unsupported extracted claims.
```

Recent test-related corrections:

```text
Use update_fields, not update_field, when saving a model with selected fields.
Use the actual ExtractedClaim note field name consistently, currently reviewed_notes if the model has that field.
```

## Tests

Current test coverage has started for:

```text
auth registration/login
note upload
note list permission gating
verification service behavior
canonical claim creation
flashcard generation from verified claims
```

Known test direction:

```text
Keep tests aligned with real URLs.
Prefer fixing project wiring over weakening tests.
Do not rely on manually created profiles in tests now that the user profile signal exists.
Run python manage.py test before committing backend behavior changes.
```

## Local Development Notes

Use `curl.exe` in PowerShell, not `curl`, because PowerShell aliases `curl` to `Invoke-WebRequest`.

Correct:

```powershell
curl.exe -X GET "http://127.0.0.1:8000/api/learning/flashcards/" `
  -H "Authorization: Bearer $token"
```

Incorrect:

```powershell
curl -X GET "[http://127.0.0.1:8000/api/learning/flashcards/](http://127.0.0.1:8000/api/learning/flashcards/)"
```

Do not paste Markdown link syntax into terminal commands.

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
docs
```
