import hashlib
import re

from django.db import migrations, models


def _normalize_ws(text):
    return re.sub(r"\s+", " ", (text or "").strip())


def _normalize_claim(text):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", (text or "").casefold())).strip()


def backfill_hashes_and_versions(apps, schema_editor):
    """Backfill hashes and demote duplicate current documents before the unique constraint.

    The original pipeline deduplicated by (source, url) without a constraint, so
    concurrent runs may have stored duplicates. The newest stays current; older
    copies are retained (with their claims and cards) as superseded versions.
    """
    SourceDocument = apps.get_model("knowledge", "SourceDocument")
    CanonicalClaim = apps.get_model("knowledge", "CanonicalClaim")

    for document in SourceDocument.objects.exclude(raw_text="").only("id", "raw_text").iterator():
        digest = hashlib.sha256(_normalize_ws(document.raw_text).encode("utf-8")).hexdigest()
        SourceDocument.objects.filter(pk=document.pk).update(content_hash=digest)

    duplicates = (
        SourceDocument.objects.exclude(url="").exclude(source__isnull=True)
        .values("source_id", "url").annotate(n=models.Count("id")).filter(n__gt=1)
    )
    for row in duplicates:
        ids = list(
            SourceDocument.objects.filter(source_id=row["source_id"], url=row["url"])
            .order_by("-created_at", "-id").values_list("id", flat=True)
        )
        SourceDocument.objects.filter(id__in=ids[1:]).update(is_current=False, superseded_by_id=ids[0])

    for claim in CanonicalClaim.objects.only("id", "text").iterator():
        digest = hashlib.sha256(_normalize_claim(claim.text).encode("utf-8")).hexdigest()
        CanonicalClaim.objects.filter(pk=claim.pk).update(text_hash=digest)



class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0008_ingestionjob_sourcediscoverycheckpoint_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_hashes_and_versions, migrations.RunPython.noop),
    ]
