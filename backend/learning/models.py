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

class SavedFlashcard(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_flashcards',
    )
    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name='saved_by_users',
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'flashcard')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.user_id} saved {self.flashcard_id}"

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