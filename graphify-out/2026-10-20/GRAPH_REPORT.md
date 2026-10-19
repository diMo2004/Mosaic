# Graph Report - Mosaic  (2026-10-19)

## Corpus Check
- 203 files · ~105,416 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 7, .example 2, .css 1)

## Summary
- 1279 nodes · 2421 edges · 113 communities (67 shown, 46 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 254 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6c12b3d3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Note
- learning/views.py
- users/views.py
- learning.ts
- knowledge/admin.py
- Neon
- expo
- django_conf
- env
- HybridOCRProvider
- flashcard.ts
- django_apps
- App Status
- MOSAIC Architecture
- compilerOptions
- Managed Better Auth: implement login
- Concept
- PlaceholderOCRProvider
- Docker Compose Configuration
- Lakebase Postgres Branching
- CSE Technology & Concept Knowledge Graph
- Current State
- AuthTests
- rest_framework
- mobile/package.json
- Function Triggers
- AGENTS.md
- copilot-instructions.md
- AGENTS.md
- claim_verification.py
- Evidence
- ingest_external.py
- django_db
- d_mosaic_backend_learning_services_py
- client.ts
- RootNavigator.tsx
- FlashcardAPITests
- Flashcard
- Source
- Postgres Egress Optimizer
- Neon AI Gateway
- Neon Functions
- Neon Object Storage
- Sentry (errors, logs, and traces)
- CLAUDE.md
- Lakebase Postgres
- ExtractedClaim
- Semantic Vector Search
- Mastra agents with Mastra Studio observability
- Shipping native binaries with a Function
- Production hardening for Neon Functions
- Server-sent events (SSE) on Neon Functions
- hybrid-search.md
- neon-functions/SKILL.md
- Managing Lakebase Search with Drizzle
- KnowledgeExplorerScreen.tsx
- package.json
- learning/tests.py
- AI SDK agents on Neon Functions
- KnowledgeAPIPermissionTests
- Full-Text Search with BM25 Ranking
- Setup Flow
- Troubleshooting and Neon-Specific Performance
- WebSocket Servers
- dependencies
- Logs: CLI, Loki, and SDK pagination
- sdk.md
- learning/serializers.py
- MCP servers on Neon Functions
- UserProgress
- IngestionItem
- ClaimExtractionService
- verification/tests.py
- Claimable Neon
- django_contrib
- rag_explanation.py
- react
- os
- FlashcardSerializer
- KnowledgeModelTests
- NotePermissionTests
- neon/references/function-triggers.md
- celery.py
- 0007_canonicalclaim_claim_text_trgm_idx.py
- MasteryBadge
- 0002_alter_flashcard_options_and_more.py
- nativewind-env.d.ts

## God Nodes (most connected - your core abstractions)
1. `Source` - 41 edges
2. `Evidence` - 36 edges
3. `IngestionItem` - 31 edges
4. `Concept` - 30 edges
5. `ExtractedClaim` - 29 edges
6. `FlashcardAPITests` - 28 edges
7. `ClaimVerificationService` - 26 edges
8. `CanonicalClaim` - 24 edges
9. `react` - 24 edges
10. `SourceDocument` - 23 edges

## Surprising Connections (you probably didn't know these)
- `5. Pass the creds via `neon.ts` (third-party env)` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/mastra-studio.md → backend/config/settings.py
- `Option 1 — OAuth via the Better Auth MCP plugin (best for third-party clients)` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/mcp.md → backend/config/settings.py
- `Standalone executables` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/native-binaries.md → backend/config/settings.py
- `2. Provide the DSN as a deploy-time secret` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/sentry.md → backend/config/settings.py
- `Other Node integrations` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/sentry.md → backend/config/settings.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Knowledge Ingestion Pipeline** — backend_notes, backend_verification, backend_knowledge, backend_learning [EXTRACTED 1.00]
- **MVP Technology Stack** — docker_compose, github_actions_ci, backend_users [EXTRACTED 1.00]

## Communities (113 total, 46 thin omitted)

### Community 0 - "Note"
Cohesion: 0.17
Nodes (8): Meta, Note, Meta, NoteDetailSerializer, NoteUploadSerializer, NoteDetailView, NoteListView, NoteUploadView

### Community 1 - "learning/views.py"
Cohesion: 0.16
Nodes (14): FlashcardFeedbackSerializer, ConceptMasteryStatusView, FlashcardFeedbackView, FlashcardUnderstoodView, GroundedExplanationView, APIView, SaveFlashCardView, UserProgressSummaryView (+6 more)

### Community 2 - "users/views.py"
Cohesion: 0.08
Nodes (26): URL configuration for config project. The `urlpatterns` list routes URLs to…, CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes., CompleteProfileSerializer, GoogleAuthSerializer, Meta, RegisterSerializer (+18 more)

### Community 3 - "learning.ts"
Cohesion: 0.20
Nodes (18): createPlaylist(), getFlashcardDetail(), getFlashcards(), getPlaylists(), getProgressSummary(), getUserBadges(), markFlashcardUnderstood(), recordFlashcardView() (+10 more)

### Community 4 - "knowledge/admin.py"
Cohesion: 0.18
Nodes (13): action, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, register (+5 more)

### Community 5 - "Neon"
Cohesion: 0.05
Nodes (36): Auth, 1. Install the Neon CLI, 2. Install the Neon MCP Server, 3. Install Neon Agent Skills, 4. Link Your Project and Get Started, Architecture: How to Use Neon, Backend Primitives, Bootstrap a New Project (+28 more)

### Community 6 - "expo"
Cohesion: 0.06
Nodes (34): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, permissions, predictiveBackGestureEnabled (+26 more)

### Community 7 - "django_conf"
Cohesion: 0.10
Nodes (14): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+6 more)

