from django.urls import path

from .views import (
    FlashcardDetailView,
    FlashcardFeedbackView,
    FlashcardFeedView,
    SaveFlashCardView,
    UserProgressSummaryView,
    GroundedExplanationView,
)

urlpatterns = [
    path("flashcards/", FlashcardFeedView.as_view(), name="flashcard-feed"),
    path("flashcards/<int:pk>/", FlashcardDetailView.as_view(), name="flashcard-detail"),
    path("flashcards/<int:pk>/save/", SaveFlashCardView.as_view(), name="flashcard-save"),
    path("flashcards/<int:pk>/feedback/", FlashcardFeedbackView.as_view(), name="flashcard-feedback"),
    path("progress/", UserProgressSummaryView.as_view(), name="progress-summary"),
    path("canonical-claims/<int:pk>/explain/", GroundedExplanationView.as_view(), name="grounded-explanation"),
]