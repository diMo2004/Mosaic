# Graph Report - backend  (2026-10-04)

## Corpus Check
- 103 files · ~13,647 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .example 1)

## Summary
- 569 nodes · 1324 edges · 36 communities (17 shown, 19 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 196 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `590d034d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- verification/tests.py
- Source
- learning/views.py
- knowledge/admin.py
- learning/tests.py
- django_db
- ExtractedClaim
- os
- HybridOCRProvider
- IsProfileComplete
- EmbeddingService
- users/views.py
- SourceDocument
- django_apps
- Evidence
- knowledge/models.py
- GoogleAuthTests
- KnowledgeAPIPermissionTests
- PlaceholderOCRProvider

## God Nodes (most connected - your core abstractions)
1. `Source` - 39 edges
2. `Evidence` - 36 edges
3. `ExtractedClaim` - 29 edges
4. `IngestionItem` - 28 edges
5. `ClaimVerificationService` - 25 edges
6. `SourceDocument` - 23 edges
7. `CanonicalClaim` - 23 edges
8. `Concept` - 21 edges
9. `RAGExplanationService` - 20 edges
10. `FlashcardAPITests` - 20 edges

## Surprising Connections (you probably didn't know these)
- `ExternalIngestionPipeline` --uses--> `ClaimExtractionService`  [INFERRED]
  knowledge/ingestion/pipeline.py → verification/services/claim_extraction.py
- `ExternalIngestionPipeline` --uses--> `ClaimVerificationService`  [INFERRED]
  knowledge/ingestion/pipeline.py → verification/services/claim_verification.py
- `EvidenceRetrievalServiceTests` --uses--> `Source`  [INFERRED]
  learning/tests.py → knowledge/models.py
- `FlashcardAPITests` --uses--> `Source`  [INFERRED]
  learning/tests.py → knowledge/models.py
- `GroundedExplanationAPITests` --uses--> `Source`  [INFERRED]
  learning/tests.py → knowledge/models.py

## Import Cycles
- None detected.

## Communities (36 total, 19 thin omitted)

### Community 0 - "verification/tests.py"
Cohesion: 0.06
Nodes (33): django_contrib, django_contrib_auth_models, django_core_files_uploadedfile, django_db_models_signals, django_dispatch, django_test, django_utils, NoteAdmin (+25 more)

### Community 1 - "Source"
Cohesion: 0.09
Nodes (33): base64, dataclasses, decimal, ArxivAdapter, Fetches academic computer science preprints from arXiv., GitHubAdapter, Fetches README and doc markdown from GitHub repositories., Fetches community discussion strictly for evidence attribution after legal… (+25 more)

### Community 2 - "learning/views.py"
Cohesion: 0.08
Nodes (29): django_db_models, FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin (+21 more)

### Community 3 - "knowledge/admin.py"
Cohesion: 0.07
Nodes (30): action, django_core_management_base, django_utils_text, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline (+22 more)

### Community 4 - "learning/tests.py"
Cohesion: 0.10
Nodes (16): Any, CanonicalClaim, RuntimeError, RAGExplanationService, RAGExplanationServiceError, Raised when RAG explanation generation fails., FakeEvidenceRetriever, FakeExplanationClient (+8 more)

### Community 5 - "django_db"
Cohesion: 0.08
Nodes (17): django_db, django_db_models_deletion, Migration, Migration, Migration, Migration, Migration, Migration (+9 more)

### Community 6 - "ExtractedClaim"
Cohesion: 0.09
Nodes (12): django_shortcuts, ExtractedClaim, FlashcardGenerationService, Generate flashcards from a given canonical claim., FlashcardAPITests, rest_framework_response, rest_framework_views, ClaimVerificationService (+4 more)

### Community 7 - "os"
Cohesion: 0.07
Nodes (16): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, dj_database_url, django_core_asgi, django_core_wsgi, dotenv, google_genai, json (+8 more)

### Community 8 - "HybridOCRProvider"
Cohesion: 0.12
Nodes (13): google_api_core, io, mimetypes, pil, OCRProvider, ABC, get_azure_client(), get_gemini_model() (+5 more)

### Community 9 - "IsProfileComplete"
Cohesion: 0.13
Nodes (14): CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes., Meta, NoteDetailSerializer, NoteUploadSerializer, NoteDetailView, NoteListView (+6 more)

### Community 10 - "EmbeddingService"
Cohesion: 0.14
Nodes (12): google, build_embedding_text(), Command, BaseCommand, EmbeddingService, EmbeddingServiceError, RuntimeError, Raised when an embedding cannot be generated. (+4 more)

### Community 11 - "users/views.py"
Cohesion: 0.14
Nodes (16): URL configuration for config project. The `urlpatterns` list routes URLs to…, django_conf_urls_static, django_urls, google_auth_transport, google_oauth2, rest_framework_simplejwt_tokens, rest_framework_simplejwt_views, CompleteProfileSerializer (+8 more)

### Community 12 - "SourceDocument"
Cohesion: 0.19
Nodes (14): SourceDocument, CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer, CanonicalClaimViewSet (+6 more)

### Community 13 - "django_apps"
Cohesion: 0.12
Nodes (11): django_apps, KnowledgeConfig, AppConfig, LearningConfig, AppConfig, NotesConfig, AppConfig, AppConfig (+3 more)

### Community 14 - "Evidence"
Cohesion: 0.28
Nodes (4): Evidence, EvidenceRetrievalService, EvidenceRetrievalServiceTests, TestCase

### Community 15 - "knowledge/models.py"
Cohesion: 0.26
Nodes (8): django_conf, Migration, EvidenceRetrievalError, RuntimeError, Raised when semantic evidence retrieval cannot be completed., pgvector_django, pgvector_django_vector, typing

### Community 16 - "GoogleAuthTests"
Cohesion: 0.22
Nodes (4): AuthTests, GoogleAuthTests, APITestCase, patch

## Knowledge Gaps
- **18 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+13 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 206 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Source` connect `Source` to `verification/tests.py`, `knowledge/admin.py`, `learning/tests.py`, `django_db`, `ExtractedClaim`, `SourceDocument`, `Evidence`, `knowledge/models.py`, `KnowledgeAPIPermissionTests`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `Evidence` connect `Evidence` to `verification/tests.py`, `Source`, `knowledge/admin.py`, `learning/tests.py`, `django_db`, `ExtractedClaim`, `EmbeddingService`, `SourceDocument`, `knowledge/models.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `ExtractedClaim` connect `ExtractedClaim` to `verification/tests.py`, `Source`, `knowledge/admin.py`, `learning/tests.py`, `django_db`, `SourceDocument`, `Evidence`, `knowledge/models.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `ExternalIngestionPipeline`) actually correct?**
  _`Evidence` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ExtractedClaim` (e.g. with `ExternalIngestionPipeline` and `ExtractedClaimSerializer`) actually correct?**
  _`ExtractedClaim` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `IngestionItem` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`IngestionItem` has 8 INFERRED edges - model-reasoned connections that need verification._