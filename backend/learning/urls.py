from django.urls import path

from .views import (
    ConceptMasteryStatusView,
    FlashcardDetailView,
    FlashcardFeedbackView,
    FlashcardFeedView,
    TopicSearchView,
    FlashcardUnderstoodView,
    FlashcardViewedView,
    SaveFlashCardView,
    StartQuestionnaireView,
    SubmitQuestionnaireView,
    UserMasteryBadgesView,
    UserProgressSummaryView,
    GroundedExplanationView,
    PlaylistDetailView,
    PlaylistListCreateView,
)

urlpatterns = [
    path("flashcards/", FlashcardFeedView.as_view(), name="flashcard-feed"),
    path("search/", TopicSearchView.as_view(), name="flashcard-topic-search"),
    path("flashcards/<int:pk>/", FlashcardDetailView.as_view(), name="flashcard-detail"),
    path("flashcards/<int:pk>/save/", SaveFlashCardView.as_view(), name="flashcard-save"),
    path("flashcards/<int:pk>/feedback/", FlashcardFeedbackView.as_view(), name="flashcard-feedback"),
    path("flashcards/<int:pk>/understood/", FlashcardUnderstoodView.as_view(), name="flashcard-understood"),
    path("flashcards/<int:pk>/viewed/", FlashcardViewedView.as_view(), name="flashcard-viewed"),
    path("playlists/", PlaylistListCreateView.as_view(), name="playlist-list"),
    path("playlists/<int:pk>/", PlaylistDetailView.as_view(), name="playlist-detail"),
    path("progress/", UserProgressSummaryView.as_view(), name="progress-summary"),
    path("canonical-claims/<int:pk>/explain/", GroundedExplanationView.as_view(), name="grounded-explanation"),
    path("concepts/<int:pk>/mastery-status/", ConceptMasteryStatusView.as_view(), name="concept-mastery-status"),
    path("concepts/<int:pk>/questionnaires/start/", StartQuestionnaireView.as_view(), name="start-questionnaire"),
    path("questionnaires/<int:pk>/submit/", SubmitQuestionnaireView.as_view(), name="submit-questionnaire"),
    path("badges/", UserMasteryBadgesView.as_view(), name="user-badges"),
]
