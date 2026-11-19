# Graph Report - Mosaic  (2026-11-14)

## Corpus Check
- 229 files · ~105,346 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 7, .example 2, .css 1)

## Summary
- 1838 nodes · 3786 edges · 153 communities (86 shown, 67 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 347 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eb661353`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- notes/views.py
- FlashcardFeedEvent
- react
- MasteryScreen.tsx
- knowledge/admin.py
- Neon
- expo
- django_db
- settings.py
- HybridOCRProvider
- flashcard.ts
- django_apps
- App Status
- MOSAIC Architecture
- compilerOptions
- Managed Better Auth: implement login
- MasteryService
- PlaceholderOCRProvider
- Docker Compose Configuration
- Lakebase Postgres Branching
- CSE Technology & Concept Knowledge Graph
- Current State
- AuthTests
- backend
- knowledge/models.py
- Function Triggers
- AGENTS.md
- copilot-instructions.md
- AGENTS.md
- mobile/package.json
- jobs.py
- knowledge/views.py
- scripts
- IngestionJobTests
- client.ts
- RootNavigator.tsx
- FlashcardGenerationService
- learning/models.py
- IngestionItem
- Postgres Egress Optimizer
- Neon AI Gateway
- Neon Functions
- Neon Object Storage
- Sentry (errors, logs, and traces)
- CLAUDE.md
- Lakebase Postgres
- ClaimExtractionService
- Semantic Vector Search
- Mastra agents with Mastra Studio observability
- Shipping native binaries with a Function
- Production hardening for Neon Functions
- Server-sent events (SSE) on Neon Functions
- hybrid-search.md
- users/views.py
- Managing Lakebase Search with Drizzle
- ingestion_status
- package.json
- RAGExplanationService
- AI SDK agents on Neon Functions
- learning/views.py
- Full-Text Search with BM25 Ranking
- Setup Flow
- Troubleshooting and Neon-Specific Performance
- provider_get
- dependencies
- Logs: CLI, Loki, and SDK pagination
- sdk.md
- Playlist
- App.tsx
- UserProfile
- wiki_item
- manage.py
- ExtractedClaim
- Claimable Neon
- FlashcardFeedback
- Source
- learning.ts
- FlashcardAPITests
- FlashcardSerializer
- ConceptAssignmentService
- generate_flashcard_for_claim_task
- neon/references/function-triggers.md
- accessible_flashcards
- official_docs.py
- PersonalFlashcardEnvironmentTests
- registry.py
- nativewind-env.d.ts
- Concept
- metro.config.js
- django_conf
- FlashcardGenerationIdempotencyTests
- FeedPaginationTests
- IngestionRunView
- AdapterDiscoveryTests
- DeferredVerificationTests
- NotePermissionTests
- neon-functions/SKILL.md
- KnowledgeAPIPermissionTests
- 0010_deduplicate_active_flashcards.py
- learning/models.py
- env
- expo-dev-client@~57.0.20
- CanViewOwnNotes
- PlaylistDetailView
- postgres
- test
- with
- react-native-safe-area-context@~5.7.0
- react-native-screens@~4.26.0
- docker-build
- steps
- SearchScreen.tsx
- deploy
- on
- 0007_canonicalclaim_claim_text_trgm_idx.py
- WebSocket Servers
- ProfileAwareTokenObtainPairSerializer
- expo@~57.0.29
- parse-env.md
- expo-document-picker

## God Nodes (most connected - your core abstractions)
1. `Source` - 46 edges
2. `IngestionItem` - 40 edges
3. `Evidence` - 39 edges
4. `ExtractedClaim` - 37 edges
5. `Concept` - 36 edges
6. `provider_get()` - 36 edges
7. `FlashcardGenerationService` - 35 edges
8. `ClaimVerificationService` - 35 edges
9. `CanonicalClaim` - 32 edges
10. `SourceDocument` - 31 edges

## Surprising Connections (you probably didn't know these)
- `How enforcement works` --references--> `SourceDocument`  [INFERRED]
  docs/source_policy.md → backend/knowledge/models.py
- `Feed API contract` --references--> `useFlashcardFeed()`  [INFERRED]
  docs/ingestion.md → mobile/src/hooks/useFlashcardFeed.ts
- `Idempotency and incremental updates` --references--> `Flashcard`  [INFERRED]
  docs/ingestion.md → backend/learning/models.py
- `Idempotency and incremental updates` --references--> `FlashcardGenerationService`  [INFERRED]
  docs/ingestion.md → backend/learning/services/flashcard_service.py
- `Configuration` --references--> `ingestion_status()`  [INFERRED]
  docs/ingestion.md → backend/knowledge/ingestion/status.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Knowledge Ingestion Pipeline** — backend_notes, backend_verification, backend_knowledge, backend_learning [EXTRACTED 1.00]
- **MVP Technology Stack** — docker_compose, github_actions_ci, backend_users [EXTRACTED 1.00]

## Communities (153 total, 67 thin omitted)

### Community 0 - "notes/views.py"
Cohesion: 0.08
Nodes (18): NoteAdmin, Note, Meta, NoteDetailSerializer, Meta, NoteUploadSerializer, Meta, enqueue_note_processing() (+10 more)

### Community 1 - "FlashcardFeedEvent"
Cohesion: 0.13
Nodes (8): FlashcardFeedEvent, Meta, active_flashcards(), feed_eligible_flashcards(), FlashcardFeedView, personal_feed_eligible_flashcards(), PersonalFlashcardFeedView, user_feed_eligible_flashcards()

### Community 2 - "react"
Cohesion: 0.15
Nodes (15): uploadNote(), destinations, ProfileMenu(), ScreenHeader(), BadgeProps, BadgeVariant, ButtonProps, ButtonSize (+7 more)

### Community 3 - "MasteryScreen.tsx"
Cohesion: 0.19
Nodes (14): getFlashcardDetail(), getMasteryStatus(), getPlaylistDetail(), sendFeedback(), startQuestionnaire(), submitQuestionnaire(), Badge(), Button() (+6 more)

### Community 4 - "knowledge/admin.py"
Cohesion: 0.16
Nodes (11): CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, IngestionJobAdmin, SourceAdmin (+3 more)

### Community 5 - "Neon"
Cohesion: 0.05
Nodes (36): Auth, 1. Install the Neon CLI, 2. Install the Neon MCP Server, 3. Install Neon Agent Skills, 4. Link Your Project and Get Started, Architecture: How to Use Neon, Backend Primitives, Bootstrap a New Project (+28 more)

### Community 6 - "expo"
Cohesion: 0.06
Nodes (34): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, permissions, predictiveBackGestureEnabled (+26 more)

### Community 7 - "django_db"
Cohesion: 0.05
Nodes (24): Migration, Migration, Migration, Migration, Migration, Migration, Migration, embed_evidence_task() (+16 more)

### Community 8 - "settings.py"
Cohesion: 0.38
Nodes (3): env(), env_bool(), env_list()

### Community 9 - "HybridOCRProvider"
Cohesion: 0.12
Nodes (4): OCRProvider, get_azure_client(), get_gemini_model(), HybridOCRProvider

### Community 10 - "flashcard.ts"
Cohesion: 0.12
Nodes (28): CardRenderer(), CardRendererProps, CardShell(), CardShellProps, formatCardType(), getDifficultyStyle(), getTypeBadgeStyle(), { height: WINDOW_HEIGHT } (+20 more)

### Community 11 - "django_apps"
Cohesion: 0.12
Nodes (5): KnowledgeConfig, LearningConfig, NotesConfig, UsersConfig, VerificationConfig

### Community 12 - "App Status"
Cohesion: 0.11
Nodes (18): App Status, Audience And Product Split, Current Work, External ingestion — completed (Category 10), Future Work (updated after Category 9), Knowledge — models and admin in place, Learning — category 7 done, MOSAIC Roadmap (+10 more)

### Community 13 - "MOSAIC Architecture"
Cohesion: 0.32
Nodes (3): MOSAIC Architecture, Architecture Decisions, MOSAIC Project Report & Technical Architecture

### Community 14 - "compilerOptions"
Cohesion: 0.29
Nodes (6): compilerOptions, moduleResolution, paths, strict, extends, expo/tsconfig.base

### Community 15 - "Managed Better Auth: implement login"
Cohesion: 0.08
Nodes (23): Auth emails, Cross-subdomain vs bearer JWT, Data API identity, Environment, Managed Better Auth: implement login, Next.js, Organization invitations, Packages (+15 more)

### Community 16 - "MasteryService"
Cohesion: 0.24
Nodes (3): Questionnaire, Meta, MasteryService

### Community 19 - "Lakebase Postgres Branching"
Cohesion: 0.08
Nodes (25): Beta Support Guidance (Mandatory), Branch Type Decision, Branching in CI/CD, CLI usage, Console and API usage, Create a Normal Branch (Preferred for Real-Data Migration Testing), Create a Schema-Only Branch (Beta, Sensitive Data), Example 1: Migration testing with realistic data (+17 more)

### Community 36 - "AuthTests"
Cohesion: 0.16
Nodes (3): AuthTests, GoogleAuthTests, HealthCheckTests

### Community 37 - "backend"
Cohesion: 0.05
Nodes (46): build, command, container_name, depends_on, environment, ports, restart, volumes (+38 more)

### Community 38 - "knowledge/models.py"
Cohesion: 0.08
Nodes (11): build_embedding_text(), Command, Migration, Evidence, Meta, EmbeddingService, EmbeddingServiceError, EvidenceRetrievalError (+3 more)

### Community 39 - "Function Triggers"
Cohesion: 0.15
Nodes (13): CLI, Delivery payload, Fields, Function Triggers, Inheritance, Local `neon dev`, Logs, MCP backup (+5 more)

### Community 50 - "mobile/package.json"
Cohesion: 0.21
Nodes (11): devDependencies, babel-preset-expo@~57.0.15, @types/react@~19.2.2, typescript@~6.0.3, main, name, private, version (+3 more)

### Community 51 - "jobs.py"
Cohesion: 0.07
Nodes (22): backoff_seconds(), DiscoveryService, DiscoveryStats, enqueue_jobs(), IngestionJobService, JobRetry, per_adapter_limit(), recover_stale_jobs() (+14 more)

### Community 52 - "knowledge/views.py"
Cohesion: 0.12
Nodes (16): CanonicalClaimSerializer, Meta, EvidenceSerializer, Meta, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, Meta (+8 more)

### Community 53 - "scripts"
Cohesion: 0.18
Nodes (11): scripts, android, build:android:apk, build:preview, ios, lint, prebuild, start (+3 more)

### Community 54 - "IngestionJobTests"
Cohesion: 0.17
Nodes (5): RateLimitedError, TransientProviderError, FakeAdapter, FakePipeline, IngestionJobTests

### Community 55 - "client.ts"
Cohesion: 0.35
Nodes (7): completeProfile(), getProfile(), login(), register(), CompleteProfileScreen(), getAuthErrorMessage(), LoginScreen()

### Community 56 - "RootNavigator.tsx"
Cohesion: 0.13
Nodes (17): apiClient, BASE_URL, configuredApiUrl, CustomAxiosRequestConfig, getCanonicalClaims(), getEvidenceList(), getSources(), getExtractedClaims() (+9 more)

### Community 57 - "FlashcardGenerationService"
Cohesion: 0.17
Nodes (3): Command, Command, FlashcardGenerationService

### Community 58 - "learning/models.py"
Cohesion: 0.27
Nodes (8): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, UserProgressAdmin, PlaylistItem, Meta

### Community 59 - "IngestionItem"
Cohesion: 0.13
Nodes (9): ProviderError, is_policy_enabled(), LicensePolicyError, policy_for_adapter(), resolve_policy(), _reviewed_sources(), SourcePolicy, InsufficientContentError (+1 more)

### Community 60 - "Postgres Egress Optimizer"
Cohesion: 0.12
Nodes (16): Application-side aggregation, Check if pg_stat_statements is available, Diagnostic queries, Further Reading, Handle empty stats, High-frequency queries on static data, Interpret the results, JOIN duplication (+8 more)

### Community 61 - "Neon AI Gateway"
Cohesion: 0.12
Nodes (15): Availability, Build Agents with Mastra (Recommended), Build Agents with the Vercel AI SDK (Recommended), Enabling the gateway: plan and model-catalog gating, Environment Variables, Further Reading, List Available Models at Runtime (`/v1/models`), Model Identifiers (+7 more)

### Community 62 - "Neon Functions"
Cohesion: 0.09
Nodes (22): Application instrumentation, Architecture: Where Functions Fit, Availability, Built-in branch logs, Connecting to Postgres, Develop Locally and Deploy, Environment Variables, Function Triggers (+14 more)

### Community 63 - "Neon Object Storage"
Cohesion: 0.12
Nodes (15): Architecture: Where Object Storage Fits, Availability, Built-in Branch Logs, CLI Bucket and Object Commands, Environment Variables, Further Reading, Neon Documentation, Neon Infrastructure as Code (`neon.ts`) (+7 more)

### Community 64 - "Sentry (errors, logs, and traces)"
Cohesion: 0.20
Nodes (10): 1. Initialize before anything else, 2. Provide the DSN as a deploy-time secret, 3. Create the request span and catch route errors, 4. Errors are for failures; logs are for the story, 5. Trace the agent itself, Environment variables, Other Node integrations, Sentry error monitoring on Neon Functions (+2 more)

### Community 66 - "Lakebase Postgres"
Cohesion: 0.15
Nodes (13): Autoscaling, Branching, Connection Pooling, Gotchas, Instant Restore, IP Allow Lists, Lakebase Postgres, Lakebase Search (+5 more)

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
Cohesion: 0.22
Nodes (9): Choose the caller shape, Function Triggers only, Limit authenticated application work, Native URL, Preserve existing clients, Production hardening for Neon Functions, Public consumers through a Worker, Reject these (+1 more)

### Community 72 - "Server-sent events (SSE) on Neon Functions"
Cohesion: 0.25
Nodes (7): Caveats, Client, Minimal SSE endpoint (no framework), Push to every client, across isolates, Server-sent events (SSE) on Neon Functions, Wire format (just text), With Hono

### Community 73 - "hybrid-search.md"
Cohesion: 0.43
Nodes (3): Adapt the Hybrid Search, Hybrid Search, RRF Example

### Community 74 - "users/views.py"
Cohesion: 0.13
Nodes (8): CompleteProfileSerializer, GoogleAuthSerializer, CompleteProfileView, GoogleAuthView, HealthCheckView, jwt_response_for_user(), ProfileAwareTokenObtainPairView, RegisterView

### Community 75 - "Managing Lakebase Search with Drizzle"
Cohesion: 0.29
Nodes (7): BM25 Index, Config, Extensions, Managing Lakebase Search with Drizzle, Query, Schema, Tune Per Query

### Community 76 - "ingestion_status"
Cohesion: 0.10
Nodes (16): ingestion_status(), Command, Adapters (`knowledge/ingestion/adapters/`, registry in `registry.py`), Configuration, Continuous external ingestion and the flashcard feed, Feed API contract, Manual, bounded runs, Observability (+8 more)

### Community 77 - "package.json"
Cohesion: 0.31
Nodes (7): dependencies, expo@^58.0.25, @neon/config@^1.8.6, @neon/env@^1.5.3, expo, @neon/config, @neon/env

### Community 78 - "RAGExplanationService"
Cohesion: 0.12
Nodes (7): RAGExplanationService, RAGExplanationServiceError, FakeEvidenceRetriever, FakeExplanationClient, FakeExplanationModels, FakeExplanationResponse, RAGExplanationServiceTests

### Community 79 - "AI SDK agents on Neon Functions"
Cohesion: 0.29
Nodes (7): 1. Declare the gateway and the function, 2. The handler: stream a tool-calling agent, 3. Generate images and persist them, 4. Call it directly from the client (don't proxy the stream), 5. Run and deploy, AI SDK agents on Neon Functions, Further reading

### Community 80 - "learning/views.py"
Cohesion: 0.25
Nodes (11): ConceptMasteryStatusView, FlashcardFeedbackView, FlashcardUnderstoodView, FlashcardViewedView, GroundedExplanationView, SaveFlashCardView, StartQuestionnaireView, SubmitQuestionnaireView (+3 more)

### Community 81 - "Full-Text Search with BM25 Ranking"
Cohesion: 0.33
Nodes (6): Full-Text Search with BM25 Ranking, Prepare and Index Text, Query and Interpret Scores, Set Parameters at Build Time or Per Query, Set the Candidate Limit, Use Prefilter Selectively

### Community 82 - "Setup Flow"
Cohesion: 0.33
Nodes (6): 1. Select the organization and project, 2. Get the connection string, 3. Pick the connection method and driver, 4. Set up the schema, Setup Flow, When to use pooled vs direct connections

### Community 83 - "Troubleshooting and Neon-Specific Performance"
Cohesion: 0.33
Nodes (6): Choose CLI or MCP, Inspect Neon Cache Behavior Per Query, Interpret Results Safely, Performance Workflow, Pick the Diagnostic, Troubleshooting and Neon-Specific Performance

### Community 84 - "provider_get"
Cohesion: 0.12
Nodes (13): RedditAdapter, _cooldown_key(), _json_or_none(), _min_interval(), PermanentProviderError, provider_get(), _rate_key(), _retry_after_seconds() (+5 more)

### Community 85 - "dependencies"
Cohesion: 0.13
Nodes (15): dependencies, axios@^1.20.0, expo-secure-store@~57.0.4, react@19.2.3, react-native@0.86.3, react-native-svg@^15.16.0, @react-navigation/bottom-tabs@^7.18.18, @react-navigation/native-stack@^7.18.10 (+7 more)

### Community 88 - "Playlist"
Cohesion: 0.20
Nodes (5): Playlist, Meta, PlaylistSerializer, Meta, PlaylistListCreateView

### Community 89 - "App.tsx"
Cohesion: 0.24
Nodes (7): App(), styles, expo-status-bar@~57.0.1, @react-navigation/native@^7.3.18, RootNavigator(), expo-status-bar, @react-navigation/native

### Community 90 - "UserProfile"
Cohesion: 0.19
Nodes (4): UserProfile, RegisterSerializer, Meta, create_user_profile()

### Community 91 - "wiki_item"
Cohesion: 0.05
Nodes (20): LicenseChecker, PolicyDecision, best_supporting_passage(), claim_hash(), content_hash(), _content_tokens(), normalize_claim_text(), normalize_document_text() (+12 more)

### Community 93 - "ExtractedClaim"
Cohesion: 0.10
Nodes (10): ExtractedClaim, ClaimVerificationService, dispatch_flashcard_generation(), EvidenceRetrievalService, ClaimVerificationServiceTests, NoteProcessJobIntegrationTests, test_embedding_task_skips_existing_embedding(), test_embedding_task_stores_vector() (+2 more)

### Community 94 - "Claimable Neon"
Cohesion: 0.29
Nodes (6): Claim, Claimable Neon, If neon claim is missing, Path, With REST, With the CLI

### Community 96 - "FlashcardFeedback"
Cohesion: 0.33
Nodes (4): FlashcardFeedback, Meta, FlashcardFeedbackSerializer, Meta

### Community 98 - "Source"
Cohesion: 0.12
Nodes (8): CanonicalClaim, Meta, Source, Meta, SourceDocument, Meta, GroundedExplanationAPITests, Idempotency and incremental updates

### Community 99 - "learning.ts"
Cohesion: 0.18
Nodes (19): createPlaylist(), getExplanation(), getFlashcards(), getPlaylists(), getProgressSummary(), getUserBadges(), markFlashcardUnderstood(), recordFlashcardView() (+11 more)

### Community 101 - "FlashcardSerializer"
Cohesion: 0.20
Nodes (4): FlashcardSerializer, Meta, PlaylistDetailSerializer, Meta

### Community 103 - "generate_flashcard_for_claim_task"
Cohesion: 0.19
Nodes (5): backfill_missing_flashcards_task(), generate_flashcard_for_claim_task(), _max_attempts(), FlashcardTaskTests, make_claim()

### Community 106 - "accessible_flashcards"
Cohesion: 0.25
Nodes (3): accessible_flashcards(), FlashcardDetailView, record_flashcard_view()

### Community 107 - "official_docs.py"
Cohesion: 0.13
Nodes (7): DocSource, extract_main_text(), OfficialDocumentationAdapter, parse_sphinx_inventory(), _plain_text(), AccessDisallowedError, policy_key_for()

### Community 109 - "registry.py"
Cohesion: 0.12
Nodes (12): ArxivAdapter, _base_id(), GitHubAdapter, license_for_post(), site_domain(), StackExchangeAdapter, WikimediaAdapter, BaseExternalAdapter (+4 more)

### Community 113 - "Concept"
Cohesion: 0.11
Nodes (11): Command, Concept, Meta, ConceptRelationship, Meta, UnmappedConceptReview, Meta, KnowledgeModelTests (+3 more)

### Community 114 - "metro.config.js"
Cohesion: 0.33
Nodes (4): { getDefaultConfig }, { withNativeWind }, nativewind@^4.2.7, nativewind

### Community 115 - "django_conf"
Cohesion: 0.18
Nodes (3): pending_counts(), Flashcard, Meta

### Community 119 - "AdapterDiscoveryTests"
Cohesion: 0.20
Nodes (5): AdapterDiscoveryTests, route(), route(), route(), fake_response()

### Community 122 - "neon-functions/SKILL.md"
Cohesion: 0.21
Nodes (6): Authenticating the server, MCP servers on Neon Functions, Option 1 — OAuth via the Better Auth MCP plugin (best for third-party clients), Option 2 — API key or session JWT via self-hosted Better Auth (simplest), Testing, The server

### Community 125 - "learning/models.py"
Cohesion: 0.13
Nodes (13): MasteryBadge, Meta, QuestionnaireQuestion, UserProgress, Meta, MasteryBadgeSerializer, Meta, QuestionnaireQuestionClientSerializer (+5 more)

### Community 126 - "env"
Cohesion: 0.14
Nodes (14): ALLOWED_HOSTS, CELERY_BROKER_URL, CELERY_RESULT_BACKEND, CORS_ALLOWED_ORIGINS, DATABASE_URL, DEBUG, GEMINI_API_KEY, GEMINI_CLAIM_MODEL (+6 more)

### Community 131 - "postgres"
Cohesion: 0.25
Nodes (8): POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, env, image, options, ports, postgres

### Community 132 - "test"
Cohesion: 0.25
Nodes (8): test, image, options, ports, redis, name, runs-on, services

### Community 133 - "with"
Cohesion: 0.25
Nodes (8): with, cache, cache-dependency-path, context, file, push, python-version, tags

### Community 136 - "docker-build"
Cohesion: 0.29
Nodes (6): name, needs, runs-on, jobs, docker-build, name

### Community 137 - "steps"
Cohesion: 0.47
Nodes (6): steps, steps, name, run, uses, steps

### Community 138 - "SearchScreen.tsx"
Cohesion: 0.24
Nodes (4): lucide-react-native@^1.59.0, searchFlashcardsByTopic(), SearchScreen(), lucide-react-native

### Community 140 - "deploy"
Cohesion: 0.40
Nodes (5): if, name, needs, runs-on, deploy

### Community 141 - "on"
Cohesion: 0.40
Nodes (5): on, pull_request, push, branches, branches

### Community 143 - "WebSocket Servers"
Cohesion: 0.50
Nodes (4): Client must reconnect, Heartbeat (keep the socket alive), Keeping clients in sync across isolates (do not skip this), WebSocket Servers

## Knowledge Gaps
- **7 isolated node(s):** `expo/tsconfig.base`, `Architecture Decisions`, `MOSAIC Project Report & Technical Architecture`, `Docker Compose Configuration`, `Mosaic CI/CD Workflow` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 809 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **67 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Feed API contract` connect `ingestion_status` to `learning.ts`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 23 INFERRED edges - model-reasoned connections that need verification._
- **What connects `expo/tsconfig.base`, `Architecture Decisions`, `MOSAIC Project Report & Technical Architecture` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `notes/views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07607843137254902 - nodes in this community are weakly interconnected._
- **Why does `useFlashcardFeed()` connect `learning.ts` to `react`, `ingestion_status`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `IngestionItem` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`IngestionItem` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Should `FlashcardFeedEvent` be split into smaller, more focused modules?**
  _Cohesion score 0.13157894736842105 - nodes in this community are weakly interconnected._