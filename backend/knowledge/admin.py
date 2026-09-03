from django.contrib import admin
from .models import Evidence, Source, CanonicalClaim, Concept, ExtractedClaim, SourceDocument
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
    search_fields = ["text", "reviewer_notes"]
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
    search_fields = ["title", "excerpt", "url", "source_name", "claim_text"]

@admin.register(SourceDocument)
class SourceDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "document_type",
        "source",
        "uploaded_note",
        "created_at",
    ]
    list_filter = ["document_type", "created_at"]
    search_fields = ["title", "raw_text", "url"]

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
    search_fields = ["text", "concept_name"]

    def short_text(self, obj):
        return obj.text[:80]