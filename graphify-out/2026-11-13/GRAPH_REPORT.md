# Graph Report - Mosaic  (2026-11-13)

## Corpus Check
- 229 files · ~105,262 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 7, .example 2, .css 1)

## Summary
- 1830 nodes · 3859 edges · 147 communities (89 shown, 58 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 427 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eb661353`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- notes/views.py
- learning/views.py
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
- EmbeddingService
- Function Triggers
- AGENTS.md
- copilot-instructions.md
- AGENTS.md
- mobile/package.json
- jobs.py
- SourceDocument
- scripts
- knowledge/models.py
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
- pipeline.py
- Semantic Vector Search
- Mastra agents with Mastra Studio observability
- Shipping native binaries with a Function
- Production hardening for Neon Functions
- Server-sent events (SSE) on Neon Functions
- hybrid-search.md
- users/views.py
- Managing Lakebase Search with Drizzle
- KnowledgeExplorerScreen.tsx
- package.json
- Evidence
- AI SDK agents on Neon Functions
- Source
- Full-Text Search with BM25 Ranking
- Setup Flow
- Troubleshooting and Neon-Specific Performance
- provider_get
- dependencies
- Logs: CLI, Loki, and SDK pagination
- sdk.md
- learning/urls.py
- App.tsx
- FlashcardFeedEvent
- IngestionJobTests
- manage.py
- verification/tests.py
- Claimable Neon
- IsProfileComplete
- SourceDocument
- learning.ts
- FlashcardAPITests
- FlashcardSerializer
- ConceptAssignmentService
- FlashcardGenerationIdempotencyTests
- neon/references/function-triggers.md
- ClaimVerificationService
- official_docs.py
- PermanentProviderError
- registry.py
- nativewind-env.d.ts
- ConceptRelationship
- metro.config.js
- tests_feed.py
- Evidence
- FeedPaginationTests
- OfficialDocumentationAdapter
- AdapterDiscoveryTests
- DeferredVerificationTests
- NotePermissionTests
- neon-functions/SKILL.md
- KnowledgeAPIPermissionTests
- 0010_deduplicate_active_flashcards.py
- learning/models.py
- env
- expo-dev-client@~57.0.20
- ExtractedClaim
- postgres
- test
- with
- react-native-safe-area-context@~5.7.0
- react-native-screens@~4.26.0
- docker-build
- steps
- react
- deploy
- on
- 0007_canonicalclaim_claim_text_trgm_idx.py
- WebSocket Servers
- 0006_evidence_embedding.py
- tailwindcss@^3.4.19
- parse-env.md

## God Nodes (most connected - your core abstractions)
1. `Source` - 48 edges
2. `Concept` - 44 edges
3. `Evidence` - 41 edges
4. `IngestionItem` - 40 edges
5. `ExtractedClaim` - 39 edges
6. `FlashcardGenerationService` - 37 edges
7. `ClaimVerificationService` - 36 edges
8. `CanonicalClaim` - 36 edges
9. `Flashcard` - 36 edges
10. `provider_get()` - 36 edges

## Surprising Connections (you probably didn't know these)
- `How enforcement works` --references--> `SourceDocument`  [INFERRED]
  docs/source_policy.md → backend/knowledge/models.py
- `Feed API contract` --references--> `useFlashcardFeed()`  [INFERRED]
  docs/ingestion.md → mobile/src/hooks/useFlashcardFeed.ts
- `Idempotency and incremental updates` --references--> `SourceDocument`  [INFERRED]
  docs/ingestion.md → backend/knowledge/models.py
- `Idempotency and incremental updates` --references--> `FlashcardGenerationService`  [INFERRED]
  docs/ingestion.md → backend/learning/services/flashcard_service.py
- `Idempotency and incremental updates` --references--> `Flashcard`  [INFERRED]
  docs/ingestion.md → backend/learning/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Knowledge Ingestion Pipeline** — backend_notes, backend_verification, backend_knowledge, backend_learning [EXTRACTED 1.00]
- **MVP Technology Stack** — docker_compose, github_actions_ci, backend_users [EXTRACTED 1.00]

## Communities (147 total, 58 thin omitted)

### Community 0 - "notes/views.py"
Cohesion: 0.13
Nodes (11): NoteAdmin, Note, Meta, NoteDetailSerializer, Meta, NoteUploadSerializer, Meta, enqueue_note_processing() (+3 more)

### Community 1 - "learning/views.py"
Cohesion: 0.15
Nodes (9): Flashcard, Meta, accessible_flashcards(), active_flashcards(), feed_eligible_flashcards(), FlashcardDetailView, personal_feed_eligible_flashcards(), PersonalFlashcardFeedView (+1 more)

### Community 2 - "react"
Cohesion: 0.17
Nodes (11): searchFlashcardsByTopic(), uploadNote(), destinations, ProfileMenu(), ScreenHeader(), FeedScreen(), styles, SearchScreen() (+3 more)

### Community 3 - "MasteryScreen.tsx"
Cohesion: 0.31
Nodes (13): getFlashcardDetail(), getMasteryStatus(), getPlaylistDetail(), sendFeedback(), startQuestionnaire(), submitQuestionnaire(), Badge(), Button() (+5 more)

### Community 4 - "knowledge/admin.py"
Cohesion: 0.14
Nodes (13): CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, IngestionJobAdmin, SourceAdmin (+5 more)

### Community 5 - "Neon"
Cohesion: 0.05
Nodes (36): Auth, 1. Install the Neon CLI, 2. Install the Neon MCP Server, 3. Install Neon Agent Skills, 4. Link Your Project and Get Started, Architecture: How to Use Neon, Backend Primitives, Bootstrap a New Project (+28 more)

### Community 6 - "expo"
Cohesion: 0.06
Nodes (34): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, permissions, predictiveBackGestureEnabled (+26 more)

### Community 7 - "django_db"
Cohesion: 0.05
Nodes (23): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+15 more)

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
Cohesion: 0.14
Nodes (11): TopicPlanner, Concept, Meta, QuestionnaireQuestionClientSerializer, Meta, QuestionnaireQuestionReviewSerializer, Meta, MasteryService (+3 more)

### Community 19 - "Lakebase Postgres Branching"
Cohesion: 0.08
Nodes (25): Beta Support Guidance (Mandatory), Branch Type Decision, Branching in CI/CD, CLI usage, Console and API usage, Create a Normal Branch (Preferred for Real-Data Migration Testing), Create a Schema-Only Branch (Beta, Sensitive Data), Example 1: Migration testing with realistic data (+17 more)

### Community 36 - "AuthTests"
Cohesion: 0.16
Nodes (3): AuthTests, GoogleAuthTests, HealthCheckTests

### Community 37 - "backend"
Cohesion: 0.05
Nodes (46): build, command, container_name, depends_on, environment, ports, restart, volumes (+38 more)

### Community 38 - "EmbeddingService"
Cohesion: 0.21
Nodes (5): build_embedding_text(), Command, EmbeddingService, EmbeddingServiceError, EmbeddingServiceTests

### Community 39 - "Function Triggers"
Cohesion: 0.15
Nodes (13): CLI, Delivery payload, Fields, Function Triggers, Inheritance, Local `neon dev`, Logs, MCP backup (+5 more)

### Community 50 - "mobile/package.json"
Cohesion: 0.18
Nodes (13): @react-navigation/native-stack@^7.18.10, devDependencies, babel-preset-expo@~57.0.15, @types/react@~19.2.2, typescript@~6.0.3, main, name, private (+5 more)

### Community 51 - "jobs.py"
Cohesion: 0.05
Nodes (26): backoff_seconds(), DiscoveryService, DiscoveryStats, enqueue_jobs(), IngestionJobService, JobRetry, per_adapter_limit(), recover_stale_jobs() (+18 more)

### Community 52 - "SourceDocument"
Cohesion: 0.05
Nodes (35): ingestion_status(), Command, CanonicalClaimSerializer, Meta, EvidenceSerializer, Meta, ExtractedClaimSerializer, Meta (+27 more)

### Community 53 - "scripts"
Cohesion: 0.18
Nodes (11): scripts, android, build:android:apk, build:preview, ios, lint, prebuild, start (+3 more)

### Community 55 - "client.ts"
Cohesion: 0.35
Nodes (7): completeProfile(), getProfile(), login(), register(), CompleteProfileScreen(), getAuthErrorMessage(), LoginScreen()

### Community 56 - "RootNavigator.tsx"
Cohesion: 0.21
Nodes (11): getExplanation(), getExtractedClaims(), getNotes(), getNoteStatus(), verifyClaim(), Stack, Tab, ClaimReviewScreen() (+3 more)

### Community 57 - "FlashcardGenerationService"
Cohesion: 0.17
Nodes (3): Command, Command, FlashcardGenerationService

### Community 58 - "learning/models.py"
Cohesion: 0.27
Nodes (8): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, UserProgressAdmin, PlaylistItem, Meta

### Community 59 - "IngestionItem"
Cohesion: 0.16
Nodes (10): IngestionItem, is_policy_enabled(), LicenseChecker, LicensePolicyError, policy_for_adapter(), PolicyDecision, resolve_policy(), _reviewed_sources() (+2 more)

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

### Community 67 - "pipeline.py"
Cohesion: 0.10
Nodes (14): best_supporting_passage(), claim_hash(), content_hash(), _content_tokens(), normalize_claim_text(), normalize_document_text(), ExternalIngestionPipeline, Command (+6 more)

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
Cohesion: 0.06
Nodes (14): CanViewOwnNotes, UserProfile, CompleteProfileSerializer, GoogleAuthSerializer, RegisterSerializer, Meta, create_user_profile(), CompleteProfileView (+6 more)

### Community 75 - "Managing Lakebase Search with Drizzle"
Cohesion: 0.29
Nodes (7): BM25 Index, Config, Extensions, Managing Lakebase Search with Drizzle, Query, Schema, Tune Per Query

### Community 76 - "KnowledgeExplorerScreen.tsx"
Cohesion: 0.24
Nodes (8): apiClient, BASE_URL, configuredApiUrl, CustomAxiosRequestConfig, getCanonicalClaims(), getEvidenceList(), getSources(), KnowledgeExplorerScreen()

### Community 77 - "package.json"
Cohesion: 0.31
Nodes (7): dependencies, expo@^58.0.25, @neon/config@^1.8.6, @neon/env@^1.5.3, expo, @neon/config, @neon/env

### Community 78 - "Evidence"
Cohesion: 0.06
Nodes (15): CanonicalClaim, Meta, EvidenceRetrievalError, EvidenceRetrievalService, RAGExplanationService, RAGExplanationServiceError, EvidenceRetrievalServiceTests, FakeEvidenceRetriever (+7 more)

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

### Community 84 - "provider_get"
Cohesion: 0.13
Nodes (13): _cooldown_key(), _json_or_none(), _min_interval(), provider_get(), _rate_key(), RateLimitedError, _retry_after_seconds(), robots_allows() (+5 more)

### Community 85 - "dependencies"
Cohesion: 0.12
Nodes (16): dependencies, axios@^1.20.0, expo@~57.0.29, expo-document-picker@~57.0.3, expo-secure-store@~57.0.4, lucide-react-native@^1.59.0, react@19.2.3, react-native@0.86.3 (+8 more)

### Community 88 - "learning/urls.py"
Cohesion: 0.14
Nodes (9): Playlist, Meta, PlaylistDetailSerializer, Meta, PlaylistSerializer, Meta, PlaylistDetailView, PlaylistListCreateView (+1 more)

### Community 89 - "App.tsx"
Cohesion: 0.24
Nodes (7): App(), styles, expo-status-bar@~57.0.1, @react-navigation/native@^7.3.18, RootNavigator(), expo-status-bar, @react-navigation/native

### Community 90 - "FlashcardFeedEvent"
Cohesion: 0.27
Nodes (3): FlashcardFeedEvent, Meta, FlashcardFeedView

### Community 91 - "IngestionJobTests"
Cohesion: 0.12
Nodes (5): FakeExtractor, FakeVerifier, LicensePolicyTests, PipelineIncrementalTests, wiki_item()

### Community 93 - "verification/tests.py"
Cohesion: 0.17
Nodes (5): ClaimVerificationServiceTests, NoteProcessJobIntegrationTests, test_embedding_task_skips_existing_embedding(), test_embedding_task_stores_vector(), test_placeholder_evidence_queues_embedding_after_commit()

### Community 94 - "Claimable Neon"
Cohesion: 0.29
Nodes (6): Claim, Claimable Neon, If neon claim is missing, Path, With REST, With the CLI

### Community 96 - "IsProfileComplete"
Cohesion: 0.14
Nodes (9): FlashcardFeedback, Meta, FlashcardFeedbackSerializer, Meta, FlashcardFeedbackView, FlashcardUnderstoodView, FlashcardViewedView, UserProgressSummaryView (+1 more)

### Community 98 - "SourceDocument"
Cohesion: 0.18
Nodes (3): SourceDocument, Meta, KnowledgeModelTests

### Community 99 - "learning.ts"
Cohesion: 0.21
Nodes (17): createPlaylist(), getFlashcards(), getPlaylists(), getProgressSummary(), getUserBadges(), markFlashcardUnderstood(), recordFlashcardView(), saveFlashcard() (+9 more)

### Community 101 - "FlashcardSerializer"
Cohesion: 0.27
Nodes (3): FlashcardSerializer, Meta, TopicSearchView

### Community 103 - "FlashcardGenerationIdempotencyTests"
Cohesion: 0.18
Nodes (3): FlashcardGenerationIdempotencyTests, FlashcardTaskTests, make_claim()

### Community 106 - "ClaimVerificationService"
Cohesion: 0.22
Nodes (3): ClaimVerificationService, dispatch_flashcard_generation(), VerifyClaimView

### Community 107 - "official_docs.py"
Cohesion: 0.23
Nodes (3): extract_main_text(), parse_sphinx_inventory(), _plain_text()

### Community 108 - "PermanentProviderError"
Cohesion: 0.19
Nodes (4): RedditAdapter, WikimediaAdapter, PermanentProviderError, ProviderError

### Community 109 - "registry.py"
Cohesion: 0.14
Nodes (8): ArxivAdapter, _base_id(), GitHubAdapter, BaseExternalAdapter, DiscoveryCandidate, DiscoveryPage, get_adapter(), UnknownAdapterError

### Community 113 - "ConceptRelationship"
Cohesion: 0.28
Nodes (4): Command, ConceptRelationship, Meta, invalidate_cached_graph()

### Community 114 - "metro.config.js"
Cohesion: 0.33
Nodes (4): { getDefaultConfig }, { withNativeWind }, nativewind@^4.2.7, nativewind

### Community 115 - "tests_feed.py"
Cohesion: 0.18
Nodes (4): pending_counts(), backfill_missing_flashcards_task(), generate_flashcard_for_claim_task(), _max_attempts()

### Community 116 - "Evidence"
Cohesion: 0.32
Nodes (4): Evidence, Meta, embed_evidence_task(), EvidenceRetrievalService

### Community 118 - "OfficialDocumentationAdapter"
Cohesion: 0.36
Nodes (3): DocSource, OfficialDocumentationAdapter, AccessDisallowedError

### Community 119 - "AdapterDiscoveryTests"
Cohesion: 0.15
Nodes (8): license_for_post(), site_domain(), StackExchangeAdapter, AdapterDiscoveryTests, route(), route(), route(), fake_response()

### Community 122 - "neon-functions/SKILL.md"
Cohesion: 0.21
Nodes (6): Authenticating the server, MCP servers on Neon Functions, Option 1 — OAuth via the Better Auth MCP plugin (best for third-party clients), Option 2 — API key or session JWT via self-hosted Better Auth (simplest), Testing, The server

### Community 125 - "learning/models.py"
Cohesion: 0.16
Nodes (12): MasteryBadge, Meta, Questionnaire, Meta, QuestionnaireQuestion, UserProgress, Meta, MasteryBadgeSerializer (+4 more)

### Community 126 - "env"
Cohesion: 0.14
Nodes (14): ALLOWED_HOSTS, CELERY_BROKER_URL, CELERY_RESULT_BACKEND, CORS_ALLOWED_ORIGINS, DATABASE_URL, DEBUG, GEMINI_API_KEY, GEMINI_CLAIM_MODEL (+6 more)

### Community 128 - "ExtractedClaim"
Cohesion: 0.14
Nodes (7): ExtractedClaim, NoteProcessingJobAdmin, Command, NoteProcessingJob, Meta, NoteProcessingService, process_note_task()

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

### Community 138 - "react"
Cohesion: 0.13
Nodes (8): BadgeProps, BadgeVariant, ButtonProps, ButtonSize, ButtonVariant, CardProps, InputProps, react

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 803 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **58 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Feed API contract` connect `SourceDocument` to `learning.ts`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 25 INFERRED edges - model-reasoned connections that need verification._
- **What connects `expo/tsconfig.base`, `Architecture Decisions`, `MOSAIC Project Report & Technical Architecture` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `notes/views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13230769230769232 - nodes in this community are weakly interconnected._
- **Why does `useFlashcardFeed()` connect `learning.ts` to `react`, `SourceDocument`?**
  _High betweenness centrality (0.138) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `Concept` (e.g. with `UnmappedConceptReviewAdmin` and `TopicPlanner`) actually correct?**
  _`Concept` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Should `learning/views.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._