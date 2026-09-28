# Graph Report - Mosaic  (2026-09-28)

## Corpus Check
- 118 files · ~47,367 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 2)

## Summary
- 619 nodes · 1168 edges · 49 communities (21 shown, 28 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 132 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `18751c71`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ExtractedClaim
- learning/views.py
- users/views.py
- RootNavigator.tsx
- knowledge/admin.py
- package.json
- expo
- django_conf
- rag_explanation.py
- HybridOCRProvider
- IsProfileComplete
- django_apps
- App Status
- MOSAIC Architecture
- compilerOptions
- FlashcardAPITests
- knowledge/models.py
- PlaceholderOCRProvider
- Docker Compose Configuration
- CSE Technology & Concept Knowledge Graph
- Current State
- GoogleAuthTests
- RAGExplanationService
- ClaimExtractionService
- NotePermissionTests
- settings.py
- manage.py
- 0006_evidence_embedding.py
- wsgi.py
- copilot-instructions.md
- AGENTS.md

## God Nodes (most connected - your core abstractions)
1. `ExtractedClaim` - 23 edges
2. `Source` - 22 edges
3. `ClaimVerificationService` - 21 edges
4. `Evidence` - 20 edges
5. `FlashcardAPITests` - 20 edges
6. `CanonicalClaim` - 19 edges
7. `IsProfileComplete` - 19 edges
8. `Concept` - 18 edges
9. `Note` - 18 edges
10. `NoteProcessingService` - 17 edges

## Surprising Connections (you probably didn't know these)
- `Mosaic CI/CD Workflow` --semantically_similar_to--> `Docker Compose Configuration`  [INFERRED] [semantically similar]
  .github/workflows/ci-cd.yml → docker-compose.yml
- `EvidenceInline` --uses--> `Evidence`  [INFERRED]
  backend/knowledge/admin.py → backend/knowledge/models.py
- `MOSAIC Project Report & Technical Architecture` --references--> `MOSAIC Architecture`  [EXTRACTED]
  README.md → docs/architecture.md
- `KnowledgeModelTests` --uses--> `Source`  [INFERRED]
  backend/knowledge/tests.py → backend/knowledge/models.py
- `FlashcardAPITests` --uses--> `Source`  [INFERRED]
  backend/learning/tests.py → backend/knowledge/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Knowledge Ingestion Pipeline** — backend_notes, backend_verification, backend_knowledge, backend_learning [EXTRACTED 1.00]
- **MVP Technology Stack** — docker_compose, github_actions_ci, backend_users [EXTRACTED 1.00]

## Communities (49 total, 28 thin omitted)

### Community 0 - "ExtractedClaim"
Cohesion: 0.07
Nodes (28): Migration, ExtractedClaim, Migration, NoteAdmin, register, Meta, Note, Migration (+20 more)

### Community 1 - "learning/views.py"
Cohesion: 0.08
Nodes (30): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin, Flashcard (+22 more)

### Community 2 - "users/views.py"
Cohesion: 0.09
Nodes (25): URL configuration for config project. The `urlpatterns` list routes URLs to…, UserProfile, CompleteProfileSerializer, GoogleAuthSerializer, Meta, RegisterSerializer, create_user_profile(), CompleteProfileView (+17 more)

### Community 3 - "RootNavigator.tsx"
Cohesion: 0.09
Nodes (36): completeProfile(), login(), register(), apiClient, BASE_URL, configuredApiUrl, CustomAxiosRequestConfig, createPlaylist() (+28 more)

### Community 4 - "knowledge/admin.py"
Cohesion: 0.07
Nodes (30): action, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, register (+22 more)

### Community 5 - "package.json"
Cohesion: 0.05
Nodes (43): App(), styles, dependencies, axios, expo, expo-dev-client, expo-document-picker, expo-secure-store (+35 more)

### Community 6 - "expo"
Cohesion: 0.06
Nodes (34): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, permissions, predictiveBackGestureEnabled (+26 more)

### Community 7 - "django_conf"
Cohesion: 0.12
Nodes (12): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+4 more)

