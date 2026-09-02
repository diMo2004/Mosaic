from rest_framework import serializers
from .models import Note

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

class NoteDetailSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "file",
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