from django.urls import path
from .views import NoteDetailView, NoteListView, NoteUploadView

urlpatterns = [
    path("upload/", NoteUploadView.as_view(), name="note-upload"),
    path("", NoteListView.as_view(), name="note-list"),
    path("<int:pk>/", NoteDetailView.as_view(), name="note-detail"),
]