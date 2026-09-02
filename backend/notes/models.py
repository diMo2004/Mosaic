from django.db import models

# Create your models here.
from django.conf import settings

class Note(models.Model):
    STATUS_UPLOADED = "uploaded"
    STATUS_PROCESSING = "processing"
    STATUS_OCR_DONE = "ocr_done"
    STATUS_CLAIMS_EXTRACTED = "claims_extracted"
    STATUS_VERIFIED = "verified"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_UPLOADED, "Uploaded"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_OCR_DONE, "OCR Done"),
        (STATUS_CLAIMS_EXTRACTED, "Claims Extracted"),
        (STATUS_VERIFIED, "Verified"),
        (STATUS_FAILED, "Failed"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    file = models.FileField(upload_to='notes/')
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=30, 
        choices=STATUS_CHOICES, 
        default=STATUS_UPLOADED,
        )
    original_filename = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    extracted_text = models.TextField(blank=True)
    processing_error = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title