# MOSAIC Roadmap

This roadmap separates current work from future work so the team and coding agents can stay focused.

## Current Work

The project is currently building the backend MVP foundation.

The immediate goal is:

```text
Authenticated users can enter the app, upload notes, and consume basic flashcards.
The backend has the data model foundation for source documents, extracted claims, evidence, canonical claims, and processing jobs.
```

## Current Backend Milestone

Finish and stabilize:

```text
users
notes
knowledge
verification
learning
```

### Users

Current/foundation work:

```text
Email/password registration
Email/password login
JWT refresh
UserProfile
Google sign-in
Mandatory immediate profile completion
```

Do next:

```text
Confirm UserProfile fields
Add Google auth endpoint if not complete
Add profile completion endpoint
Add tests for auth flows
```

### Notes

Current/foundation work:

```text
Authenticated upload
File metadata
Upload validation
Owner tracking
Premium/contributor-gated note list/detail
```

Do next:

```text
Improve file validation
Create NoteProcessingJob automatically after upload
Trigger placeholder processing task
Prepare for async processing
```

### Knowledge

Current/foundation work:

```text
Source registry
Evidence model/API
Admin review tools
```

Do next:

```text
Finalize SourceDocument
Finalize ExtractedClaim
Finalize Concept
Finalize CanonicalClaim
Point Evidence to ExtractedClaim
Point Flashcard to CanonicalClaim
Clean up old/duplicate Claim model usage
```

### Verification

Current/foundation work:

```text
verification app exists
processing model/service needs completion
```

Do next:

```text
Add NoteProcessingJob
Add placeholder processing task
Create source document from uploaded note
Create placeholder extracted claim
Update job/note statuses during processing
```

### Learning

Current/foundation work:

```text
Flashcard feed/detail
Save/unsave flashcard
Feedback endpoint
Basic progress summary
Admin tools
```

Do next:

```text
Fix small typos/field mismatches as found
Ensure save/detail/progress work using same user token
Add "understood" or mastery action endpoint later
Ensure flashcards link to CanonicalClaim
```

## Near-Term Sprint Plan

### Sprint 1: Stabilize Backend Foundation

Deliver:

```text
Auth works
Notes upload works
Flashcard feed/detail/save/feedback/progress works
Source/evidence admin/API works
Clean migrations
No generated files in Git
```

Definition of done:

```text
All migrations run cleanly
Admin opens without errors
curl.exe tests pass
Normal user cannot view gated note library
Eligible user can view only their own notes
```

### Sprint 2: Pipeline Wiring

Deliver:

```text
Note upload creates processing job
Placeholder task creates SourceDocument
Placeholder task creates ExtractedClaim
Statuses update correctly
Admin can inspect processing jobs and claims
```

Definition of done:

```text
Upload note
Run placeholder processor
See SourceDocument
See ExtractedClaim
See NoteProcessingJob status
```

### Sprint 3: OCR And Claim Extraction

Deliver:

```text
OCR provider selected
OCR interface added
One provider implemented
Claim extraction service added
Extracted claims stored from real uploaded content
```

Research required before implementation:

```text
Compare Gemini document processing, Azure Document Intelligence, Amazon Textract, and OpenAI vision/document extraction.
Score on handwriting quality, PDF/image support, cost, API simplicity, output structure, latency, and privacy/data terms.
```

### Sprint 4: Verification MVP

Deliver:

```text
Evidence retrieval placeholder
Manual/admin evidence attachment
Verification status updates
CanonicalClaim creation from supported/corrected extracted claims
```

Definition of done:

```text
ExtractedClaim can become supported/contradicted/uncertain.
Supported/corrected knowledge can become CanonicalClaim.
Flashcard can be linked to CanonicalClaim.
```

### Sprint 5: Mobile MVP Shell

Deliver:

```text
Expo app scaffold
Auth screens
Google sign-in screen
Mandatory profile form
Flashcard feed
Flashcard detail
Save/feedback actions
Upload note screen
```

Definition of done:

```text
Mobile app can login, fetch flashcards, save a card, submit feedback, upload a note.
```

## Future Work

These should not distract from the current backend foundation.

### Production Storage

Later:

```text
S3 or S3-compatible object storage
private file access
signed URLs
file deletion lifecycle
```

### Background Jobs

Later:

```text
Celery
Redis
retry policy
dead-letter/failure handling
worker monitoring
```

### PostgreSQL And pgvector

Later:

```text
Move from SQLite to PostgreSQL
Add pgvector
Store embeddings
Add vector retrieval
```

### RAG Explanation

Later:

```text
Retrieve canonical claims
Retrieve evidence
Generate grounded explanation
Return citations/provenance
```

### Recommendation System

Later:

```text
Topic-based recommendations
Saved concepts
Difficulty
Prerequisites
User mastery
Learning history
```

### Reward And Contributor System

Later:

```text
reward points
contributor status
premium eligibility
upload quality scoring
accepted-claim percentage
source/evidence contribution score
```

This system can eventually control:

```text
can_view_own_notes
advanced contribution tools
review privileges
premium features
```

### Social Features

Later only:

```text
friends
chat
comments
likes
sharing
community contributions
reputation
```

Do not build social features before the knowledge pipeline works.

### Scale Architecture

Later only:

```text
OpenSearch/Elasticsearch
dedicated graph database
microservices
source partnerships
licensed external corpora
advanced monitoring
```

The MVP should remain a modular monolith.

