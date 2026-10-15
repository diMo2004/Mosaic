from django.shortcuts import render
from django.db import transaction

# Create your views here.
from rest_framework import generics, permissions
from .models import Note
from verification.models import NoteProcessingJob
from verification.tasks import process_note_task
from .serializers import NoteDetailSerializer, NoteUploadSerializer
from users.permissions import IsProfileComplete
from verification.services.note_processing import NoteProcessingService
import logging

logger = logging.getLogger(__name__)


def enqueue_note_processing(note_id):
    try:
        process_note_task.delay(note_id)
    except Exception:
        # Production may not have a Celery broker/worker configured yet. Do not
        # turn a successfully stored upload into HTTP 500; process it inline.
        logger.exception(
            "Could not enqueue note %s; processing it synchronously instead",
            note_id,
        )
        NoteProcessingService().process(note_id)

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
