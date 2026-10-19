# Graph Report - Mosaic  (2026-10-19)

## Corpus Check
- 194 files · ~103,719 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 7, .example 2)

## Summary
- 1235 nodes · 2322 edges · 108 communities (66 shown, 42 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 243 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6c12b3d3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- notes/views.py
- learning/views.py
- users/views.py
- learning.ts
- knowledge/admin.py
- Neon
- expo
- django_db
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
- UserProfile
- knowledge/views.py
- Function Triggers
- AGENTS.md
- copilot-instructions.md
- AGENTS.md
- django_conf
- Evidence
- Source
- verification/tests.py
- d_mosaic_backend_learning_services_py
- client.ts
- RootNavigator.tsx
- FlashcardAPITests
- Flashcard
- knowledge/models.py
- Postgres Egress Optimizer
- Neon AI Gateway
- Neon Functions
- Neon Object Storage
- Sentry (errors, logs, and traces)
- CLAUDE.md
- Lakebase Postgres
- ClaimVerificationService
- Semantic Vector Search
- Mastra agents with Mastra Studio observability
- Shipping native binaries with a Function
- Production hardening for Neon Functions
- Server-sent events (SSE) on Neon Functions
- hybrid-search.md
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
- mobile/package.json
- Logs: CLI, Loki, and SDK pagination
- sdk.md
- knowledge/tests.py
- MCP servers on Neon Functions
- CanViewOwnNotes
- GoogleAuthTests
- ClaimExtractionService
- manage.py
- Claimable Neon
- config/urls.py
- ProgressScreen.tsx
- FeedScreen.tsx
- os
- FlashcardSerializer
- KnowledgeModelTests
- ProfileAwareTokenObtainPairSerializer
- neon/references/function-triggers.md
- GoogleAuthView
- 0007_canonicalclaim_claim_text_trgm_idx.py

## God Nodes (most connected - your core abstractions)
1. `Source` - 39 edges
2. `Evidence` - 36 edges
3. `ExtractedClaim` - 29 edges
4. `Concept` - 29 edges
5. `IngestionItem` - 28 edges
6. `ClaimVerificationService` - 26 edges
7. `FlashcardAPITests` - 25 edges
8. `CanonicalClaim` - 24 edges
9. `SourceDocument` - 23 edges
10. `FlashcardGenerationService` - 23 edges

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

## Communities (108 total, 42 thin omitted)

### Community 0 - "notes/views.py"
Cohesion: 0.11
Nodes (13): NoteAdmin, register, Meta, Note, Meta, NoteDetailSerializer, NoteUploadSerializer, NotePermissionTests (+5 more)

### Community 1 - "learning/views.py"
Cohesion: 0.10
Nodes (21): FlashcardFeedbackSerializer, MasteryBadgeSerializer, PlaylistSerializer, active_flashcards(), FlashcardDetailView, FlashcardFeedbackView, FlashcardFeedView, FlashcardUnderstoodView (+13 more)

### Community 2 - "users/views.py"
Cohesion: 0.13
Nodes (14): CompleteProfileSerializer, CompleteProfileView, jwt_response_for_user(), RegisterView, APIView, VerifyClaimView, django_shortcuts, django_urls (+6 more)

### Community 3 - "learning.ts"
Cohesion: 0.24
Nodes (16): createPlaylist(), getFlashcards(), getMasteryStatus(), getPlaylists(), markFlashcardUnderstood(), recordFlashcardView(), saveFlashcard(), startQuestionnaire() (+8 more)

### Community 4 - "knowledge/admin.py"
Cohesion: 0.13
Nodes (16): action, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, register (+8 more)

### Community 5 - "Neon"
Cohesion: 0.05
Nodes (36): Auth, 1. Install the Neon CLI, 2. Install the Neon MCP Server, 3. Install Neon Agent Skills, 4. Link Your Project and Get Started, Architecture: How to Use Neon, Backend Primitives, Bootstrap a New Project (+28 more)

### Community 6 - "expo"
Cohesion: 0.06
Nodes (34): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, permissions, predictiveBackGestureEnabled (+26 more)

### Community 7 - "django_db"
Cohesion: 0.07
Nodes (19): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+11 more)

### Community 8 - "env"
Cohesion: 0.22
Nodes (8): env(), Trusted app server, Application instrumentation, Built-in branch logs, Functions as an Agent Backend (Next.js and Similar Frameworks), Integrations and Observability, Neon Infrastructure as Code (`neon.ts`), Type-safe env vars with parseEnv

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
Cohesion: 0.17
Nodes (11): Concept, Questionnaire, QuestionnaireQuestion, QuestionnaireQuestionClientSerializer, QuestionnaireQuestionReviewSerializer, MasteryService, atomic, Returns the next unpassed tier (1 to 5), or 6 if all 5 are passed. (+3 more)

