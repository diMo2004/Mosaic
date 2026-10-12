# Graph Report - Mosaic  (2026-09-28)

## Corpus Check
- 122 files · ~49,693 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 2)

## Summary
- 691 nodes · 1378 edges · 55 communities (24 shown, 31 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 168 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `18751c71`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- verification/tests.py
- learning/views.py
- users/views.py
- RootNavigator.tsx
- Concept
- dependencies
- expo
- django_db
- os
- HybridOCRProvider
- django_conf
- django_apps
- App Status
- MOSAIC Architecture
- compilerOptions
- ClaimVerificationService
- knowledge/views.py
- PlaceholderOCRProvider
- Docker Compose Configuration
- knowledge/admin.py
- CSE Technology & Concept Knowledge Graph
- Current State
- GoogleAuthTests
- learning/tests.py
- EmbeddingServiceError
- ClaimVerificationServiceTests
- knowledge/tests.py
- EmbeddingService
- 0006_evidence_embedding.py
- knowledge/tasks.py
- copilot-instructions.md
- AGENTS.md
- KnowledgeAPIPermissionTests
- KnowledgeModelTests
- verification/admin.py
- .is_ai_usable
- .can_redistribute
- d_mosaic_backend_learning_services_py

## God Nodes (most connected - your core abstractions)
1. `Evidence` - 34 edges
2. `ExtractedClaim` - 26 edges
3. `Source` - 25 edges
4. `CanonicalClaim` - 23 edges
5. `ClaimVerificationService` - 22 edges
6. `Concept` - 21 edges
7. `RAGExplanationService` - 20 edges
8. `FlashcardAPITests` - 20 edges
9. `SourceDocument` - 19 edges
10. `IsProfileComplete` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Mosaic CI/CD Workflow` --semantically_similar_to--> `Docker Compose Configuration`  [INFERRED] [semantically similar]
  .github/workflows/ci-cd.yml → docker-compose.yml
- `EvidenceInline` --uses--> `Evidence`  [INFERRED]
  backend/knowledge/admin.py → backend/knowledge/models.py
- `MOSAIC Project Report & Technical Architecture` --references--> `MOSAIC Architecture`  [EXTRACTED]
  README.md → docs/architecture.md
- `UnmappedConceptReviewAdmin` --uses--> `Concept`  [INFERRED]
  backend/knowledge/admin.py → backend/knowledge/models.py
- `UnmappedConceptReviewAdmin` --uses--> `ConceptRelationship`  [INFERRED]
  backend/knowledge/admin.py → backend/knowledge/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Knowledge Ingestion Pipeline** — backend_notes, backend_verification, backend_knowledge, backend_learning [EXTRACTED 1.00]
- **MVP Technology Stack** — docker_compose, github_actions_ci, backend_users [EXTRACTED 1.00]

## Communities (55 total, 31 thin omitted)

### Community 0 - "verification/tests.py"
Cohesion: 0.25
Nodes (8): ExtractedClaim, Source, SourceDocument, Meta, NoteProcessingJob, NoteProcessingService, atomic, django_utils

### Community 1 - "learning/views.py"
Cohesion: 0.07
Nodes (32): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin, Flashcard (+24 more)

### Community 2 - "users/views.py"
Cohesion: 0.09
Nodes (24): UserProfile, CompleteProfileSerializer, GoogleAuthSerializer, Meta, RegisterSerializer, create_user_profile(), CompleteProfileView, GoogleAuthView (+16 more)

### Community 3 - "RootNavigator.tsx"
Cohesion: 0.06
Nodes (55): App(), styles, devDependencies, @types/react, typescript, main, name, private (+47 more)

### Community 4 - "Concept"
Cohesion: 0.16
Nodes (11): Command, BaseCommand, Concept, ConceptRelationship, Meta, UnmappedConceptReview, get_cached_nx_graph(), Builds and caches the NetworkX in-memory graph from PostgreSQL. (+3 more)

### Community 5 - "dependencies"
Cohesion: 0.08
Nodes (24): dependencies, axios, expo, expo-dev-client, expo-document-picker, expo-secure-store, expo-status-bar, react (+16 more)

### Community 6 - "expo"
Cohesion: 0.06
Nodes (34): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, permissions, predictiveBackGestureEnabled (+26 more)

### Community 7 - "django_db"
Cohesion: 0.09
Nodes (16): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+8 more)

### Community 8 - "os"
Cohesion: 0.07
Nodes (16): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, main(), Django's command-line utility for administrative tasks., Run administrative tasks., ClaimExtractionService, get_extractor_model(), dj_database_url (+8 more)

### Community 9 - "HybridOCRProvider"
Cohesion: 0.12
Nodes (13): ABC, OCRProvider, get_azure_client(), get_gemini_model(), HybridOCRProvider, Attempts OCR & visual analysis via Gemini-1.5-Flash. Falls back to Azure…, Dispatches to Text Parser, Document Parser, or Multimodal Image Parser and…, Extracts the absolute filesystem path from FieldFile or string. (+5 more)

### Community 10 - "django_conf"
Cohesion: 0.07
Nodes (22): URL configuration for config project. The `urlpatterns` list routes URLs to…, NoteAdmin, register, Meta, Note, CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes. (+14 more)

### Community 11 - "django_apps"
Cohesion: 0.12
Nodes (11): KnowledgeConfig, AppConfig, LearningConfig, AppConfig, NotesConfig, AppConfig, AppConfig, UsersConfig (+3 more)

### Community 12 - "App Status"
Cohesion: 0.11
Nodes (18): App Status, Audience And Product Split, Current Work, External ingestion, Future Work (updated after Category 9), Knowledge — models and admin in place, Learning — category 7 done, MOSAIC Roadmap (+10 more)

### Community 13 - "MOSAIC Architecture"
Cohesion: 0.32
Nodes (8): Knowledge App, Learning App, Notes App, Users App, Verification App, MOSAIC Architecture, Architecture Decisions, MOSAIC Project Report & Technical Architecture

### Community 14 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, moduleResolution, paths, strict, extends, expo/tsconfig.base

### Community 15 - "ClaimVerificationService"
Cohesion: 0.09
Nodes (9): FlashcardGenerationService, Generate flashcards from a given canonical claim., FlashcardAPITests, ClaimVerificationService, atomic, ConceptAssignmentService, Finds direct keywor matches in text against concept names., Retrieves a focused 1-hop sub-graph around anchor nodes. Returns a list of… (+1 more)

### Community 16 - "knowledge/views.py"
Cohesion: 0.19
Nodes (14): CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer, CanonicalClaimViewSet, EvidenceViewSet (+6 more)

### Community 19 - "knowledge/admin.py"
Cohesion: 0.19
Nodes (12): action, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, register (+4 more)

### Community 36 - "GoogleAuthTests"
Cohesion: 0.22
Nodes (4): AuthTests, GoogleAuthTests, APITestCase, patch

### Community 37 - "learning/tests.py"
Cohesion: 0.07
Nodes (25): Any, CanonicalClaim, Evidence, EvidenceRetrievalError, EvidenceRetrievalService, RuntimeError, Raised when semantic evidence retrieval cannot be completed., RuntimeError (+17 more)

### Community 38 - "EmbeddingServiceError"
Cohesion: 0.18
Nodes (8): build_embedding_text(), Command, BaseCommand, EmbeddingServiceError, RuntimeError, Raised when an embedding cannot be generated., django_core_management_base, google

### Community 39 - "ClaimVerificationServiceTests"
Cohesion: 0.19
Nodes (8): ClaimVerificationServiceTests, NoteProcessJobIntegrationTests, patch, TestCase, test_embedding_task_skips_existing_embedding(), test_embedding_task_stores_vector(), test_placeholder_evidence_queues_embedding_after_commit(), override_settings

### Community 40 - "knowledge/tests.py"
Cohesion: 0.36
Nodes (6): decimal, django_contrib_auth_models, django_core_files_uploadedfile, django_test, rest_framework_test, unittest_mock

### Community 43 - "knowledge/tasks.py"
Cohesion: 0.33
Nodes (4): embed_evidence_task(), EvidenceRetrievalService, logging, shared_task

## Knowledge Gaps
- **109 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 288 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Source` connect `verification/tests.py` to `Concept`, `learning/tests.py`, `ClaimVerificationServiceTests`, `knowledge/tests.py`, `knowledge/tasks.py`, `ClaimVerificationService`, `knowledge/views.py`, `KnowledgeAPIPermissionTests`, `KnowledgeModelTests`, `knowledge/admin.py`, `.is_ai_usable`, `.can_redistribute`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Evidence` connect `learning/tests.py` to `verification/tests.py`, `Concept`, `EmbeddingServiceError`, `ClaimVerificationServiceTests`, `knowledge/tests.py`, `knowledge/tasks.py`, `ClaimVerificationService`, `knowledge/views.py`, `KnowledgeModelTests`, `knowledge/admin.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `HybridOCRProvider` connect `HybridOCRProvider` to `verification/tests.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `build_embedding_text()`) actually correct?**
  _`Evidence` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `ExtractedClaim` (e.g. with `ExtractedClaimSerializer` and `KnowledgeModelTests`) actually correct?**
  _`ExtractedClaim` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Source` (e.g. with `SourceSerializer` and `KnowledgeAPIPermissionTests`) actually correct?**
  _`Source` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `CanonicalClaim` (e.g. with `CanonicalClaimSerializer` and `CanonicalClaimViewSet`) actually correct?**
  _`CanonicalClaim` has 9 INFERRED edges - model-reasoned connections that need verification._