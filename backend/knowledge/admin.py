from django.contrib import admin
from django.utils.text import slugify
from django.utils import timezone
from .models import Evidence, Source, CanonicalClaim, Concept, ExtractedClaim, SourceDocument, ConceptRelationship, UnmappedConceptReview, IngestionJob, SourceDiscoveryCheckpoint
from verification.services.concept_assignment import invalidate_cached_graph
# Register your models here.

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "domain",
        "source_type",
        "authority_score",
        "commercial_use_allowed",
        "ai_use_allowed",
        "scraping_allowed",
        "last_checked",
    ]
    list_filter = [
        "source_type",
        "commercial_use_allowed",
        "ai_use_allowed",
        "scraping_allowed",
        "api_available",
    ]
    search_fields = ["name", "domain", "license", "notes"]

class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 0
    fields = [
        "source",
        "relation",
        "title",
        "url",
        "relevance_score",
    ]

@admin.register(ExtractedClaim)
class ExtractedClaimAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "short_text",
        "status",
        "confidence",
        "source_document",
        "reviewed_by",
        "reviewed_at",
        "created_at",
    ]
    list_filter = ["status", "reviewed_at", "created_at"]
    search_fields = ["text", "reviewed_notes"]
    readonly_fields = ["created_at"]
    inlines = [EvidenceInline]

    def short_text(self, obj):
        return obj.text[:80]

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "claim",
        "source",
        "relation",
        "retrieved_at",
        "created_at",
        "relevance_score",
    ]
    list_filter = ["relation", "source", "created_at"]
    search_fields = ["title", "excerpt", "url", "source__name", "claim__text"]

@admin.register(SourceDocument)
class SourceDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "document_type",
        "source",
        "uploaded_note",
        "is_current",
        "created_at",
    ]
    list_filter = ["document_type", "is_current", "created_at"]
    search_fields = ["title", "raw_text", "url", "external_id"]

@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
        "created_at",
    ]
    search_fields = ["name", "description"]

@admin.register(CanonicalClaim)
class CanonicalClaimAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "short_text",
        "concept",
        "confidence",
        "is_active",
        "created_by_ai",
        "created_at",
    ]

    list_filter = ["is_active", "created_by_ai", "created_at"]
    search_fields = ["text", "concept__name"]

    def short_text(self, obj):
        return obj.text[:80]

@admin.register(ConceptRelationship)
class ConceptRelationshipAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "from_concept",
        "relation_type",
        "to_concept",
        "created_at"
    ]
    list_filter = ["relation_type", "created_at"]
    search_fields = ["from_concept__name", "to_concept__name"]

@admin.register(UnmappedConceptReview)
class UnmappedConceptReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "suggested_name",
        "status",
        "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["suggested_name", "context_text"]
    actions = ["approve_and_add_to_graph"]

    @admin.action(description="Approve selected terms and add them to official Concept taxonomy")
    def approve_and_add_to_graph(self, request, queryset):
        approved_count = 0
        root_cse, _ = Concept.objects.get_or_create(
            name="Computer Science & Engineering",
            defaults={"slug": "cse"}
        )
        for item in queryset.filter(status=UnmappedConceptReview.STATUS_PENDING):
            concept, _ = Concept.objects.get_or_create(
                slug=slugify(item.suggested_name),
                defaults={
                    "name": item.suggested_name,
                    "description": f"Approved from context: {item.context_text[:100]}",
                }
            )
            parent_concept = root_cse
            if item.context_claim and hasattr(item.context_claim, 'canonical_claim'):
                canonical = item.context_claim.canonical_claims.first()
                if canonical and canonical.concept:
                    parent_concept = canonical.concept

            ConceptRelationship.objects.get_or_create(
                from_concept=concept,
                to_concept=parent_concept,
                relation_type=ConceptRelationship.RELATION_PARENT,
            )
            item.status = UnmappedConceptReview.STATUS_APPROVED
            item.reviewed_by = request.user
            item.resolution_notes = f"Approved as Concept #{concept.id}, parented under '{parent_concept.name}'."
            item.save()
            approved_count += 1

        invalidate_cached_graph()
        self.message_user(request, f"Successfully approved {approved_count} concept(s) into taxonomy.")


@admin.register(IngestionJob)
class IngestionJobAdmin(admin.ModelAdmin):
    list_display = ["id", "adapter", "external_id", "status", "attempts", "topic", "discovered_at", "completed_at"]
    list_filter = ["adapter", "status"]
    search_fields = ["external_id", "identifier", "title", "url", "last_error"]
    readonly_fields = ["discovered_at", "enqueued_at", "started_at", "completed_at", "updated_at", "result", "last_error"]
    actions = ["retry_jobs"]

    @admin.action(description="Retry selected jobs now")
    def retry_jobs(self, request, queryset):
        from knowledge.ingestion.jobs import enqueue_jobs

        ids = list(queryset.exclude(status=IngestionJob.STATUS_PROCESSING).values_list("id", flat=True))
        IngestionJob.objects.filter(id__in=ids).update(
            status=IngestionJob.STATUS_PENDING, attempts=0, next_attempt_at=None, locked_until=None,
        )
        enqueue_jobs(ids)
        self.message_user(request, f"Re-queued {len(ids)} job(s).")


@admin.register(SourceDiscoveryCheckpoint)
class SourceDiscoveryCheckpointAdmin(admin.ModelAdmin):
    list_display = ["adapter", "topic", "runs", "candidates_total", "exhausted", "consecutive_failures", "last_success_at", "next_run_at"]
    list_filter = ["adapter", "exhausted"]
    search_fields = ["topic", "last_error"]
    actions = ["reset_checkpoints"]

    @admin.action(description="Reset cursor and run on next schedule")
    def reset_checkpoints(self, request, queryset):
        updated = queryset.update(cursor={}, exhausted=False, next_run_at=None, lease_until=None, consecutive_failures=0)
        self.message_user(request, f"Reset {updated} checkpoint(s).")