### Community 19 - "Lakebase Postgres Branching"
Cohesion: 0.08
Nodes (25): Beta Support Guidance (Mandatory), Branch Type Decision, Branching in CI/CD, CLI usage, Console and API usage, Create a Normal Branch (Preferred for Real-Data Migration Testing), Create a Schema-Only Branch (Beta, Sensitive Data), Example 1: Migration testing with realistic data (+17 more)

### Community 36 - "AuthTests"
Cohesion: 0.25
Nodes (3): AuthTests, HealthCheckTests, APITestCase

### Community 37 - "UserProfile"
Cohesion: 0.20
Nodes (8): UserProfile, Meta, RegisterSerializer, create_user_profile(), django_db_models_signals, django_dispatch, profile, receiver

### Community 38 - "knowledge/views.py"
Cohesion: 0.20
Nodes (13): CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer, CanonicalClaimViewSet, EvidenceViewSet (+5 more)

### Community 39 - "Function Triggers"
Cohesion: 0.15
Nodes (13): CLI, Delivery payload, Fields, Function Triggers, Inheritance, Local `neon dev`, Logs, MCP backup (+5 more)

### Community 50 - "django_conf"
Cohesion: 0.17
Nodes (12): Command, BaseCommand, ConceptRelationship, django_conf, django_core_cache, google, google_genai, json (+4 more)

### Community 51 - "Evidence"
Cohesion: 0.15
Nodes (11): build_embedding_text(), Command, BaseCommand, Evidence, EmbeddingService, EmbeddingServiceError, RuntimeError, Raised when an embedding cannot be generated. (+3 more)

### Community 52 - "Source"
Cohesion: 0.09
Nodes (31): ArxivAdapter, Fetches academic computer science preprints from arXiv., GitHubAdapter, Fetches README and doc markdown from GitHub repositories., Fetches community discussion strictly for evidence attribution after legal…, RedditAdapter, Fetches high-quality answers from Stack Overflow or CSE Stack Exchange., StackExchangeAdapter (+23 more)

### Community 53 - "verification/tests.py"
Cohesion: 0.11
Nodes (17): NoteProcessingJobAdmin, register, Command, BaseCommand, Meta, NoteProcessingJob, NoteProcessingService, atomic (+9 more)

### Community 55 - "client.ts"
Cohesion: 0.18
Nodes (13): completeProfile(), getProfile(), login(), register(), apiClient, BASE_URL, configuredApiUrl, CustomAxiosRequestConfig (+5 more)

### Community 56 - "RootNavigator.tsx"
Cohesion: 0.16
Nodes (19): getExplanation(), getFlashcardDetail(), sendFeedback(), getExtractedClaims(), getNotes(), getNoteStatus(), uploadNote(), verifyClaim() (+11 more)

### Community 57 - "FlashcardAPITests"
Cohesion: 0.08
Nodes (9): Command, BaseCommand, Command, BaseCommand, FlashcardGenerationService, Generate flashcards from a given canonical claim., Return a meaningful recall pair when model generation is unavailable., FlashcardAPITests (+1 more)

### Community 58 - "Flashcard"
Cohesion: 0.14
Nodes (17): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin, Flashcard (+9 more)

### Community 59 - "knowledge/models.py"
Cohesion: 0.33
Nodes (6): ExternalIngestionPipeline, atomic, ExtractedClaim, SourceDocument, django_utils, logging

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
Cohesion: 0.13
Nodes (14): Architecture: Where Object Storage Fits, Availability, Built-in Branch Logs, CLI Bucket and Object Commands, Environment Variables, Further Reading, Neon Documentation, Neon Infrastructure as Code (`neon.ts`) (+6 more)

### Community 64 - "Sentry (errors, logs, and traces)"
Cohesion: 0.22
Nodes (9): 2. Provide the DSN as a deploy-time secret, 3. Create the request span and catch route errors, 4. Errors are for failures; logs are for the story, 5. Trace the agent itself, Environment variables, Other Node integrations, Sentry error monitoring on Neon Functions, Sentry (errors, logs, and traces) (+1 more)

### Community 66 - "Lakebase Postgres"
Cohesion: 0.15
Nodes (13): Autoscaling, Branching, Connection Pooling, Gotchas, Instant Restore, IP Allow Lists, Lakebase Postgres, Lakebase Search (+5 more)

