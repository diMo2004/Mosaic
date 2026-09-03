from django.contrib import admin
from .models import Flashcard, FlashcardFeedback, SavedFlashcard, UserProgress 
# Register your models here.

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "difficulty",
        "source_claim",
        "is_active",
        "created_by_ai",
        "created_at",
    ]
    list_filter = ["difficulty", "is_active", "created_by_ai"]
    search_fields = ["title", "prompt", "answer", "explanation"]

@admin.register(FlashcardFeedback)
class FlashcardFeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "flashcard",
        "user",
        "feedback_type",
        "created_at",
    ]
    list_filter = ["feedback_type", "created_at"]
    search_fields = ["flashcard__title", "user__username", "comment"]

@admin.register(SavedFlashcard)
class SavedFlashcardAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "flashcard",
        "saved_at",
    ]
    list_filter = ["saved_at"]
    search_fields = ["user__username", "flashcard__title"]

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "flashcard",
        "view_count",
        "last_viewed_at",
        "understood",
        "understood_at",
    ]
    list_filter = ["understood", "last_viewed_at"]
    search_fields = ["user__username", "flashcard__title"]
