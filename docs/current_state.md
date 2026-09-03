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
Verification app folder exists
Local media settings exist
```

## Authentication

Implemented:

```text
Email/password registration
Email/password login
JWT access and refresh token response
Token refresh route
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
Stronger file validation
Processing job creation after upload
OCR integration
Claim extraction from uploaded note
Real async/background processing
```

## Knowledge

Implemented or being shaped:

```text
Source model
Evidence model
Claim-like model exists from earlier work
Admin/API foundation for source and evidence review
```

Next intended model design:

```text
SourceDocument
ExtractedClaim
Concept
CanonicalClaim
```

Important migration direction:

```text
The earlier Claim model should be treated as the extracted-claim concept or replaced by ExtractedClaim while the project is still young.
Evidence should point to ExtractedClaim.
Flashcard should point to CanonicalClaim.
```

Known cleanup needed:

```text
Remove duplicated fields in Source if present.
Fix related_name typo if present: evidences_items should become evidence_items.
Make model names line up with the architecture before the database becomes costly to change.
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
verification app folder exists
NoteProcessingJob still needs to be finalized if not already added
Placeholder processing task still needs to be added if not already added
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

