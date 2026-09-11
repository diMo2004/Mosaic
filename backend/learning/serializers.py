from rest_framework import serializers
from .models import Flashcard, FlashcardFeedback, Playlist, PlaylistItem, UserProgress

class FlashcardSerializer(serializers.ModelSerializer):
    is_saved = serializers.SerializerMethodField()
    playlist_ids = serializers.SerializerMethodField()
    canonical_claim_id = serializers.IntegerField(
        source='source_claim.id', 
        read_only=True,
        allow_null=True,
    )
    canonical_claim_text = serializers.CharField(
        source='source_claim.text', 
        read_only=True,
        allow_null=True,
    )
    concept_id = serializers.IntegerField(
        source='source_claim.concept.id', 
        read_only=True,
        allow_null=True,
    )
    concept_name = serializers.CharField(
        source='source_claim.concept.name', 
        read_only=True,
        allow_null=True,
    )
    evidence = serializers.SerializerMethodField()

    class Meta:
        model = Flashcard
        fields = [
            "id",
            "title",
            "prompt",
            "answer",
            "explanation",
            "difficulty",
            "source_claim",
            "canonical_claim_id",
            "canonical_claim_text",
            "concept_id",
            "concept_name",
            "evidence",
            "created_at",
            "updated_at",
            "is_saved",
            "playlist_ids",
        ]
    def _user_playlist_items(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return PlaylistItem.objects.none()
        return PlaylistItem.objects.filter(
            playlist__user=request.user,
            flashcard=obj,
        )
    
    def get_is_saved(self, obj):
        return self._user_playlist_items(obj).exists()

    def get_playlist_ids(self, obj):
        return list(
            self._user_playlist_items(obj).values_list('playlist_id', flat=True)
            )
    def get_evidence(self, obj):
        if not obj.source_claim or not obj.source_claim.source_claim:
            return []
        items = obj.source_claim.source_claim.evidence_items.select_related('source')
        return [
            {
                "source": item.source.name,
                "title": item.title,
                "url": item.url,
                "excerpt": item.excerpt,
                "relation": item.relation,
                "relevance_score": str(item.relevance_score),
            }
            for item in items
        ]
    
class FlashcardFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashcardFeedback
        fields = [
            "id",
            "feedback_type",
            "comment",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    comment = serializers.CharField(
        required=False, 
        allow_blank=True,
        max_length=1000,
    )

class PlaylistSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Playlist
        fields = [
            "id",
            "name",
            "is_default",
            "item_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "is_default",
            "item_count",
            "created_at",
            "updated_at",
        ]

class PlaylistDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = [
            "id",
            "name",
            "is_default",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "is_default",
            "created_at",
            "updated_at",
        ]

    def get_items(self, obj):
        serializer = FlashcardSerializer(
            [item.flashcard for item in obj.items.select_related(
                "flashcard__source_claim__concept",
                "flashcard__source_claim__source_claim"
            )],
            many=True,
            context=self.context,
        )
        return serializer.data

class UserProgressSerializer(serializers.ModelSerializer):
    flashcard_title = serializers.CharField(source='flashcard.title', read_only=True)
    class Meta:
        model = UserProgress
        fields = [
            "id",
            "flashcard",
            "flashcard_title",
            "view_count",
            "last_viewed_at",
            "understood",
            "understood_at",
        ]