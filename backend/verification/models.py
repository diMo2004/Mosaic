from django.db import models

# Create your models here.
class NoteProcessingJob(models.Model):
    STATUS_UPLOADED = 'uploaded'
    STATUS_PROCESSING = 'processing'
    STATUS_OCR_DONE = 'ocr_done'
    STATUS_CLAIMS_EXTRACTED = 'claims_extracted'
    STATUS_VERIFIED = 'verified'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_UPLOADED, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_OCR_DONE, 'OCR Done'),
        (STATUS_CLAIMS_EXTRACTED, 'Claims Extracted'),
        (STATUS_VERIFIED, 'Verified'),
        (STATUS_FAILED, 'Failed'),
    ]

    note = models.OneToOneField(
        "notes.Note",
        on_delete=models.CASCADE,
        related_name='processing_job',
    )
    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default=STATUS_UPLOADED,
    )
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Processing Job for Note {self.note.id} - Status: {self.status}"