### Community 8 - "env"
Cohesion: 0.15
Nodes (11): env(), Trusted app server, Application instrumentation, Built-in branch logs, Functions as an Agent Backend (Next.js and Similar Frameworks), Integrations and Observability, Neon Infrastructure as Code (`neon.ts`), Type-safe env vars with parseEnv (+3 more)

### Community 9 - "HybridOCRProvider"
Cohesion: 0.12
Nodes (13): OCRProvider, ABC, get_azure_client(), get_gemini_model(), HybridOCRProvider, Attempts OCR & visual analysis via Gemini-1.5-Flash. Falls back to Azure…, Dispatches to Text Parser, Document Parser, or Multimodal Image Parser and…, Extracts the absolute filesystem path from FieldFile or string. (+5 more)

### Community 10 - "flashcard.ts"
Cohesion: 0.12
Nodes (26): CardRendererProps, CardShell(), CardShellProps, formatCardType(), getDifficultyStyle(), getTypeBadgeStyle(), { height: WINDOW_HEIGHT }, styles (+18 more)

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

### Community 15 - "Managed Better Auth: implement login"
Cohesion: 0.08
Nodes (23): Auth emails, Cross-subdomain vs bearer JWT, Data API identity, Environment, Managed Better Auth: implement login, Next.js, Organization invitations, Packages (+15 more)

### Community 16 - "Concept"
Cohesion: 0.15
Nodes (11): Command, BaseCommand, Concept, ConceptRelationship, Questionnaire, MasteryService, atomic, Returns the next unpassed tier (1 to 5), or 6 if all 5 are passed. (+3 more)

### Community 19 - "Lakebase Postgres Branching"
Cohesion: 0.08
Nodes (25): Beta Support Guidance (Mandatory), Branch Type Decision, Branching in CI/CD, CLI usage, Console and API usage, Create a Normal Branch (Preferred for Real-Data Migration Testing), Create a Schema-Only Branch (Beta, Sensitive Data), Example 1: Migration testing with realistic data (+17 more)

### Community 36 - "AuthTests"
Cohesion: 0.16
Nodes (5): AuthTests, GoogleAuthTests, HealthCheckTests, APITestCase, patch

### Community 37 - "rest_framework"
Cohesion: 0.16
Nodes (12): UserProfile, create_user_profile(), django_contrib_auth_models, django_core_files_uploadedfile, django_db_models_signals, django_dispatch, django_test, profile (+4 more)

### Community 38 - "mobile/package.json"
Cohesion: 0.07
Nodes (27): App(), styles, mobile_global, { getDefaultConfig }, { withNativeWind }, devDependencies, @types/react, typescript (+19 more)

### Community 39 - "Function Triggers"
Cohesion: 0.15
Nodes (13): CLI, Delivery payload, Fields, Function Triggers, Inheritance, Local `neon dev`, Logs, MCP backup (+5 more)

