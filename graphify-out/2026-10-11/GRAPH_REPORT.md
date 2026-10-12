# Graph Report - Mosaic  (2026-10-04)

## Corpus Check
- 140 files · ~53,750 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 2)

## Summary
- 787 nodes · 1698 edges · 53 communities (24 shown, 29 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `be8e3fae`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- django_db
- learning/views.py
- knowledge/tests.py
- RootNavigator.tsx
- Concept
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
- ClaimVerificationService
- ExtractedClaim
- PlaceholderOCRProvider
- Docker Compose Configuration
- scripts
- CSE Technology & Concept Knowledge Graph
- Current State
- GoogleAuthTests
- learning/tests.py
- Evidence
- verification/tests.py
- AGENTS.md
- copilot-instructions.md
- AGENTS.md
- django_contrib
- Source
- d_mosaic_backend_learning_services_py

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
- `Mosaic CI/CD Workflow` --semantically_similar_to--> `Docker Compose Configuration`  [INFERRED] [semantically similar]
  .github/workflows/ci-cd.yml → docker-compose.yml
- `EvidenceInline` --uses--> `Evidence`  [INFERRED]
  backend/knowledge/admin.py → backend/knowledge/models.py
- `MOSAIC Project Report & Technical Architecture` --references--> `MOSAIC Architecture`  [EXTRACTED]
  README.md → docs/architecture.md
- `ExternalIngestionPipeline` --uses--> `Evidence`  [INFERRED]
  backend/knowledge/ingestion/pipeline.py → backend/knowledge/models.py
- `ExternalIngestionPipeline` --uses--> `ExtractedClaim`  [INFERRED]
  backend/knowledge/ingestion/pipeline.py → backend/knowledge/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Knowledge Ingestion Pipeline** — backend_notes, backend_verification, backend_knowledge, backend_learning [EXTRACTED 1.00]
- **MVP Technology Stack** — docker_compose, github_actions_ci, backend_users [EXTRACTED 1.00]

## Communities (53 total, 29 thin omitted)

### Community 0 - "django_db"
Cohesion: 0.11
Nodes (13): Migration, Migration, Migration, Command, BaseCommand, Migration, Meta, NoteProcessingJob (+5 more)

### Community 1 - "learning/views.py"
Cohesion: 0.06
Nodes (45): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin, Flashcard (+37 more)

### Community 2 - "knowledge/tests.py"
Cohesion: 0.05
Nodes (37): URL configuration for config project. The `urlpatterns` list routes URLs to…, KnowledgeAPIPermissionTests, APITestCase, NotePermissionTests, APITestCase, UserProfile, CompleteProfileSerializer, GoogleAuthSerializer (+29 more)

### Community 3 - "RootNavigator.tsx"
Cohesion: 0.06
Nodes (55): App(), styles, devDependencies, @types/react, typescript, main, name, private (+47 more)

### Community 4 - "Concept"
Cohesion: 0.06
Nodes (32): action, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, register (+24 more)

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
Cohesion: 0.08
Nodes (16): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, main(), Django's command-line utility for administrative tasks., Run administrative tasks., ClaimExtractionService, get_extractor_model(), dj_database_url (+8 more)

### Community 9 - "HybridOCRProvider"
Cohesion: 0.12
Nodes (13): OCRProvider, ABC, get_azure_client(), get_gemini_model(), HybridOCRProvider, Attempts OCR & visual analysis via Gemini-1.5-Flash. Falls back to Azure…, Dispatches to Text Parser, Document Parser, or Multimodal Image Parser and…, Extracts the absolute filesystem path from FieldFile or string. (+5 more)

### Community 10 - "notes/views.py"
Cohesion: 0.13
Nodes (14): NoteAdmin, register, Meta, Note, CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes., Meta (+6 more)

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

### Community 15 - "ClaimVerificationService"
Cohesion: 0.23
Nodes (4): ClaimVerificationService, atomic, EvidenceRetrievalService, ClaimVerificationServiceTests

### Community 16 - "ExtractedClaim"
Cohesion: 0.17
Nodes (15): ExtractedClaim, SourceDocument, CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer (+7 more)

### Community 19 - "scripts"
Cohesion: 0.20
Nodes (10): scripts, android, build:android:apk, build:preview, ios, lint, prebuild, start (+2 more)

### Community 36 - "GoogleAuthTests"
Cohesion: 0.22
Nodes (4): AuthTests, GoogleAuthTests, APITestCase, patch

### Community 37 - "learning/tests.py"
Cohesion: 0.07
Nodes (18): Any, CanonicalClaim, FlashcardGenerationService, Generate flashcards from a given canonical claim., RuntimeError, RAGExplanationService, RAGExplanationServiceError, Raised when RAG explanation generation fails. (+10 more)

### Community 38 - "Evidence"
Cohesion: 0.08
Nodes (23): build_embedding_text(), Command, BaseCommand, Migration, Evidence, EmbeddingService, EmbeddingServiceError, RuntimeError (+15 more)

### Community 39 - "verification/tests.py"
Cohesion: 0.22
Nodes (9): NoteProcessingService, atomic, NoteProcessJobIntegrationTests, patch, TestCase, test_embedding_task_skips_existing_embedding(), test_embedding_task_stores_vector(), test_placeholder_evidence_queues_embedding_after_commit() (+1 more)

### Community 51 - "django_contrib"
Cohesion: 0.40
Nodes (3): NoteProcessingJobAdmin, register, django_contrib

### Community 52 - "Source"
Cohesion: 0.09
Nodes (33): ArxivAdapter, Fetches academic computer science preprints from arXiv., GitHubAdapter, Fetches README and doc markdown from GitHub repositories., Fetches community discussion strictly for evidence attribution after legal…, RedditAdapter, Fetches high-quality answers from Stack Overflow or CSE Stack Exchange., StackExchangeAdapter (+25 more)

## Knowledge Gaps
- **111 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+106 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 323 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Source` connect `Source` to `django_db`, `knowledge/tests.py`, `Concept`, `learning/tests.py`, `Evidence`, `verification/tests.py`, `ClaimVerificationService`, `ExtractedClaim`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `Concept` connect `Concept` to `django_db`, `learning/views.py`, `knowledge/tests.py`, `learning/tests.py`, `Evidence`, `verification/tests.py`, `ClaimVerificationService`, `Source`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `Evidence` connect `Evidence` to `django_db`, `knowledge/tests.py`, `Concept`, `learning/tests.py`, `verification/tests.py`, `ClaimVerificationService`, `ExtractedClaim`, `Source`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `ExternalIngestionPipeline`) actually correct?**
  _`Evidence` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Concept` (e.g. with `UnmappedConceptReviewAdmin` and `Command`) actually correct?**
  _`Concept` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ExtractedClaim` (e.g. with `ExternalIngestionPipeline` and `ExtractedClaimSerializer`) actually correct?**
  _`ExtractedClaim` has 13 INFERRED edges - model-reasoned connections that need verification._