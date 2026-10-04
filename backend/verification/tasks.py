from django.utils import timezone
from knowledge.models import ExtractedClaim, Source, SourceDocument
from notes.models import Note
from .models import NoteProcessingJob
from .services.note_processing import NoteProcessingService
import logging
from celery import shared_task
from django.db import close_old_connections

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    name="verification.process_note",
    max_retries=3,
    acks_late=True,
)
def process_note_task(self, note_id: int):
    """
    Asynchronously processes an uploaded note through OCR, claim extraction,
    and verification using production retry backoff.
    """
    close_old_connections()
    logger.info("Starting processing task for note_id=%s (attempt %s/3)", note_id, self.request.retries + 1)
    service = NoteProcessingService()
    try:
        job = service.process(note_id)
        if job.status == NoteProcessingJob.STATUS_FAILED:
            raise RuntimeError(f"Note processing failed for note_id={note_id}: {job.error_message}")
        return {
            "status": job.status,
            "note_id": note_id,
            "job_id": job.id,
        }
    except Exception as e:
        retry_count = self.request.retries + 1
        logger.warning(
            "Note processing encountered an error for note_id=%s (retry %s/3): %s",
            note_id,
            retry_count,
            e,
            exc_info=True,
        )
        if self.request.retries < self.max_retries:
            countdown = 60 * (2 ** self.request.retries)  # Exponential backoff: 60s, 120s, 240s
            raise self.retry(exc=e, countdown=countdown)

        logger.error("All retries exhausted for note_id=%s. Marking as permanently failed.", note_id)
        return {
            "status": "failed",
            "note_id": note_id,
            "error": str(e),
        }