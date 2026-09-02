from rest_framework import serializers
from .models import Claim, Evidence, Source

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = [
            "id",
            "name",
            "domain",
            "source_type",
            "access_method",
            "license",
            "license_url",
            "attribution_required",
            "commercial_use_allowed",
            "ai_use_allowed",
            "scraping_allowed",
            "api_available",
            "authority_score",
            "last_checked",
            "notes",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = [
            "id",
            "text",
            "status",
            "confidence",
            "reviewer_notes",
            "reviewed_by",
            "reviewed_at",
            "created_from_note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = [
            "id",
            "claim",
            "claim_text",
            "source",
            "source_name",
            "relation",
            "url",
            "title",
            "excerpt",
            "retrieved_at",
            "relevance_score",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]