from django.db import models
from django.conf import settings
# Create your models here.

class UserProfile(models.Model):
    AUTH_PROVIDER_DJANGO = 'django'
    AUTH_PROVIDER_GOOGLE = 'google'

    AUTH_PROVIDER_CHOICES = [
        (AUTH_PROVIDER_DJANGO, 'Django'),
        (AUTH_PROVIDER_GOOGLE, 'Google'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDER_CHOICES,
        default=AUTH_PROVIDER_DJANGO,
    )

    full_name = models.CharField(max_length=255, blank=True)
    education_level = models.CharField(max_length=255, blank=True)
    learning_goal = models.CharField(max_length=255, blank=True)
    interests = models.JSONField(default=list, blank=True)
    profile_completed = models.BooleanField(default=False)
    google_picture_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    can_view_own_notes = models.BooleanField(default=False)

    def missing_required_fields(self):
        fields = []
        if not self.full_name:
            fields.append("full_name")
        if not self.education_level:
            fields.append("education_level")
        if not self.learning_goal:
            fields.append("learning_goal")
        return fields

    def update_completion_status(self):
        self.profile_completed = not self.missing_required_fields()
        self.save(update_fields=['profile_completed','updated_at'])