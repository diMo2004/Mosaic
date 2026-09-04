from rest_framework import serializers
from .models import Note
from django.conf import settings

class NoteUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "file",
            "status",
            "uploaded_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "uploaded_at",
        ]
    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_file(self, file):
        if file.size > settings.NOTE_UPLOAD_MAX_SIZE:
            raise serializers.ValidationError(f"File size must be 10MB or smaller.")

        content_type = getattr(file, 'content_type', "")

        if content_type not in settings.NOTE_UPLOAD_ALLOWED_CONTENT_TYPES:
            raise serializers.ValidationError("Unsupported file type. Allowed types are: PDF, DOC, DOCX, JPEG, PNG, TXT, WEBP, PPT, PPTX.")
        return file

class NoteDetailSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "file_url",
            "status",
            "original_filename",
            "content_type",
            "file_size",
            "extracted_text",
            "processing_error",
            "uploaded_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "original_filename",
            "content_type",
            "file_size",
            "extracted_text",
            "processing_error",
            "uploaded_at",
            "updated_at",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if not obj.file:
            return None
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url