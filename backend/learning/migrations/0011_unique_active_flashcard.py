from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0010_deduplicate_active_flashcards'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='flashcard',
            constraint=models.UniqueConstraint(condition=models.Q(('is_active', True), ('source_claim__isnull', False)), fields=('source_claim',), name='unique_active_flashcard_per_canonical_claim'),
        ),
    ]
