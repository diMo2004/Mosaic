from django.utils import timezone
from knowledge.models import ExtractedClaim, Source, SourceDocument
from notes.models import Note
from .models import NoteProcessingJob

def process_note_placeholder(note_id):
    note = Note.objects.get(id=note_id)
    job, _ = NoteProcessingJob.objects.get_or_create(note=note)
    job.status = NoteProcessingJob.STATUS_PROCESSING
    job.started_at = timezone.now()
    job.save(update_fields=['status', 'started_at', 'updated_at'])

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
        raw_text=note.extracted_text or "",
    )

    job.status = NoteProcessingJob.STATUS_OCR_DONE
    job.save(update_fields=['status', 'updated_at'])

    ExtractedClaim.objects.create(
        source_document=source_document,
        text="This is a placeholder claim extracted from the note.",
    )

    job.status = NoteProcessingJob.STATUS_CLAIMS_EXTRACTED
    job.save(update_fields=['status', 'updated_at'])

    note.status = Note.STATUS_CLAIMS_EXTRACTED
    note.save(update_fields=['status', 'updated_at'])

    job.completed_at = timezone.now()
    job.save(update_fields=['completed_at', 'updated_at'])

    return job