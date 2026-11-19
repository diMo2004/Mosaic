from django.shortcuts import get_object_or_404
from django.db import transaction

# Create your views here.
from rest_framework import generics, permissions
from .models import Note
from verification.models import NoteProcessingJob
from verification.tasks import process_note_task
from .serializers import NoteDetailSerializer, NoteUploadSerializer
from users.permissions import IsProfileComplete
from verification.services.note_processing import NoteProcessingService
from knowledge.models import ExtractedClaim
from knowledge.serializers import ExtractedClaimSerializer
from django import db
from django.conf import settings
import logging
import threading

logger = logging.getLogger(__name__)


def _process_note_in_background(note_id):
    try:
        NoteProcessingService().process(note_id)
    except Exception:
        logger.exception("Background processing failed for note %s", note_id)
    finally:
        db.connections.close_all()


def process_note_in_thread(note_id):
    # Processing calls Gemini and can take minutes, far past gunicorn's request
    # timeout, so it must never run on the request thread.
    threading.Thread(
        target=_process_note_in_background,
        args=(note_id,),
        name=f"note-processing-{note_id}",
        daemon=True,
    ).start()


def enqueue_note_processing(note_id):
    if settings.CELERY_TASK_ALWAYS_EAGER:
        process_note_in_thread(note_id)
        return
    try:
        process_note_task.apply_async(args=[note_id], retry=False)
    except Exception:
        # Production may not have a Celery broker/worker configured yet. Do not
        # turn a successfully stored upload into HTTP 500 or a request timeout.
        logger.exception(
            "Could not enqueue note %s; processing it in a background thread instead",
            note_id,
        )
        process_note_in_thread(note_id)

class NoteUploadView(generics.CreateAPIView):
    serializer_class = NoteUploadSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get('file')
        note = serializer.save(
            owner=self.request.user,
            original_filename=getattr(uploaded_file, 'name', ''),
            content_type=getattr(uploaded_file, 'content_type', ''),
            file_size=getattr(uploaded_file, 'size', 0),
            status = Note.STATUS_UPLOADED,
        )

        NoteProcessingJob.objects.get_or_create(note=note)
        transaction.on_commit(lambda: enqueue_note_processing(note.id))
class NoteListView(generics.ListAPIView):
    serializer_class = NoteDetailSerializer
    # Public to profile-complete users until premium access starts; data stays owner-scoped.
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

class NoteDetailView(generics.RetrieveAPIView):
    serializer_class = NoteDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteClaimsView(generics.ListAPIView):
    """List claims extracted from one of the signed-in user's notes."""
    serializer_class = ExtractedClaimSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        note = get_object_or_404(
            Note.objects.filter(owner=self.request.user),
            pk=self.kwargs['pk'],
        )
        return ExtractedClaim.objects.filter(
            source_document__uploaded_note=note,
        ).select_related('source_document', 'reviewed_by')
