from django.db import transaction
from django.utils import timezone
from knowledge.models import ExtractedClaim, Source, SourceDocument
from notes.models import Note
from verification.models import NoteProcessingJob
from verification.services.claim_extraction import ClaimExtractionService
from verification.services.ocr.factory import HybridOCRProvider

class NoteProcessingService:
    def process(self, note_id: int):
        note = Note.objects.get(id=note_id)
        job, _ = NoteProcessingJob.objects.get_or_create(note=note)

        if job.attempts >= job.max_attempts:
            return job

        job.status = NoteProcessingJob.STATUS_PROCESSING
        job.attempts += 1
        job.started_at = timezone.now()
        job.error_message = ""
        job.save(update_fields=['status', 'attempts', 'started_at', 'error_message', 'updated_at'])

        try:
            return self._process_note(note, job)
        except Exception as exc:
            job.status = NoteProcessingJob.STATUS_FAILED
            job.error_message = str(exc)
            job.failed_at = timezone.now()
            job.save(update_fields=['status', 'error_message', 'failed_at', 'updated_at'])
            note.status = Note.STATUS_FAILED
            note.processing_error = str(exc)
            note.save(update_fields=['status', 'processing_error', 'updated_at'])
            return job

    @transaction.atomic
    def _process_note(self, note: Note, job: NoteProcessingJob):
        ocr_provider = HybridOCRProvider()
        extracted_text = ocr_provider.extract_text(note.file)
        note.extracted_text = extracted_text
        note.status = Note.STATUS_OCR_DONE
        note.save(update_fields=['extracted_text', 'status', 'updated_at'])

        job.status = NoteProcessingJob.STATUS_OCR_DONE
        job.save(update_fields=['status', 'updated_at'])

        user_source, _ = Source.objects.get_or_create(
            name="User uploaded notes",
            defaults={
                "source_type": Source.SOURCE_TYPE_USER,
                "authority_score": 0.30,
            },
        )

        source_document = SourceDocument.objects.create(
            source=user_source,
            uploaded_note=note,
            title=note.title,
            document_type=SourceDocument.DOCUMENT_TYPE_NOTE,
            raw_text=extracted_text or "",
        )
        extractor = ClaimExtractionService()
        claims = extractor.extract_claims(extracted_text)

        for claim_text in claims:
            ExtractedClaim.objects.create(
                source_document=source_document,
                text=claim_text,
            )

        job.status = NoteProcessingJob.STATUS_CLAIMS_EXTRACTED
        job.completed_at = timezone.now()
        job.save(update_fields=['status', 'completed_at', 'updated_at'])

        note.status = Note.STATUS_CLAIMS_EXTRACTED
        note.save(update_fields=['status', 'updated_at'])

        return job
