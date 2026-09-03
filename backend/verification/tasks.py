from django.utils import timezone
from knowledge.models import ExtractedClaim, Source, SourceDocument
from notes.models import Note
from .models import NoteProcessingJob
from .services.note_processing import NoteProcessingService

def process_note_placeholder(note_id):
    service = NoteProcessingService()
    return service.process(note_id)