### Community 50 - "claim_verification.py"
Cohesion: 0.27
Nodes (8): django_core_cache, google, google_genai, json, logging, networkx, pickle, re

### Community 51 - "Evidence"
Cohesion: 0.15
Nodes (11): build_embedding_text(), Command, BaseCommand, Evidence, EmbeddingService, EmbeddingServiceError, RuntimeError, Raised when an embedding cannot be generated. (+3 more)

### Community 52 - "ingest_external.py"
Cohesion: 0.13
Nodes (16): ArxivAdapter, Fetches academic computer science preprints from arXiv., GitHubAdapter, Fetches README and doc markdown from GitHub repositories., OfficialDocumentationAdapter, Fetches community discussion strictly for evidence attribution after legal…, RedditAdapter, Fetches high-quality answers from Stack Overflow or CSE Stack Exchange. (+8 more)

### Community 53 - "django_db"
Cohesion: 0.14
Nodes (14): Migration, Migration, enqueue_note_processing(), Migration, Migration, Meta, NoteProcessingJob, NoteProcessingService (+6 more)

### Community 55 - "client.ts"
Cohesion: 0.18
Nodes (13): completeProfile(), getProfile(), login(), register(), apiClient, BASE_URL, configuredApiUrl, CustomAxiosRequestConfig (+5 more)

### Community 56 - "RootNavigator.tsx"
Cohesion: 0.16
Nodes (15): getExplanation(), getMasteryStatus(), startQuestionnaire(), submitQuestionnaire(), getExtractedClaims(), getNotes(), getNoteStatus(), verifyClaim() (+7 more)

### Community 57 - "FlashcardAPITests"
Cohesion: 0.08
Nodes (9): Command, BaseCommand, Command, BaseCommand, FlashcardGenerationService, Generate flashcards from a given canonical claim., Return a meaningful recall pair when model generation is unavailable., FlashcardAPITests (+1 more)

### Community 58 - "Flashcard"
Cohesion: 0.20
Nodes (11): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin, Flashcard (+3 more)

### Community 59 - "Source"
Cohesion: 0.18
Nodes (11): First-party programming-language documentation adapter. The registry is…, Determines if content from this source can be fed to external LLMs, Determines if derived excerpts/flashcards can be shared publicly., Source, SourceDocument, base64, dataclasses, decimal (+3 more)

### Community 60 - "Postgres Egress Optimizer"
Cohesion: 0.12
Nodes (16): Application-side aggregation, Check if pg_stat_statements is available, Diagnostic queries, Further Reading, Handle empty stats, High-frequency queries on static data, Interpret the results, JOIN duplication (+8 more)

### Community 61 - "Neon AI Gateway"
Cohesion: 0.12
Nodes (15): Availability, Build Agents with Mastra (Recommended), Build Agents with the Vercel AI SDK (Recommended), Enabling the gateway: plan and model-catalog gating, Environment Variables, Further Reading, List Available Models at Runtime (`/v1/models`), Model Identifiers (+7 more)

### Community 62 - "Neon Functions"
Cohesion: 0.12
Nodes (16): Architecture: Where Functions Fit, Availability, Connecting to Postgres, Develop Locally and Deploy, Function Triggers, Further Reading, MCP Servers, Native binaries and custom builds (+8 more)

### Community 63 - "Neon Object Storage"
Cohesion: 0.12
Nodes (15): Architecture: Where Object Storage Fits, Availability, Built-in Branch Logs, CLI Bucket and Object Commands, Environment Variables, Further Reading, Neon Documentation, Neon Infrastructure as Code (`neon.ts`) (+7 more)

### Community 64 - "Sentry (errors, logs, and traces)"
Cohesion: 0.14
Nodes (13): main(), Django's command-line utility for administrative tasks., Run administrative tasks., 1. Initialize before anything else, 2. Provide the DSN as a deploy-time secret, 3. Create the request span and catch route errors, 4. Errors are for failures; logs are for the story, 5. Trace the agent itself (+5 more)

### Community 66 - "Lakebase Postgres"
Cohesion: 0.15
Nodes (13): Autoscaling, Branching, Connection Pooling, Gotchas, Instant Restore, IP Allow Lists, Lakebase Postgres, Lakebase Search (+5 more)

