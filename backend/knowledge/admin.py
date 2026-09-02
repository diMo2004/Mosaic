from django.contrib import admin
from .models import Claim, Evidence, Source
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

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "short_text",
        "status",
        "confidence",
        "reviewed_by",
        "reviewed_at",
        "created_from_note",
        "created_at",
    ]
    list_filter = ["status", "confidence", "reviewed_by"]
    search_fields = ["text", "reviewer_notes"]
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