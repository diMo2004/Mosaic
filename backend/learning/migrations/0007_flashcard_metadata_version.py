from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0006_flashcard_card_type_flashcard_key_points_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="flashcard",
            name="card_metadata_version",
            field=models.PositiveSmallIntegerField(default=0, editable=False),
        ),
    ]
