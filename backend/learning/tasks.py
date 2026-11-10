import logging
import random
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.db import close_old_connections
from django.db.models import F
from django.utils import timezone

from knowledge.models import CanonicalClaim
from learning.services.flashcard_service import FlashcardGenerationService

logger = logging.getLogger(__name__)


def _max_attempts() -> int:
    return int(getattr(settings, "FLASHCARD_GENERATION_MAX_ATTEMPTS", 4))


@shared_task(
    bind=True,
    name="learning.generate_flashcard_for_claim",
    max_retries=3,
    acks_late=True,
    ignore_result=True,
)
def generate_flashcard_for_claim_task(self, canonical_claim_id: int) -> dict:
    """Generate (idempotently) the flashcard for a verified canonical claim."""
    close_old_connections()
    claim = CanonicalClaim.objects.select_related("concept").filter(pk=canonical_claim_id, is_active=True).first()
    if claim is None:
        return {"status": "missing", "canonical_claim_id": canonical_claim_id}
    if claim.flashcards.exists():
        return {"status": "exists", "canonical_claim_id": canonical_claim_id}
    if claim.flashcard_attempts >= _max_attempts():
        logger.error("flashcard.generation.exhausted canonical_claim=%s error=%s", claim.id, claim.flashcard_error[:200])
        return {"status": "exhausted", "canonical_claim_id": canonical_claim_id}

    CanonicalClaim.objects.filter(pk=claim.pk).update(flashcard_attempts=F("flashcard_attempts") + 1)
    try:
        flashcard = FlashcardGenerationService().generate_from_canonical_claim(claim)
    except Exception as exc:
        CanonicalClaim.objects.filter(pk=claim.pk).update(flashcard_error=f"{type(exc).__name__}: {exc}"[:2000])
        logger.warning("flashcard.generation.failed canonical_claim=%s retry=%s", claim.id, self.request.retries, exc_info=True)
        if self.request.retries < self.max_retries:
            countdown = min(60 * (2 ** self.request.retries), 900) + random.uniform(0, 30)
            raise self.retry(exc=exc, countdown=countdown)
        return {"status": "failed", "canonical_claim_id": canonical_claim_id}

    CanonicalClaim.objects.filter(pk=claim.pk).update(flashcard_error="")
    logger.info(
        "flashcard.generation.persisted canonical_claim=%s flashcard=%s method=%s",
        claim.id, flashcard.id, flashcard.generation_method,
    )
    return {"status": "created", "canonical_claim_id": canonical_claim_id, "flashcard_id": flashcard.id}


@shared_task(name="learning.backfill_missing_flashcards", ignore_result=True)
def backfill_missing_flashcards_task(limit: int | None = None) -> dict:
    """Re-dispatch generation for supported claims whose card task was lost or failed.

    Claims younger than a grace period are skipped so the on-commit dispatch from
    verification normally wins; attempts are bounded per claim.
    """
    close_old_connections()
    limit = limit or int(getattr(settings, "FLASHCARD_BACKFILL_BATCH_SIZE", 50))
    grace = timezone.now() - timedelta(minutes=int(getattr(settings, "FLASHCARD_BACKFILL_GRACE_MINUTES", 5)))
    claim_ids = list(
        CanonicalClaim.objects.filter(
            is_active=True,
            flashcards__isnull=True,
            flashcard_attempts__lt=_max_attempts(),
            created_at__lt=grace,
        )
        .order_by("created_at")
        .values_list("id", flat=True)[:limit]
    )
    for claim_id in claim_ids:
        generate_flashcard_for_claim_task.delay(claim_id)
    if claim_ids:
        logger.info("flashcard.backfill.dispatched count=%s", len(claim_ids))
    return {"dispatched": len(claim_ids)}