### Community 67 - "ClaimVerificationService"
Cohesion: 0.12
Nodes (10): ClaimVerificationService, atomic, ConceptAssignmentService, get_cached_nx_graph(), Finds direct keywor matches in text against concept names., Retrieves a focused 1-hop sub-graph around anchor nodes. Returns a list of…, Assigns an official Concept from the sub-graph. If the text contains an…, EvidenceRetrievalService (+2 more)

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
Cohesion: 0.06
Nodes (27): Any, Migration, CanonicalClaim, EvidenceRetrievalError, EvidenceRetrievalService, RuntimeError, Raised when semantic evidence retrieval cannot be completed., RuntimeError (+19 more)

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

### Community 85 - "mobile/package.json"
Cohesion: 0.04
Nodes (45): App(), styles, dependencies, axios, expo, expo-dev-client, expo-document-picker, expo-secure-store (+37 more)

### Community 88 - "knowledge/tests.py"
Cohesion: 0.44
Nodes (6): django_contrib_auth_models, django_core_files_uploadedfile, django_test, rest_framework, rest_framework_test, unittest_mock

### Community 89 - "MCP servers on Neon Functions"
Cohesion: 0.33
Nodes (6): Authenticating the server, MCP servers on Neon Functions, Option 1 — OAuth via the Better Auth MCP plugin (best for third-party clients), Option 2 — API key or session JWT via self-hosted Better Auth (simplest), Testing, The server

### Community 90 - "CanViewOwnNotes"
Cohesion: 0.33
Nodes (4): CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes., rest_framework_permissions

### Community 93 - "manage.py"
Cohesion: 0.29
Nodes (6): main(), Django's command-line utility for administrative tasks., Run administrative tasks., 1. Initialize before anything else, Environment Variables, sys

### Community 94 - "Claimable Neon"
Cohesion: 0.29
Nodes (6): Claim, Claimable Neon, If neon claim is missing, Path, With REST, With the CLI

### Community 96 - "config/urls.py"
Cohesion: 0.33
Nodes (5): URL configuration for config project. The `urlpatterns` list routes URLs to…, ProfileAwareTokenObtainPairView, django_conf_urls_static, rest_framework_simplejwt_views, TokenObtainPairView

### Community 98 - "ProgressScreen.tsx"
Cohesion: 0.83
Nodes (3): getProgressSummary(), getUserBadges(), ProgressScreen()

### Community 99 - "FeedScreen.tsx"
Cohesion: 0.40
Nodes (4): CardRenderer(), mobile_src_components_cards_index_cardrenderer, FeedScreen(), styles

### Community 100 - "os"
Cohesion: 0.18
Nodes (8): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, dj_database_url, django_core_asgi, django_core_wsgi, dotenv, os, pathlib

### Community 101 - "FlashcardSerializer"
Cohesion: 0.36
Nodes (3): FlashcardSerializer, Meta, PlaylistDetailSerializer

### Community 106 - "GoogleAuthView"
Cohesion: 0.40
Nodes (4): GoogleAuthSerializer, GoogleAuthView, HealthCheckView, APIView

### Community 107 - "0007_canonicalclaim_claim_text_trgm_idx.py"
Cohesion: 0.50
Nodes (3): Migration, django_contrib_postgres_indexes, django_contrib_postgres_operations

## Knowledge Gaps
- **349 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+344 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 595 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `env()` connect `env` to `Sentry (errors, logs, and traces)`, `os`, `Mastra agents with Mastra Studio observability`, `Shipping native binaries with a Function`, `MCP servers on Neon Functions`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `Neon Functions` connect `Neon Functions` to `env`, `neon-functions/SKILL.md`, `WebSocket Servers`, `manage.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Source` connect `Source` to `ClaimVerificationService`, `knowledge/admin.py`, `knowledge/views.py`, `KnowledgeModelTests`, `learning/tests.py`, `KnowledgeAPIPermissionTests`, `Evidence`, `verification/tests.py`, `knowledge/tests.py`, `FlashcardAPITests`, `knowledge/models.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `ExternalIngestionPipeline`) actually correct?**
  _`Evidence` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ExtractedClaim` (e.g. with `ExternalIngestionPipeline` and `ExtractedClaimSerializer`) actually correct?**
  _`ExtractedClaim` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `Concept` (e.g. with `UnmappedConceptReviewAdmin` and `Command`) actually correct?**
  _`Concept` has 13 INFERRED edges - model-reasoned connections that need verification._