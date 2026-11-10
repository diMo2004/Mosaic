from django.db import migrations, models


def deactivate_duplicate_active_cards(apps, schema_editor):
    """Keep the oldest active card per canonical claim; deactivate (not delete) the rest.

    Saved playlist items, feedback, and progress on the duplicates are retained.
    """
    Flashcard = apps.get_model("learning", "Flashcard")
    duplicates = (
        Flashcard.objects.filter(is_active=True, source_claim__isnull=False)
        .values("source_claim_id").annotate(n=models.Count("id")).filter(n__gt=1)
    )
    for row in duplicates:
        ids = list(
            Flashcard.objects.filter(is_active=True, source_claim_id=row["source_claim_id"])
            .order_by("id").values_list("id", flat=True)
        )
        Flashcard.objects.filter(id__in=ids[1:]).update(is_active=False)


def label_legacy_generation(apps, schema_editor):
    # Pre-existing cards cannot be classified reliably; mark fallback-shaped ones.
    Flashcard = apps.get_model("learning", "Flashcard")
    Flashcard.objects.filter(explanation="Verified from the canonical claim.").update(generation_method="fallback")



class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0009_flashcard_generation_method_and_more'),
    ]

    operations = [
        migrations.RunPython(deactivate_duplicate_active_cards, migrations.RunPython.noop),
        migrations.RunPython(label_legacy_generation, migrations.RunPython.noop),
    ]
