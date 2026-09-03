from django.contrib import admin
from .models import NoteProcessingJob
# Register your models here.

@admin.register(NoteProcessingJob)
class NoteProcessingJobAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "note",
        "status",
        "error_message",
        "started_at",
        "completed_at",
        "created_at",
        "updated_at",
    ]
    list_filter = ["status", "started_at", "completed_at", "created_at"]
    search_fields = ["note__title", "error_message"]
