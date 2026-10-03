from django.db import models

# Create your models here.
from django.conf import settings

class Flashcard(models.Model):
    DIFFICULTY_BEGINNER = 'beginner'
    DIFFICULTY_INTERMEDIATE = 'intermediate'
    DIFFICULTY_ADVANCED = 'advanced'

    DIFFICULTY_CHOICES = [
        (DIFFICULTY_BEGINNER, 'Beginner'),
        (DIFFICULTY_INTERMEDIATE, 'Intermediate'),
        (DIFFICULTY_ADVANCED, 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    prompt = models.TextField()
    answer = models.TextField()
    explanation = models.TextField(blank=True)
    source_claim = models.ForeignKey(
        'knowledge.CanonicalClaim',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flashcards',
    )
    difficulty = models.CharField(
        max_length=30,
        choices=DIFFICULTY_CHOICES,
        default=DIFFICULTY_BEGINNER,
    )
    is_active = models.BooleanField(default=True)
    created_by_ai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='playlists',
    )
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_default_playlist_per_user',
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.user_id})"

    @classmethod
    def get_default_for_user(cls, user):
        playlist, _ = cls.objects.get_or_create(
            user=user,
            is_default=True,
            defaults={'name': 'Saved'},
        )
        return playlist
    
class PlaylistItem(models.Model):
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='items',
    )
    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name='playlist_items',
    )
    added_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('playlist', 'flashcard')
        ordering = ['position','added_at']

    def __str__(self):
        return f"{self.flashcard_id} in {self.playlist_id}"

class FlashcardFeedback(models.Model):
    FEEDBACK_LIKE = 'like'
    FEEDBACK_DISLIKE = 'dislike'
    FEEDBACK_CONFUSING = 'confusing'
    FEEDBACK_INCORRECT = 'incorrect'
    FEEDBACK_TOO_EASY = 'too_easy'
    FEEDBACK_TOO_HARD = 'too_hard'

    FEEDBACK_CHOICES = [
        (FEEDBACK_LIKE, 'Like'),
        (FEEDBACK_DISLIKE, 'Dislike'),
        (FEEDBACK_CONFUSING, 'Confusing'),
        (FEEDBACK_INCORRECT, 'Incorrect'),
        (FEEDBACK_TOO_EASY, 'Too Easy'),
        (FEEDBACK_TOO_HARD, 'Too Hard'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='flashcard_feedbacks',
    )
    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name='feedback_items',
    )
    feedback_type = models.CharField(
        max_length=30,
        choices=FEEDBACK_CHOICES,
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.feedback_type} on {self.flashcard_id}"

class UserProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_items',
    )
    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name='progress_items',
    )
    view_count = models.PositiveIntegerField(default=0)
    last_viewed_at = models.DateTimeField(null=True, blank=True)
    understood = models.BooleanField(default=False)
    understood_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'flashcard')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.user_id} progress on {self.flashcard_id}"

class Questionnaire(models.Model):
    TIER_EASY = 1
    TIER_MODERATE = 2
    TIER_INTERMEDIATE = 3
    TIER_ADVANCED = 4
    TIER_EXPERT = 5

    TIER_CHOICES = [
        (TIER_EASY, 'Easy'),
        (TIER_MODERATE, 'Moderate'),
        (TIER_INTERMEDIATE, 'Intermediate'),
        (TIER_ADVANCED, 'Advanced'),
        (TIER_EXPERT, 'Expert'),
    ]

    STATUS_IN_PROGRESS = "in_progress"
    STATUS_PASSED = "passed"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_PASSED, "Passed"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questionnaires',
    )
    concept = models.ForeignKey(
        'knowledge.Concept',
        on_delete=models.CASCADE,
        related_name='questionnaires',
    )
    tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_IN_PROGRESS,
    )
    score = models.PositiveSmallIntegerField(default=0)
    passing_threshold = models.PositiveSmallIntegerField(default=8)
    created_at = models.DateField(auto_now_add=True)
    completed_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.concept.name} Tier {self.tier} ({self.status})"

class QuestionnaireQuestion(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="questionnaire_questions",
    )
    prompt = models.TextField()
    options = models.JSONField(help_text="List of 4 string options")
    correct_option_index = models.PositiveSmallIntegerField(help_text="Index 0-3 of the correct option")
    explanation = models.TextField(blank=True)
    user_selected_index = models.PositiveSmallIntegerField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Q for {self.questionnaire_id}: {self.prompt[:50]}"

class MasteryBadge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mastery_badges',
    )
    concept = models.ForeignKey(
        'knowledge.Concept',
        on_delete=models.CASCADE,
        related_name='mastery_badges',
    )
    is_superset = models.BooleanField(default=False)
    completion_date = models.DateTimeField(auto_now_add=True)
    difficult_progression = models.JSONField(
        default=dict,
        help_text="Log of completed tiers, scores, and dates",
    )

    class Meta:
        unique_together = ('user', 'concept')
        ordering = ['-completion_date']

    def __str__(self):
        badge_type = "Superset Badge" if self.is_superset else "Mastery Badge"
        return f"{badge_type}: {self.concept.name} for {self.user.username}"