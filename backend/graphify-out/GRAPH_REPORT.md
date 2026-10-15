# Graph Report - backend  (2026-10-15)

## Corpus Check
- 110 files · ~16,606 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .example 1)

## Summary
- 632 nodes · 1506 edges · 48 communities (23 shown, 25 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 221 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0441b071`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- UserProfile
- Source
- learning/views.py
- knowledge/admin.py
- Evidence
- django_db_models_deletion
- FlashcardAPITests
- os
- HybridOCRProvider
- CanViewOwnNotes
- knowledge/tests.py
- Concept
- knowledge/views.py
- django_apps
- learning/serializers.py
- CompleteProfileView
- GoogleAuthTests
- ClaimVerificationService
- PlaceholderOCRProvider
- django_conf
- concept_assignment.py
- users/views.py
- settings.py
- manage.py
- learning/admin.py
- FlashcardSerializer
- AuthTests
- ProfileAwareTokenObtainPairSerializer
- RegisterSerializer

## God Nodes (most connected - your core abstractions)
1. `Source` - 39 edges
2. `Evidence` - 36 edges
3. `ExtractedClaim` - 29 edges
4. `Concept` - 29 edges
5. `IngestionItem` - 28 edges
6. `ClaimVerificationService` - 26 edges
7. `CanonicalClaim` - 24 edges
8. `SourceDocument` - 23 edges
9. `FlashcardAPITests` - 22 edges
10. `MasteryService` - 21 edges

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

## Communities (48 total, 25 thin omitted)

### Community 0 - "UserProfile"
Cohesion: 0.24
Nodes (7): django_contrib_auth_models, django_db_models_signals, django_dispatch, profile, receiver, UserProfile, create_user_profile()

### Community 1 - "Source"
Cohesion: 0.06
Nodes (49): base64, dataclasses, decimal, django_contrib_postgres_indexes, django_contrib_postgres_operations, django_db, django_utils, ArxivAdapter (+41 more)

### Community 2 - "learning/views.py"
Cohesion: 0.06
Nodes (37): django_db_models, django_shortcuts, django_urls, MasteryBadgeSerializer, QuestionnaireQuestionReviewSerializer, active_flashcards(), FlashcardDetailView, FlashcardFeedbackView (+29 more)

### Community 3 - "knowledge/admin.py"
Cohesion: 0.13
Nodes (16): action, django_contrib, django_utils_text, CanonicalClaimAdmin, ConceptAdmin, ConceptRelationshipAdmin, EvidenceAdmin, EvidenceInline (+8 more)

### Community 4 - "Evidence"
Cohesion: 0.07
Nodes (26): Any, Migration, CanonicalClaim, Evidence, EvidenceRetrievalError, EvidenceRetrievalService, RuntimeError, Raised when semantic evidence retrieval cannot be completed. (+18 more)

### Community 5 - "django_db_models_deletion"
Cohesion: 0.09
Nodes (12): django_db_models_deletion, Migration, Migration, Migration, Migration, Migration, Migration, Migration (+4 more)

### Community 6 - "FlashcardAPITests"
Cohesion: 0.15
Nodes (3): FlashcardGenerationService, Generate flashcards from a given canonical claim., FlashcardAPITests

### Community 7 - "os"
Cohesion: 0.29
Nodes (5): ASGI config for config project. It exposes the ASGI callable as a module-level…, WSGI config for config project. It exposes the WSGI callable as a module-level…, django_core_asgi, django_core_wsgi, os

### Community 8 - "HybridOCRProvider"
Cohesion: 0.12
Nodes (13): google_api_core, io, mimetypes, pil, OCRProvider, ABC, get_azure_client(), get_gemini_model() (+5 more)

### Community 9 - "CanViewOwnNotes"
Cohesion: 0.33
Nodes (4): CanViewOwnNotes, BasePermission, Custom permission to allow users to view their own notes., rest_framework_permissions

### Community 10 - "knowledge/tests.py"
Cohesion: 0.06
Nodes (18): django_core_files_uploadedfile, django_test, build_embedding_text(), Command, BaseCommand, EmbeddingService, EmbeddingServiceError, RuntimeError (+10 more)

### Community 11 - "Concept"
Cohesion: 0.21
Nodes (8): Concept, Questionnaire, QuestionnaireQuestionClientSerializer, MasteryService, atomic, Returns the next unpassed tier (1 to 5), or 6 if all 5 are passed., ConceptMasteryStatusView, StartQuestionnaireView

### Community 12 - "knowledge/views.py"
Cohesion: 0.20
Nodes (13): CanonicalClaimSerializer, EvidenceSerializer, ExtractedClaimSerializer, Meta, SourceDocumentSerializer, SourceSerializer, CanonicalClaimViewSet, EvidenceViewSet (+5 more)

### Community 13 - "django_apps"
Cohesion: 0.12
Nodes (11): django_apps, KnowledgeConfig, AppConfig, LearningConfig, AppConfig, NotesConfig, AppConfig, AppConfig (+3 more)

### Community 14 - "learning/serializers.py"
Cohesion: 0.23
Nodes (10): FlashcardFeedback, MasteryBadge, Meta, Playlist, UserProgress, FlashcardFeedbackSerializer, Meta, PlaylistDetailSerializer (+2 more)

### Community 15 - "CompleteProfileView"
Cohesion: 0.20
Nodes (8): CompleteProfileSerializer, GoogleAuthSerializer, CompleteProfileView, GoogleAuthView, HealthCheckView, jwt_response_for_user(), APIView, RegisterView

### Community 17 - "ClaimVerificationService"
Cohesion: 0.06
Nodes (22): django_core_management_base, override_settings, Command, BaseCommand, Meta, NoteProcessingJob, ClaimExtractionService, get_extractor_model() (+14 more)

### Community 36 - "django_conf"
Cohesion: 0.25
Nodes (7): django_conf, google, google_genai, json, Flashcard, QuestionnaireQuestion, math

### Community 37 - "concept_assignment.py"
Cohesion: 0.12
Nodes (13): Command, BaseCommand, ConceptRelationship, Meta, UnmappedConceptReview, networkx, pickle, re (+5 more)

### Community 38 - "users/views.py"
Cohesion: 0.20
Nodes (10): URL configuration for config project. The `urlpatterns` list routes URLs to…, django_conf_urls_static, django_core_cache, google_auth_transport, google_oauth2, rest_framework_simplejwt_serializers, rest_framework_simplejwt_tokens, rest_framework_simplejwt_views (+2 more)

### Community 39 - "settings.py"
Cohesion: 0.40
Nodes (3): dj_database_url, dotenv, pathlib

### Community 40 - "manage.py"
Cohesion: 0.40
Nodes (4): main(), Django's command-line utility for administrative tasks., Run administrative tasks., sys

### Community 41 - "learning/admin.py"
Cohesion: 0.31
Nodes (8): FlashcardAdmin, FlashcardFeedbackAdmin, PlaylistAdmin, PlaylistItemAdmin, PlaylistItemInline, register, UserProgressAdmin, PlaylistItem

## Knowledge Gaps
- **21 isolated node(s):** `Migration`, `Migration`, `Migration`, `Migration`, `Migration` (+16 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 229 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Source` connect `Source` to `knowledge/admin.py`, `Evidence`, `concept_assignment.py`, `FlashcardAPITests`, `knowledge/tests.py`, `knowledge/views.py`, `ClaimVerificationService`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `Concept` connect `Concept` to `Source`, `learning/views.py`, `knowledge/admin.py`, `django_conf`, `concept_assignment.py`, `Evidence`, `FlashcardAPITests`, `knowledge/tests.py`, `ClaimVerificationService`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `HybridOCRProvider` connect `HybridOCRProvider` to `Source`, `ClaimVerificationService`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `Source` (e.g. with `ArxivAdapter` and `GitHubAdapter`) actually correct?**
  _`Source` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Evidence` (e.g. with `EvidenceInline` and `ExternalIngestionPipeline`) actually correct?**
  _`Evidence` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `ExtractedClaim` (e.g. with `ExternalIngestionPipeline` and `ExtractedClaimSerializer`) actually correct?**
  _`ExtractedClaim` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `Concept` (e.g. with `UnmappedConceptReviewAdmin` and `Command`) actually correct?**
  _`Concept` has 13 INFERRED edges - model-reasoned connections that need verification._