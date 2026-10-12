# Graph Report - Mosaic  (2026-10-11)

## Corpus Check
- 142 files · ~54,154 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 2)

## Summary
- 796 nodes · 1715 edges · 66 communities (33 shown, 33 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `be8e3fae`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- verification/tests.py
- learning/views.py
- users/views.py
- RootNavigator.tsx
- knowledge/admin.py
- dependencies
- expo
- django_conf
- os
- HybridOCRProvider
- notes/views.py
- django_apps
- App Status
- MOSAIC Architecture
- compilerOptions
- ExtractedClaim
- knowledge/views.py
- PlaceholderOCRProvider
- Docker Compose Configuration
- scripts
- CSE Technology & Concept Knowledge Graph
- Current State
- GoogleAuthTests
- learning/tests.py
- EmbeddingService
- NoteProcessJobIntegrationTests
- AGENTS.md
- copilot-instructions.md
- AGENTS.md
- NoteProcessingService
- config/urls.py
- Source
- rag_explanation.py
- d_mosaic_backend_learning_services_py
- UserProfile
- KnowledgeModelTests
- knowledge/tests.py
- ClaimExtractionService
- ConceptRelationship
- KnowledgeAPIPermissionTests
- NotePermissionTests
- concept_assignment.py
- verification/views.py
- manage.py
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `Source` - 39 edges
2. `Evidence` - 36 edges
3. `ExtractedClaim` - 29 edges
4. `Concept` - 29 edges
5. `IngestionItem` - 28 edges
6. `ClaimVerificationService` - 25 edges
7. `CanonicalClaim` - 24 edges
8. `SourceDocument` - 23 edges
9. `MasteryService` - 21 edges
10. `FlashcardAPITests` - 21 edges

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

## Communities (66 total, 33 thin omitted)

### Community 0 - "verification/tests.py"
Cohesion: 0.19
Nodes (7): Migration, SourceDocument, Migration, Migration, Migration, django_db, django_utils

### Community 1 - "learning/views.py"
Cohesion: 0.05
Nodes (49): Concept, FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin (+41 more)

### Community 2 - "users/views.py"
Cohesion: 0.22
Nodes (11): CompleteProfileSerializer, GoogleAuthSerializer, CompleteProfileView, GoogleAuthView, HealthCheckView, jwt_response_for_user(), APIView, RegisterView (+3 more)

### Community 3 - "RootNavigator.tsx"
Cohesion: 0.06
Nodes (55): App(), styles, devDependencies, @types/react, typescript, main, name, private (+47 more)

### Community 4 - "knowledge/admin.py"
Cohesion: 0.19
Nodes (12): action, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, register (+4 more)

### Community 5 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, axios, expo, expo-dev-client, expo-document-picker, expo-secure-store, expo-status-bar, react (+6 more)

### Community 6 - "expo"
Cohesion: 0.06
Nodes (34): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, permissions, predictiveBackGestureEnabled (+26 more)

### Community 7 - "django_conf"
Cohesion: 0.11
Nodes (13): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+5 more)

### Community 8 - "os"
Cohesion: 0.17
Nodes (8): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, dj_database_url, django_core_asgi, django_core_wsgi, dotenv, os, pathlib

### Community 9 - "HybridOCRProvider"
Cohesion: 0.12
Nodes (13): OCRProvider, ABC, get_azure_client(), get_gemini_model(), HybridOCRProvider, Attempts OCR & visual analysis via Gemini-1.5-Flash. Falls back to Azure…, Dispatches to Text Parser, Document Parser, or Multimodal Image Parser and…, Extracts the absolute filesystem path from FieldFile or string. (+5 more)

### Community 10 - "notes/views.py"
Cohesion: 0.15
Nodes (12): Meta, Note, CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes., Meta, NoteDetailSerializer, NoteUploadSerializer (+4 more)

### Community 11 - "django_apps"
Cohesion: 0.12
Nodes (11): KnowledgeConfig, AppConfig, LearningConfig, AppConfig, NotesConfig, AppConfig, AppConfig, UsersConfig (+3 more)

### Community 12 - "App Status"
Cohesion: 0.11
Nodes (18): App Status, Audience And Product Split, Current Work, External ingestion — completed (Category 10), Future Work (updated after Category 9), Knowledge — models and admin in place, Learning — category 7 done, MOSAIC Roadmap (+10 more)

### Community 13 - "MOSAIC Architecture"
Cohesion: 0.32
Nodes (8): Knowledge App, Learning App, Notes App, Users App, Verification App, MOSAIC Architecture, Architecture Decisions, MOSAIC Project Report & Technical Architecture

### Community 14 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, moduleResolution, paths, strict, extends, expo/tsconfig.base

### Community 15 - "ExtractedClaim"
Cohesion: 0.08
Nodes (13): ExtractedClaim, FlashcardGenerationService, Generate flashcards from a given canonical claim., FlashcardAPITests, ClaimVerificationService, atomic, ConceptAssignmentService, Finds direct keywor matches in text against concept names. (+5 more)

