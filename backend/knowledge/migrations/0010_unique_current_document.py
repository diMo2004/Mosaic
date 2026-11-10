from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0009_backfill_document_versions'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='sourcedocument',
            constraint=models.UniqueConstraint(condition=models.Q(('is_current', True), models.Q(('url', ''), _negated=True)), fields=('source', 'url'), name='unique_current_document_per_source_url'),
        ),
    ]