### Community 67 - "ExtractedClaim"
Cohesion: 0.07
Nodes (30): CanonicalClaim, ExtractedClaim, CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer (+22 more)

### Community 68 - "Semantic Vector Search"
Cohesion: 0.22
Nodes (9): Build the Index, Contents, Create the Extension, Prepare Embeddings, Query, Semantic Vector Search, Tune Search, Tune the Index (+1 more)

### Community 69 - "Mastra agents with Mastra Studio observability"
Cohesion: 0.25
Nodes (8): 1. Define the agent against the Neon AI Gateway, 2. Wire observability to Mastra Studio, 3. Structured output through the gateway, 4. Create the Mastra project + token with the CLI, 5. Pass the creds via `neon.ts` (third-party env), 6. Verify, Further reading, Mastra agents with Mastra Studio observability

### Community 70 - "Shipping native binaries with a Function"
Cohesion: 0.25
Nodes (7): `bundler: "none"`: ship a prebuilt directory, Custom `bundler`: return the file map, `externalPackages`: npm packages with a Node addon, Shipping native binaries with a Function, Size limits, Standalone executables, The runtime a binary lands on

### Community 71 - "Production hardening for Neon Functions"
Cohesion: 0.25
Nodes (8): Choose the caller shape, Function Triggers only, Limit authenticated application work, Native URL, Preserve existing clients, Production hardening for Neon Functions, Public consumers through a Worker, Reject these

### Community 72 - "Server-sent events (SSE) on Neon Functions"
Cohesion: 0.25
Nodes (7): Caveats, Client, Minimal SSE endpoint (no framework), Push to every client, across isolates, Server-sent events (SSE) on Neon Functions, Wire format (just text), With Hono

### Community 73 - "hybrid-search.md"
Cohesion: 0.43
Nodes (3): Adapt the Hybrid Search, Hybrid Search, RRF Example

### Community 75 - "Managing Lakebase Search with Drizzle"
Cohesion: 0.29
Nodes (7): BM25 Index, Config, Extensions, Managing Lakebase Search with Drizzle, Query, Schema, Tune Per Query

### Community 76 - "KnowledgeExplorerScreen.tsx"
Cohesion: 0.57
Nodes (4): getCanonicalClaims(), getEvidenceList(), getSources(), KnowledgeExplorerScreen()

### Community 77 - "package.json"
Cohesion: 0.29
Nodes (5): dependencies, @neon/config, @neon/env, @neon/config, @neon/env

### Community 78 - "learning/tests.py"
Cohesion: 0.07
Nodes (21): Any, EvidenceRetrievalError, EvidenceRetrievalService, RuntimeError, Raised when semantic evidence retrieval cannot be completed., RuntimeError, RAGExplanationService, RAGExplanationServiceError (+13 more)