### Community 16 - "knowledge/views.py"
Cohesion: 0.20
Nodes (13): CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer, CanonicalClaimViewSet, EvidenceViewSet (+5 more)

### Community 19 - "scripts"
Cohesion: 0.20
Nodes (10): scripts, android, build:android:apk, build:preview, ios, lint, prebuild, start (+2 more)

### Community 36 - "GoogleAuthTests"
Cohesion: 0.22
Nodes (4): AuthTests, GoogleAuthTests, APITestCase, patch

### Community 37 - "learning/tests.py"
Cohesion: 0.08
Nodes (21): Any, CanonicalClaim, EvidenceRetrievalError, EvidenceRetrievalService, RuntimeError, Raised when semantic evidence retrieval cannot be completed., RuntimeError, RAGExplanationService (+13 more)

### Community 38 - "EmbeddingService"
Cohesion: 0.16
Nodes (9): build_embedding_text(), Command, BaseCommand, EmbeddingService, EmbeddingServiceError, RuntimeError, Raised when an embedding cannot be generated., EmbeddingServiceTests (+1 more)

### Community 39 - "NoteProcessJobIntegrationTests"
Cohesion: 0.22
Nodes (7): NoteProcessJobIntegrationTests, patch, TestCase, test_embedding_task_skips_existing_embedding(), test_embedding_task_stores_vector(), test_placeholder_evidence_queues_embedding_after_commit(), override_settings

### Community 50 - "NoteProcessingService"
Cohesion: 0.16
Nodes (9): Command, BaseCommand, Meta, NoteProcessingJob, NoteProcessingService, atomic, process_note_task(), shared_task (+1 more)

### Community 51 - "config/urls.py"
Cohesion: 0.17
Nodes (8): URL configuration for config project. The `urlpatterns` list routes URLs to…, NoteAdmin, register, NoteProcessingJobAdmin, register, django_conf_urls_static, django_contrib, rest_framework_simplejwt_views

### Community 52 - "Source"
Cohesion: 0.08
Nodes (38): ArxivAdapter, Fetches academic computer science preprints from arXiv., GitHubAdapter, Fetches README and doc markdown from GitHub repositories., Fetches community discussion strictly for evidence attribution after legal…, RedditAdapter, Fetches high-quality answers from Stack Overflow or CSE Stack Exchange., StackExchangeAdapter (+30 more)

### Community 53 - "rag_explanation.py"
Cohesion: 0.19
Nodes (8): Migration, google, google_genai, json, logging, pgvector_django, pgvector_django_vector, typing

### Community 55 - "UserProfile"
Cohesion: 0.20
Nodes (8): UserProfile, Meta, RegisterSerializer, create_user_profile(), django_db_models_signals, django_dispatch, profile, receiver

### Community 56 - "KnowledgeModelTests"
Cohesion: 0.22
Nodes (4): Meta, UnmappedConceptReview, KnowledgeModelTests, TestCase

### Community 57 - "knowledge/tests.py"
Cohesion: 0.42
Nodes (6): django_contrib_auth_models, django_core_files_uploadedfile, django_test, rest_framework, rest_framework_test, unittest_mock

### Community 59 - "ConceptRelationship"
Cohesion: 0.29
Nodes (5): Command, BaseCommand, ConceptRelationship, django_utils_text, re

### Community 62 - "concept_assignment.py"
Cohesion: 0.33
Nodes (4): get_cached_nx_graph(), django_core_cache, networkx, pickle

### Community 63 - "verification/views.py"
Cohesion: 0.33
Nodes (4): django_shortcuts, django_urls, rest_framework_response, rest_framework_views

### Community 64 - "manage.py"
Cohesion: 0.40
Nodes (4): main(), Django's command-line utility for administrative tasks., Run administrative tasks., sys

## Knowledge Gaps
- **112 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+107 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 328 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Source` connect `Source` to `verification/tests.py`, `knowledge/admin.py`, `learning/tests.py`, `ExtractedClaim`, `knowledge/views.py`, `NoteProcessingService`, `KnowledgeModelTests`, `knowledge/tests.py`, `KnowledgeAPIPermissionTests`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `Concept` connect `learning/views.py` to `verification/tests.py`, `knowledge/admin.py`, `learning/tests.py`, `NoteProcessJobIntegrationTests`, `ExtractedClaim`, `Source`, `KnowledgeModelTests`, `knowledge/tests.py`, `ConceptRelationship`, `concept_assignment.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `HybridOCRProvider` connect `HybridOCRProvider` to `verification/tests.py`, `NoteProcessingService`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `ExternalIngestionPipeline`) actually correct?**
  _`Evidence` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ExtractedClaim` (e.g. with `ExternalIngestionPipeline` and `ExtractedClaimSerializer`) actually correct?**
  _`ExtractedClaim` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `Concept` (e.g. with `UnmappedConceptReviewAdmin` and `Command`) actually correct?**
  _`Concept` has 13 INFERRED edges - model-reasoned connections that need verification._