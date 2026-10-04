from django.shortcuts import render
from django.db import transaction

# Create your views here.
from rest_framework import generics, permissions
from .models import Note
from verification.models import NoteProcessingJob
from verification.tasks import process_note_task
from .serializers import NoteDetailSerializer, NoteUploadSerializer
from .permissions import CanViewOwnNotes
from users.permissions import IsProfileComplete

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
        transaction.on_commit(lambda: process_note_task.delay(note.id))
class NoteListView(generics.ListAPIView):
    serializer_class = NoteDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete, CanViewOwnNotes]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

class NoteDetailView(generics.RetrieveAPIView):
    serializer_class = NoteDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete, CanViewOwnNotes]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)