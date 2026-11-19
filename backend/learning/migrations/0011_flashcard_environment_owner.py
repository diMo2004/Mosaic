# Generated for MOSAIC personal flashcard environment

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0011_unique_active_flashcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='environment',
            field=models.CharField(
                choices=[('public', 'Public'), ('personal', 'Personal')],
                db_index=True,
                default='public',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='owner',
            field=models.ForeignKey(
                blank=True,
                help_text='Owner for personal-environment flashcards; null for public cards.',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='personal_flashcards',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveConstraint(
            model_name='flashcard',
            name='unique_active_flashcard_per_canonical_claim',
        ),
        migrations.AddConstraint(
            model_name='flashcard',
            constraint=models.UniqueConstraint(
                condition=models.Q(is_active=True, source_claim__isnull=False, environment='public'),
                fields=['source_claim'],
                name='unique_active_public_flashcard_per_canonical_claim',
            ),
        ),
        migrations.AddConstraint(
            model_name='flashcard',
            constraint=models.UniqueConstraint(
                condition=models.Q(is_active=True, source_claim__isnull=False, environment='personal'),
                fields=['source_claim', 'owner'],
                name='unique_active_personal_flashcard_per_user_claim',
            ),
        ),
        migrations.AddIndex(
            model_name='flashcard',
            index=models.Index(fields=['environment', 'is_active', '-created_at'], name='flashcard_env_active_idx'),
        ),
        migrations.AddIndex(
            model_name='flashcard',
            index=models.Index(fields=['owner', 'environment', 'is_active'], name='flashcard_owner_env_idx'),
        ),
    ]
