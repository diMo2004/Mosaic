from rest_framework import serializers
from .models import CanonicalClaim, Evidence, ExtractedClaim, Source, SourceDocument

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

class ExtractedClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedClaim
        fields = [
            "id",
            "source_document",
            "text",
            "status",
            "confidence",
            "reviewed_notes",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]

class CanonicalClaimSerializer(serializers.ModelSerializer):
    concept_name = serializers.CharField(source='concept.name', read_only=True)
    class Meta:
        model = CanonicalClaim
        fields = [
            "id",
            "concept",
            "text",
            "source_claim",
            "concept_name",
            "is_active",
            "created_by_ai",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class EvidenceSerializer(serializers.ModelSerializer):
    claim_text = serializers.CharField(source='claim.text', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)
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

class SourceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceDocument
        fields = [
            "id",
            "title",
            "document_type",
            "source",
            "uploaded_note",
            "raw_text",
            "url",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]