### Community 79 - "AI SDK agents on Neon Functions"
Cohesion: 0.29
Nodes (7): 1. Declare the gateway and the function, 2. The handler: stream a tool-calling agent, 3. Generate images and persist them, 4. Call it directly from the client (don't proxy the stream), 5. Run and deploy, AI SDK agents on Neon Functions, Further reading

### Community 81 - "Full-Text Search with BM25 Ranking"
Cohesion: 0.33
Nodes (6): Full-Text Search with BM25 Ranking, Prepare and Index Text, Query and Interpret Scores, Set Parameters at Build Time or Per Query, Set the Candidate Limit, Use Prefilter Selectively

### Community 82 - "Setup Flow"
Cohesion: 0.33
Nodes (6): 1. Select the organization and project, 2. Get the connection string, 3. Pick the connection method and driver, 4. Set up the schema, Setup Flow, When to use pooled vs direct connections

### Community 83 - "Troubleshooting and Neon-Specific Performance"
Cohesion: 0.33
Nodes (6): Choose CLI or MCP, Inspect Neon Cache Behavior Per Query, Interpret Results Safely, Performance Workflow, Pick the Diagnostic, Troubleshooting and Neon-Specific Performance

### Community 84 - "WebSocket Servers"
Cohesion: 0.50
Nodes (4): Client must reconnect, Heartbeat (keep the socket alive), Keeping clients in sync across isolates (do not skip this), WebSocket Servers

### Community 85 - "dependencies"
Cohesion: 0.07
Nodes (29): dependencies, axios, expo, expo-dev-client, expo-document-picker, expo-secure-store, expo-status-bar, lucide-react-native (+21 more)

### Community 88 - "learning/serializers.py"
Cohesion: 0.16
Nodes (10): Playlist, QuestionnaireQuestion, Meta, PlaylistDetailSerializer, PlaylistSerializer, QuestionnaireQuestionClientSerializer, QuestionnaireQuestionReviewSerializer, UserProgressSerializer (+2 more)

### Community 89 - "MCP servers on Neon Functions"
Cohesion: 0.33
Nodes (6): Authenticating the server, MCP servers on Neon Functions, Option 1 — OAuth via the Better Auth MCP plugin (best for third-party clients), Option 2 — API key or session JWT via self-hosted Better Auth (simplest), Testing, The server

### Community 90 - "UserProgress"
Cohesion: 0.15
Nodes (10): FlashcardFeedEvent, Durable feed delivery history used to avoid immediate repetition., UserProgress, active_flashcards(), FlashcardDetailView, FlashcardFeedView, FlashcardViewedView, Record a card impression from the paged feed. (+2 more)

### Community 91 - "IngestionItem"
Cohesion: 0.21
Nodes (11): IngestionItem, Fetch content given an identifier (URL, repo, article title, etc.)., LicenseChecker, LicensePolicyError, RuntimeError, Raised when an external source fails licensing or AI-use policies., ExternalIngestionPipeline, atomic (+3 more)

### Community 93 - "verification/tests.py"
Cohesion: 0.27
Nodes (6): NoteProcessJobIntegrationTests, override_settings, patch, test_embedding_task_skips_existing_embedding(), test_embedding_task_stores_vector(), test_placeholder_evidence_queues_embedding_after_commit()

### Community 94 - "Claimable Neon"
Cohesion: 0.29
Nodes (6): Claim, Claimable Neon, If neon claim is missing, Path, With REST, With the CLI

### Community 96 - "django_contrib"
Cohesion: 0.25
Nodes (5): NoteAdmin, register, NoteProcessingJobAdmin, register, django_contrib

### Community 98 - "rag_explanation.py"
Cohesion: 0.38
Nodes (4): Migration, pgvector_django, pgvector_django_vector, typing

### Community 99 - "react"
Cohesion: 0.18
Nodes (15): searchFlashcardsByTopic(), uploadNote(), CardRenderer(), mobile_src_components_cards_index_cardrenderer, destinations, ProfileMenu(), ScreenHeader(), FeedScreen() (+7 more)

### Community 100 - "os"
Cohesion: 0.25
Nodes (5): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, django_core_asgi, django_core_wsgi, os

### Community 102 - "KnowledgeModelTests"
Cohesion: 0.22
Nodes (4): Meta, UnmappedConceptReview, KnowledgeModelTests, TestCase

### Community 107 - "0007_canonicalclaim_claim_text_trgm_idx.py"
Cohesion: 0.50
Nodes (3): Migration, django_contrib_postgres_indexes, django_contrib_postgres_operations

### Community 108 - "MasteryBadge"
Cohesion: 0.60
Nodes (3): MasteryBadge, MasteryBadgeSerializer, UserMasteryBadgesView

## Knowledge Gaps
- **360 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+355 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 620 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `env()` connect `env` to `Sentry (errors, logs, and traces)`, `Mastra agents with Mastra Studio observability`, `Shipping native binaries with a Function`, `neon-functions/SKILL.md`, `MCP servers on Neon Functions`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `Neon Functions` connect `Neon Functions` to `Sentry (errors, logs, and traces)`, `env`, `neon-functions/SKILL.md`, `WebSocket Servers`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `Source` connect `Source` to `ExtractedClaim`, `knowledge/admin.py`, `KnowledgeModelTests`, `learning/tests.py`, `KnowledgeAPIPermissionTests`, `Evidence`, `ingest_external.py`, `django_db`, `FlashcardAPITests`, `IngestionItem`, `verification/tests.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `ExternalIngestionPipeline`) actually correct?**
  _`Evidence` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `IngestionItem` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`IngestionItem` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Concept` (e.g. with `UnmappedConceptReviewAdmin` and `Command`) actually correct?**
  _`Concept` has 14 INFERRED edges - model-reasoned connections that need verification._