### Community 8 - "rag_explanation.py"
Cohesion: 0.25
Nodes (6): ASGI config for config project. It exposes the ASGI callable as a module-level…, django_core_asgi, google, google_genai, json, os

### Community 9 - "HybridOCRProvider"
Cohesion: 0.12
Nodes (13): ABC, OCRProvider, get_azure_client(), get_gemini_model(), HybridOCRProvider, Attempts OCR & visual analysis via Gemini-1.5-Flash. Falls back to Azure…, Dispatches to Text Parser, Document Parser, or Multimodal Image Parser and…, Extracts the absolute filesystem path from FieldFile or string. (+5 more)

### Community 10 - "IsProfileComplete"
Cohesion: 0.13
Nodes (14): CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes., Meta, NoteDetailSerializer, NoteUploadSerializer, NoteDetailView, NoteListView (+6 more)

### Community 11 - "django_apps"
Cohesion: 0.12
Nodes (11): KnowledgeConfig, AppConfig, LearningConfig, AppConfig, NotesConfig, AppConfig, AppConfig, UsersConfig (+3 more)

### Community 12 - "App Status"
Cohesion: 0.10
Nodes (19): App Status, Audience And Product Split, Current Work, External ingestion, Future Work (unchanged intent, updated order), Knowledge — models and admin in place, Learning — category 7 done, MOSAIC Roadmap (+11 more)

### Community 13 - "MOSAIC Architecture"
Cohesion: 0.32
Nodes (8): Knowledge App, Learning App, Notes App, Users App, Verification App, MOSAIC Architecture, Architecture Decisions, MOSAIC Project Report & Technical Architecture

### Community 14 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, moduleResolution, paths, strict, extends, expo/tsconfig.base

### Community 15 - "FlashcardAPITests"
Cohesion: 0.15
Nodes (4): FlashcardGenerationService, Generate flashcards from a given canonical claim., FlashcardAPITests, APITestCase

### Community 16 - "knowledge/models.py"
Cohesion: 0.08
Nodes (29): CanonicalClaim, Evidence, Determines if content from this source can be fed to external LLMs, Determines if derived excerpts/flashcards can be shared publicly., Source, SourceDocument, CanonicalClaimSerializer, EvidenceSerializer (+21 more)

### Community 36 - "GoogleAuthTests"
Cohesion: 0.22
Nodes (4): AuthTests, GoogleAuthTests, APITestCase, patch

### Community 40 - "settings.py"
Cohesion: 0.40
Nodes (3): dj_database_url, dotenv, pathlib

### Community 41 - "manage.py"
Cohesion: 0.40
Nodes (4): main(), Django's command-line utility for administrative tasks., Run administrative tasks., sys

### Community 42 - "0006_evidence_embedding.py"
Cohesion: 0.50
Nodes (3): Migration, pgvector_django, pgvector_django_vector

## Knowledge Gaps
- **110 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+105 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 273 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HybridOCRProvider` connect `HybridOCRProvider` to `ExtractedClaim`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `Source` connect `knowledge/models.py` to `ExtractedClaim`, `knowledge/admin.py`, `FlashcardAPITests`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `Note` connect `ExtractedClaim` to `knowledge/models.py`, `IsProfileComplete`, `NotePermissionTests`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `ExtractedClaim` (e.g. with `ExtractedClaimSerializer` and `KnowledgeModelTests`) actually correct?**
  _`ExtractedClaim` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Source` (e.g. with `SourceSerializer` and `KnowledgeAPIPermissionTests`) actually correct?**
  _`Source` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `ClaimVerificationService` (e.g. with `CanonicalClaim` and `Evidence`) actually correct?**
  _`ClaimVerificationService` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `EvidenceSerializer`) actually correct?**
  _`Evidence` has 8 INFERRED edges - model-reasoned connections that need verification._