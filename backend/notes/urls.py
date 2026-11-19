from django.urls import path
from .views import NoteClaimsView, NoteDetailView, NoteListView, NoteUploadView

urlpatterns = [
    path("upload/", NoteUploadView.as_view(), name="note-upload"),
    path("<int:pk>/claims/", NoteClaimsView.as_view(), name="note-claims"),
    path("", NoteListView.as_view(), name="note-list"),
    path("<int:pk>/", NoteDetailView.as_view(), name="note-detail"),
]
