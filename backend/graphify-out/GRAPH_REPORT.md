# Graph Report - backend  (2026-10-04)

## Corpus Check
- 105 files · ~15,113 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .example 1)

## Summary
- 599 nodes · 1431 edges · 42 communities (22 shown, 20 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 217 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8e619675`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- knowledge/tests.py
- Source
- learning/views.py
- knowledge/admin.py
- Evidence
- django_db
- FlashcardAPITests
- os
- HybridOCRProvider
- Note
- EmbeddingService
- ClaimVerificationService
- knowledge/views.py
- django_apps
- verification/tests.py
- rag_explanation.py
- GoogleAuthTests
- ClaimVerificationServiceTests
- PlaceholderOCRProvider
- django_conf
- ConceptRelationship
- ClaimExtractionService
- settings.py
- manage.py
- get_extractor_model

## God Nodes (most connected - your core abstractions)
1. `Source` - 39 edges
2. `Evidence` - 36 edges
3. `Concept` - 30 edges
4. `ExtractedClaim` - 29 edges
5. `IngestionItem` - 28 edges
6. `ClaimVerificationService` - 25 edges
7. `SourceDocument` - 23 edges
8. `CanonicalClaim` - 23 edges
9. `MasteryService` - 21 edges
10. `RAGExplanationService` - 20 edges

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

## Communities (42 total, 20 thin omitted)

### Community 0 - "knowledge/tests.py"
Cohesion: 0.07
Nodes (30): django_contrib_auth_models, django_core_files_uploadedfile, django_db_models_signals, django_dispatch, django_shortcuts, django_test, django_urls, google_auth_transport (+22 more)

### Community 1 - "Source"
Cohesion: 0.09
Nodes (34): base64, dataclasses, decimal, ArxivAdapter, Fetches academic computer science preprints from arXiv., GitHubAdapter, Fetches README and doc markdown from GitHub repositories., Fetches community discussion strictly for evidence attribution after legal… (+26 more)

### Community 2 - "learning/views.py"
Cohesion: 0.06
Nodes (47): django_db_models, Concept, FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register (+39 more)

### Community 3 - "knowledge/admin.py"
Cohesion: 0.19
Nodes (12): action, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, register (+4 more)

### Community 4 - "Evidence"
Cohesion: 0.08
Nodes (20): Any, CanonicalClaim, Evidence, EvidenceRetrievalService, RuntimeError, RAGExplanationService, RAGExplanationServiceError, Raised when RAG explanation generation fails. (+12 more)

### Community 5 - "django_db"
Cohesion: 0.07
Nodes (19): django_db, django_db_models_deletion, Migration, Migration, Migration, Migration, Migration, embed_evidence_task() (+11 more)

### Community 6 - "FlashcardAPITests"
Cohesion: 0.17
Nodes (3): FlashcardGenerationService, Generate flashcards from a given canonical claim., FlashcardAPITests

### Community 7 - "os"
Cohesion: 0.22
Nodes (5): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, django_core_asgi, django_core_wsgi, os

### Community 8 - "HybridOCRProvider"
Cohesion: 0.11
Nodes (14): google_api_core, google_genai, io, mimetypes, pil, OCRProvider, ABC, get_azure_client() (+6 more)

### Community 9 - "Note"
Cohesion: 0.07
Nodes (21): URL configuration for config project. The `urlpatterns` list routes URLs to…, django_conf_urls_static, django_contrib, NoteAdmin, register, Meta, Note, CanViewOwnNotes (+13 more)

### Community 10 - "EmbeddingService"
Cohesion: 0.11
Nodes (11): django_core_management_base, build_embedding_text(), Command, BaseCommand, EmbeddingService, EmbeddingServiceError, RuntimeError, Raised when an embedding cannot be generated. (+3 more)

### Community 11 - "ClaimVerificationService"
Cohesion: 0.15
Nodes (9): ClaimVerificationService, atomic, ConceptAssignmentService, Finds direct keywor matches in text against concept names., Retrieves a focused 1-hop sub-graph around anchor nodes. Returns a list of…, Assigns an official Concept from the sub-graph. If the text contains an…, EvidenceRetrievalService, APIView (+1 more)

### Community 12 - "knowledge/views.py"
Cohesion: 0.20
Nodes (13): CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer, CanonicalClaimViewSet, EvidenceViewSet (+5 more)

### Community 13 - "django_apps"
Cohesion: 0.12
Nodes (11): django_apps, KnowledgeConfig, AppConfig, LearningConfig, AppConfig, NotesConfig, AppConfig, AppConfig (+3 more)

### Community 14 - "verification/tests.py"
Cohesion: 0.28
Nodes (7): django_utils, ExtractedClaim, NoteProcessingJobAdmin, register, Meta, NoteProcessingJob, NoteProcessingService

### Community 15 - "rag_explanation.py"
Cohesion: 0.24
Nodes (8): Migration, EvidenceRetrievalError, RuntimeError, Raised when semantic evidence retrieval cannot be completed., logging, pgvector_django, pgvector_django_vector, typing

### Community 16 - "GoogleAuthTests"
Cohesion: 0.22
Nodes (4): AuthTests, GoogleAuthTests, APITestCase, patch

### Community 17 - "ClaimVerificationServiceTests"
Cohesion: 0.18
Nodes (8): override_settings, ClaimVerificationServiceTests, NoteProcessJobIntegrationTests, patch, TestCase, test_embedding_task_skips_existing_embedding(), test_embedding_task_stores_vector(), test_placeholder_evidence_queues_embedding_after_commit()

### Community 36 - "django_conf"
Cohesion: 0.27
Nodes (6): django_conf, django_utils_text, google, json, networkx, re

### Community 37 - "ConceptRelationship"
Cohesion: 0.18
Nodes (7): Command, BaseCommand, ConceptRelationship, Meta, UnmappedConceptReview, get_cached_nx_graph(), Builds and caches the NetworkX in-memory graph from PostgreSQL.

### Community 39 - "settings.py"
Cohesion: 0.40
Nodes (3): dj_database_url, dotenv, pathlib

### Community 40 - "manage.py"
Cohesion: 0.40
Nodes (4): main(), Django's command-line utility for administrative tasks., Run administrative tasks., sys

## Knowledge Gaps
- **19 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+14 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 213 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Source` connect `Source` to `knowledge/tests.py`, `knowledge/admin.py`, `Evidence`, `ConceptRelationship`, `FlashcardAPITests`, `django_db`, `EmbeddingService`, `ClaimVerificationService`, `knowledge/views.py`, `verification/tests.py`, `ClaimVerificationServiceTests`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `Concept` connect `learning/views.py` to `knowledge/tests.py`, `Source`, `knowledge/admin.py`, `django_conf`, `ConceptRelationship`, `Evidence`, `FlashcardAPITests`, `EmbeddingService`, `ClaimVerificationService`, `verification/tests.py`, `ClaimVerificationServiceTests`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `Evidence` connect `Evidence` to `knowledge/tests.py`, `Source`, `knowledge/admin.py`, `ConceptRelationship`, `django_db`, `EmbeddingService`, `ClaimVerificationService`, `knowledge/views.py`, `verification/tests.py`, `rag_explanation.py`, `ClaimVerificationServiceTests`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `ExternalIngestionPipeline`) actually correct?**
  _`Evidence` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Concept` (e.g. with `UnmappedConceptReviewAdmin` and `Command`) actually correct?**
  _`Concept` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ExtractedClaim` (e.g. with `ExternalIngestionPipeline` and `ExtractedClaimSerializer`) actually correct?**
  _`ExtractedClaim` has 13 INFERRED edges - model-reasoned connections that need verification._