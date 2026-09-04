from rest_framework import serializers
from .models import Flashcard, FlashcardFeedback, SavedFlashcard, UserProgress

class FlashcardSerializer(serializers.ModelSerializer):
    is_saved = serializers.SerializerMethodField()
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
            "created_at",
            "updated_at",
            "is_saved",
        ]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return SavedFlashcard.objects.filter(
            user=request.user,
            flashcard=obj,
        ).exists()

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