from django.contrib import admin

# Register your models here.
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "owner",
        "original_filename",
        "content_type",
        "file_size",
        "status",
        "updated_at",
    ]
    list_filter = [
        "content_type", 
        "status", 
        "updated_at",
        ]
    search_fields = [
        "title", 
        "owner__username", 
        "original_filename",
        "owner_email",
    ]
    readonly_fields = [
        "owner",
        "original_filename",
        "content_type",
        "file_size",
        "uploaded_at",
        "updated_at",
    ]