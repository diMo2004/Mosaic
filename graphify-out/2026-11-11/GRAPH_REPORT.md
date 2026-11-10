# Graph Report - Mosaic  (2026-10-22)

## Corpus Check
- 226 files · ~123,303 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 7, .example 2, .css 1)

## Summary
- 1677 nodes · 3643 edges · 127 communities (84 shown, 43 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 397 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `71bac54e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- notes/views.py
- learning/views.py
- config/urls.py
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
- MasteryService
- PlaceholderOCRProvider
- Docker Compose Configuration
- Lakebase Postgres Branching
- CSE Technology & Concept Knowledge Graph
- Current State
- AuthTests
- UserProfile
- mobile/package.json
- Function Triggers
- AGENTS.md
- copilot-instructions.md
- AGENTS.md
- django_conf
- IngestionJob
- SourceDocument
- scripts
- d_mosaic_backend_learning_services_py
- client.ts
- RootNavigator.tsx
- FlashcardGenerationService
- learning/admin.py
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
- RAGExplanationService
- AI SDK agents on Neon Functions
- KnowledgeAPIPermissionTests
- Full-Text Search with BM25 Ranking
- Setup Flow
- Troubleshooting and Neon-Specific Performance
- provider_get
- dependencies
- Logs: CLI, Loki, and SDK pagination
- sdk.md
- learning/models.py
- App.tsx
- FlashcardFeedEvent
- IngestionJobTests
- manage.py
- verification/tests.py
- Claimable Neon
- CanViewOwnNotes
- Source
- useFlashcardFeed.ts
- ingestion_status
- FlashcardSerializer
- Concept
- jobs.py
- neon/references/function-triggers.md
- ExtractedClaim
- metro.config.js
- AdapterDiscoveryTests
- PermanentProviderError
- nativewind-env.d.ts
- devDependencies
- tests_ingestion.py
- CanonicalClaim
- IsProfileComplete
- FeedPaginationTests
- OfficialDocumentationAdapter
- StackExchangeAdapter
- license_checker.py
- NotePermissionTests
- MCP servers on Neon Functions
- 0010_deduplicate_active_flashcards.py
- MasteryBadge
- StartQuestionnaireView

## God Nodes (most connected - your core abstractions)
1. `Source` - 47 edges
2. `Concept` - 43 edges
3. `Evidence` - 41 edges
4. `IngestionItem` - 40 edges
5. `ExtractedClaim` - 38 edges
6. `provider_get()` - 35 edges
7. `CanonicalClaim` - 35 edges
8. `FlashcardGenerationService` - 35 edges
9. `ClaimVerificationService` - 34 edges
10. `SourceDocument` - 33 edges

## Surprising Connections (you probably didn't know these)
- `5. Pass the creds via `neon.ts` (third-party env)` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/mastra-studio.md → backend/config/settings.py
- `Option 1 — OAuth via the Better Auth MCP plugin (best for third-party clients)` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/mcp.md → backend/config/settings.py
- `Standalone executables` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/native-binaries.md → backend/config/settings.py
- `Trusted app server` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/production-hardening.md → backend/config/settings.py
- `2. Provide the DSN as a deploy-time secret` --references--> `env()`  [INFERRED]
  .claude/skills/neon-functions/references/sentry.md → backend/config/settings.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Knowledge Ingestion Pipeline** — backend_notes, backend_verification, backend_knowledge, backend_learning [EXTRACTED 1.00]
- **MVP Technology Stack** — docker_compose, github_actions_ci, backend_users [EXTRACTED 1.00]

## Communities (127 total, 43 thin omitted)

### Community 0 - "notes/views.py"
Cohesion: 0.16
Nodes (11): NoteAdmin, register, Meta, Note, Meta, NoteDetailSerializer, NoteUploadSerializer, enqueue_note_processing() (+3 more)

### Community 1 - "learning/views.py"
Cohesion: 0.11
Nodes (18): FlashcardFeedbackSerializer, active_flashcards(), ConceptMasteryStatusView, feed_eligible_flashcards(), FlashcardDetailView, FlashcardFeedbackView, FlashcardUnderstoodView, FlashcardViewedView (+10 more)

### Community 2 - "config/urls.py"
Cohesion: 0.25
Nodes (6): URL configuration for config project. The `urlpatterns` list routes URLs to…, ProfileAwareTokenObtainPairView, django_conf_urls_static, django_contrib, rest_framework_simplejwt_views, TokenObtainPairView

### Community 3 - "learning.ts"
Cohesion: 0.11
Nodes (33): createPlaylist(), getFlashcardDetail(), getMasteryStatus(), getPlaylistDetail(), getPlaylists(), saveFlashcard(), searchFlashcardsByTopic(), sendFeedback() (+25 more)

### Community 4 - "knowledge/admin.py"
Cohesion: 0.16
Nodes (14): action, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline, ExtractedClaimAdmin, IngestionJobAdmin (+6 more)

### Community 5 - "Neon"
Cohesion: 0.05
Nodes (36): Auth, 1. Install the Neon CLI, 2. Install the Neon MCP Server, 3. Install Neon Agent Skills, 4. Link Your Project and Get Started, Architecture: How to Use Neon, Backend Primitives, Bootstrap a New Project (+28 more)

### Community 6 - "expo"
Cohesion: 0.06
Nodes (34): backgroundColor, backgroundImage, foregroundImage, monochromeImage, adaptiveIcon, package, permissions, predictiveBackGestureEnabled (+26 more)

### Community 7 - "django_db"
Cohesion: 0.05
Nodes (29): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+21 more)

### Community 8 - "env"
Cohesion: 0.16
Nodes (12): env(), env_bool(), env_list(), Application instrumentation, Built-in branch logs, Functions as an Agent Backend (Next.js and Similar Frameworks), Integrations and Observability, Neon Infrastructure as Code (`neon.ts`) (+4 more)

### Community 9 - "HybridOCRProvider"
Cohesion: 0.10
Nodes (14): atomic, OCRProvider, ABC, get_azure_client(), get_gemini_model(), HybridOCRProvider, Attempts OCR & visual analysis via Gemini-1.5-Flash. Falls back to Azure…, Dispatches to Text Parser, Document Parser, or Multimodal Image Parser and… (+6 more)

### Community 10 - "flashcard.ts"
Cohesion: 0.12
Nodes (27): CardRendererProps, CardShell(), CardShellProps, formatCardType(), getDifficultyStyle(), getTypeBadgeStyle(), { height: WINDOW_HEIGHT }, styles (+19 more)

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

### Community 16 - "MasteryService"
Cohesion: 0.24
Nodes (6): Questionnaire, QuestionnaireQuestionReviewSerializer, MasteryService, atomic, Returns the next unpassed tier (1 to 5), or 6 if all 5 are passed., SubmitQuestionnaireView

### Community 19 - "Lakebase Postgres Branching"
Cohesion: 0.08
Nodes (25): Beta Support Guidance (Mandatory), Branch Type Decision, Branching in CI/CD, CLI usage, Console and API usage, Create a Normal Branch (Preferred for Real-Data Migration Testing), Create a Schema-Only Branch (Beta, Sensitive Data), Example 1: Migration testing with realistic data (+17 more)

### Community 36 - "AuthTests"
Cohesion: 0.16
Nodes (5): AuthTests, GoogleAuthTests, HealthCheckTests, APITestCase, patch

### Community 37 - "UserProfile"
Cohesion: 0.20
Nodes (8): UserProfile, Meta, RegisterSerializer, create_user_profile(), django_db_models_signals, django_dispatch, profile, receiver

### Community 38 - "mobile/package.json"
Cohesion: 0.13
Nodes (14): main, name, private, version, babel-preset-expo, expo-dev-client, react-native-safe-area-context, react-native-screens (+6 more)

### Community 39 - "Function Triggers"
Cohesion: 0.15
Nodes (13): CLI, Delivery payload, Fields, Function Triggers, Inheritance, Local `neon dev`, Logs, MCP backup (+5 more)

### Community 50 - "django_conf"
Cohesion: 0.08
Nodes (21): Migration, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+13 more)

### Community 51 - "IngestionJob"
Cohesion: 0.06
Nodes (31): IngestionJobService, JobRetry, Process one job. Raises JobRetry when a transient failure should be retried., Re-enqueue jobs lost to dispatch failures, worker crashes, or missed retries., recover_stale_jobs(), enabled_adapters(), Adapters configured for scheduled discovery whose source policy allows…, pending_counts() (+23 more)

### Community 52 - "SourceDocument"
Cohesion: 0.17
Nodes (15): SourceDocument, CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer, CanonicalClaimViewSet (+7 more)

### Community 53 - "scripts"
Cohesion: 0.18
Nodes (11): scripts, android, build:android:apk, build:preview, ios, lint, prebuild, start (+3 more)

### Community 55 - "client.ts"
Cohesion: 0.18
Nodes (13): completeProfile(), getProfile(), login(), register(), apiClient, BASE_URL, configuredApiUrl, CustomAxiosRequestConfig (+5 more)

### Community 56 - "RootNavigator.tsx"
Cohesion: 0.12
Nodes (25): getExplanation(), getProgressSummary(), getUserBadges(), getExtractedClaims(), getNotes(), getNoteStatus(), uploadNote(), verifyClaim() (+17 more)

### Community 57 - "FlashcardGenerationService"
Cohesion: 0.06
Nodes (11): Command, BaseCommand, Command, BaseCommand, FlashcardGenerationService, Generate flashcards from a given canonical claim., Return a meaningful recall pair when model generation is unavailable., FlashcardGenerationIdempotencyTests (+3 more)

### Community 58 - "learning/admin.py"
Cohesion: 0.31
Nodes (8): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin, PlaylistItem

### Community 59 - "IngestionItem"
Cohesion: 0.16
Nodes (17): ArxivAdapter, _base_id(), http://arxiv.org/abs/2301.00001v2' -> '2301.00001'., Fetches academic computer science preprint metadata (title + abstract) from…, GitHubAdapter, Fetches README and doc markdown from GitHub repositories., BaseExternalAdapter, DiscoveryCandidate (+9 more)

### Community 60 - "Postgres Egress Optimizer"
Cohesion: 0.12
Nodes (16): Application-side aggregation, Check if pg_stat_statements is available, Diagnostic queries, Further Reading, Handle empty stats, High-frequency queries on static data, Interpret the results, JOIN duplication (+8 more)

### Community 61 - "Neon AI Gateway"
Cohesion: 0.12
Nodes (15): Availability, Build Agents with Mastra (Recommended), Build Agents with the Vercel AI SDK (Recommended), Enabling the gateway: plan and model-catalog gating, Environment Variables, Further Reading, List Available Models at Runtime (`/v1/models`), Model Identifiers (+7 more)

### Community 62 - "Neon Functions"
Cohesion: 0.10
Nodes (20): Architecture: Where Functions Fit, Availability, Client must reconnect, Connecting to Postgres, Develop Locally and Deploy, Function Triggers, Further Reading, Heartbeat (keep the socket alive) (+12 more)

### Community 63 - "Neon Object Storage"
Cohesion: 0.13
Nodes (14): Architecture: Where Object Storage Fits, Availability, Built-in Branch Logs, CLI Bucket and Object Commands, Environment Variables, Further Reading, Neon Documentation, Neon Infrastructure as Code (`neon.ts`) (+6 more)

### Community 64 - "Sentry (errors, logs, and traces)"
Cohesion: 0.22
Nodes (9): 2. Provide the DSN as a deploy-time secret, 3. Create the request span and catch route errors, 4. Errors are for failures; logs are for the story, 5. Trace the agent itself, Environment variables, Other Node integrations, Sentry error monitoring on Neon Functions, Sentry (errors, logs, and traces) (+1 more)

### Community 66 - "Lakebase Postgres"
Cohesion: 0.15
Nodes (13): Autoscaling, Branching, Connection Pooling, Gotchas, Instant Restore, IP Allow Lists, Lakebase Postgres, Lakebase Search (+5 more)

### Community 67 - "pipeline.py"
Cohesion: 0.09
Nodes (23): best_supporting_passage(), claim_hash(), content_hash(), _content_tokens(), normalize_claim_text(), normalize_document_text(), Text normalization used for change detection, deduplication, and grounding., Hash of whitespace-normalized document text; ignores formatting-only changes. (+15 more)

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
Cohesion: 0.14
Nodes (14): CompleteProfileSerializer, GoogleAuthSerializer, CompleteProfileView, GoogleAuthView, HealthCheckView, jwt_response_for_user(), ProfileAwareTokenObtainPairSerializer, APIView (+6 more)

### Community 75 - "Managing Lakebase Search with Drizzle"
Cohesion: 0.29
Nodes (7): BM25 Index, Config, Extensions, Managing Lakebase Search with Drizzle, Query, Schema, Tune Per Query

### Community 76 - "KnowledgeExplorerScreen.tsx"
Cohesion: 0.57
Nodes (4): getCanonicalClaims(), getEvidenceList(), getSources(), KnowledgeExplorerScreen()

### Community 77 - "package.json"
Cohesion: 0.29
Nodes (5): dependencies, @neon/config, @neon/env, @neon/config, @neon/env

### Community 78 - "RAGExplanationService"
Cohesion: 0.07
Nodes (17): Any, EvidenceRetrievalError, EvidenceRetrievalService, RuntimeError, Raised when semantic evidence retrieval cannot be completed., RuntimeError, RAGExplanationService, RAGExplanationServiceError (+9 more)

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
Cohesion: 0.12
Nodes (24): Reddit evidence adapter (disabled unless legally cleared). Reddit's Data API…, _cooldown_key(), _json_or_none(), _min_interval(), provider_get(), _rate_key(), RateLimitedError, Shared HTTP access for external source adapters. Every provider request goes… (+16 more)

### Community 85 - "dependencies"
Cohesion: 0.11
Nodes (18): dependencies, axios, expo, expo-dev-client, expo-document-picker, expo-secure-store, expo-status-bar, lucide-react-native (+10 more)

### Community 88 - "learning/models.py"
Cohesion: 0.20
Nodes (10): FlashcardFeedback, Meta, Playlist, QuestionnaireQuestion, UserProgress, Meta, PlaylistDetailSerializer, PlaylistSerializer (+2 more)

### Community 89 - "App.tsx"
Cohesion: 0.25
Nodes (7): App(), styles, mobile_global, RootNavigator(), expo, expo-status-bar, @react-navigation/native

### Community 90 - "FlashcardFeedEvent"
Cohesion: 0.24
Nodes (5): FlashcardFeedEvent, Durable feed delivery history used to avoid immediate repetition., FlashcardFeedView, Stable round-robin across concepts within each tier., Server-ranked, continuously replenished feed. Pagination uses a server-side…

### Community 91 - "IngestionJobTests"
Cohesion: 0.06
Nodes (18): LicenseChecker, LicensePolicyError, PolicyDecision, RuntimeError, Raised when an external source fails licensing or AI-use policies., ExternalIngestionTests, FakeAdapter, FakeExtractor (+10 more)

### Community 92 - "manage.py"
Cohesion: 0.29
Nodes (6): main(), Django's command-line utility for administrative tasks., Run administrative tasks., 1. Initialize before anything else, Environment Variables, sys

### Community 93 - "verification/tests.py"
Cohesion: 0.19
Nodes (10): NoteProcessingService, ClaimVerificationServiceTests, NoteProcessJobIntegrationTests, override_settings, patch, TestCase, test_embedding_task_skips_existing_embedding(), test_embedding_task_stores_vector() (+2 more)

### Community 94 - "Claimable Neon"
Cohesion: 0.29
Nodes (6): Claim, Claimable Neon, If neon claim is missing, Path, With REST, With the CLI

### Community 96 - "CanViewOwnNotes"
Cohesion: 0.50
Nodes (3): CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes.

### Community 98 - "Source"
Cohesion: 0.13
Nodes (16): Evidence, Determines if content from this source can be fed to external LLMs, Determines if derived excerpts/flashcards can be shared publicly., Source, GroundedExplanationAPITests, APITestCase, RAGExplanationServiceTests, EvidenceRetrievalService (+8 more)

### Community 99 - "useFlashcardFeed.ts"
Cohesion: 0.20
Nodes (14): Feed API contract, getFlashcards(), markFlashcardUnderstood(), recordFlashcardView(), CardRenderer(), mobile_src_components_cards_index_cardrenderer, errorMessage(), FeedStatus (+6 more)

### Community 100 - "ingestion_status"
Cohesion: 0.08
Nodes (22): ingestion_status(), Command, BaseCommand, IngestionRunView, IngestionStatusView, APIView, Staff-only operational status for external ingestion and card inventory., Staff-only: enqueue one bounded discovery run for an adapter. (+14 more)

### Community 101 - "FlashcardSerializer"
Cohesion: 0.27
Nodes (3): FlashcardSerializer, License/attribution notice for the source the card was derived from., TopicSearchView

### Community 102 - "Concept"
Cohesion: 0.07
Nodes (24): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, UnmappedConceptReviewAdmin, Command, BaseCommand, Concept, ConceptRelationship, Meta (+16 more)

### Community 103 - "jobs.py"
Cohesion: 0.14
Nodes (15): backoff_seconds(), DiscoveryService, DiscoveryStats, per_adapter_limit(), Durable discovery and ingestion job orchestration. Flow (all steps idempotent,…, Bounded exponential backoff with full jitter on top of the base delay., Chooses CSE taxonomy topics that most need flashcards., Return [(topic_key, topic, concept)] for one discovery run. (+7 more)

### Community 106 - "ExtractedClaim"
Cohesion: 0.17
Nodes (8): ExtractedClaim, DeferredVerificationTests, patch, ClaimVerificationService, dispatch_flashcard_generation(), Enqueue card generation; a broker failure is logged, and the periodic…, Return (canonical_claim, created). Idempotent per extracted claim and per fact…, Verify a claim and, when supported, canonicalize it and produce its flashcard.…

### Community 107 - "metro.config.js"
Cohesion: 0.50
Nodes (3): { getDefaultConfig }, { withNativeWind }, nativewind

### Community 108 - "AdapterDiscoveryTests"
Cohesion: 0.13
Nodes (7): Fetches articles from Wikipedia/Wikimedia REST API., WikimediaAdapter, AdapterDiscoveryTests, route(), route(), route(), NO_RATE_LIMIT

### Community 109 - "PermanentProviderError"
Cohesion: 0.17
Nodes (10): Fetches community discussion strictly for evidence attribution after legal…, RedditAdapter, PermanentProviderError, ProviderError, RuntimeError, Base class for provider failures., 4xx responses (other than 429) and malformed payloads. Do not retry., get_adapter() (+2 more)

### Community 113 - "devDependencies"
Cohesion: 0.50
Nodes (4): devDependencies, babel-preset-expo, @types/react, typescript

### Community 114 - "tests_ingestion.py"
Cohesion: 0.18
Nodes (12): extract_main_text(), parse_sphinx_inventory(), First-party programming-language documentation adapter. The registry is…, Return documentation page URLs (std:doc entries) from a Sphinx objects.inv., AccessDisallowedError, robots.txt or the source allowlist forbids this URL., django_utils_html, gzip (+4 more)

### Community 115 - "CanonicalClaim"
Cohesion: 0.20
Nodes (10): CanonicalClaim, backfill_missing_flashcards_task(), generate_flashcard_for_claim_task(), _max_attempts(), shared_task, Generate (idempotently) the flashcard for a verified canonical claim., Re-dispatch generation for supported claims whose card task was lost or failed.…, FlashcardTaskTests (+2 more)

### Community 116 - "IsProfileComplete"
Cohesion: 0.16
Nodes (9): IsProfileComplete, BasePermission, Allows access only to users with a complete profile., APIView, VerifyClaimView, django_shortcuts, rest_framework_permissions, rest_framework_response (+1 more)

### Community 117 - "FeedPaginationTests"
Cohesion: 0.32
Nodes (3): FeedPaginationTests, make_card(), APITestCase

### Community 118 - "OfficialDocumentationAdapter"
Cohesion: 0.32
Nodes (4): DocSource, OfficialDocumentationAdapter, Discovery is keyed by language, not by taxonomy topic., policy_key_for()

### Community 119 - "StackExchangeAdapter"
Cohesion: 0.29
Nodes (5): license_for_post(), _plain_text(), Fetches high-quality answers from Stack Overflow or CSE Stack Exchange., site_domain(), StackExchangeAdapter

### Community 120 - "license_checker.py"
Cohesion: 0.33
Nodes (7): is_policy_enabled(), policy_for_adapter(), Source-policy enforcement for every external ingestion item. Permissions are…, resolve_policy(), _reviewed_sources(), SourcePolicy, dataclasses

### Community 123 - "MCP servers on Neon Functions"
Cohesion: 0.33
Nodes (6): Authenticating the server, MCP servers on Neon Functions, Option 1 — OAuth via the Better Auth MCP plugin (best for third-party clients), Option 2 — API key or session JWT via self-hosted Better Auth (simplest), Testing, The server

### Community 124 - "0010_deduplicate_active_flashcards.py"
Cohesion: 0.40
Nodes (3): deactivate_duplicate_active_cards(), Migration, Keep the oldest active card per canonical claim; deactivate (not delete) the…

### Community 125 - "MasteryBadge"
Cohesion: 0.60
Nodes (3): MasteryBadge, MasteryBadgeSerializer, UserMasteryBadgesView

## Knowledge Gaps
- **381 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+376 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 705 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **43 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Continuous external ingestion and the flashcard feed` connect `ingestion_status` to `useFlashcardFeed.ts`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `Feed API contract` connect `useFlashcardFeed.ts` to `ingestion_status`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `ingestion_status()` connect `ingestion_status` to `jobs.py`, `django_conf`, `CanonicalClaim`, `IngestionJob`, `SourceDocument`, `FlashcardFeedEvent`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Concept` (e.g. with `UnmappedConceptReviewAdmin` and `TopicPlanner`) actually correct?**
  _`Concept` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `ExternalIngestionPipeline`) actually correct?**
  _`Evidence` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `IngestionItem` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`IngestionItem` has 13 INFERRED edges - model-reasoned connections that need verification._