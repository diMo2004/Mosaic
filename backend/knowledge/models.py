from django.db import models
from django.conf import settings
# Create your models here.

class Source(models.Model):
    SOURCE_TYPE_OFFICIAL = 'official'
    SOURCE_TYPE_ACADEMIC = 'academic'
    SOURCE_TYPE_EDUCATIONAL = 'educational'
    SOURCE_TYPE_COMMUNITY = 'community'
    SOURCE_TYPE_USER = 'user'
    SOURCE_TYPE_OTHER = 'other'
    SOURCE_TYPES_CHOICES = [
        (SOURCE_TYPE_OFFICIAL, 'Official'),
        (SOURCE_TYPE_ACADEMIC, 'Academic'),
        (SOURCE_TYPE_EDUCATIONAL, 'Educational'),
        (SOURCE_TYPE_COMMUNITY, 'Community'),
        (SOURCE_TYPE_USER, 'User'),
        (SOURCE_TYPE_OTHER, 'Other'),
    ]

    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, blank=True)
    source_type = models.CharField(
        max_length=30,
        choices=SOURCE_TYPES_CHOICES,
        default=SOURCE_TYPE_OTHER,
    )
    access_method = models.CharField(max_length=255, blank=True)
    source_type = models.CharField(
        max_length=30,
        choices=SOURCE_TYPES_CHOICES,
        default=SOURCE_TYPE_OTHER,
    )
    access_method = models.CharField(max_length=100, blank=True)
    license = models.CharField(max_length=255, blank=True)
    license_url = models.URLField(blank=True)
    attribution_required = models.BooleanField(default=False)
    commercial_use_allowed = models.BooleanField(default=False)
    ai_use_allowed = models.BooleanField(default=False)
    scraping_allowed = models.BooleanField(default=False)
    api_available = models.BooleanField(default=False)
    authority_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.50,
    )
    last_checked = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_sources',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Claim(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_SUPPORTED = 'supported'
    STATUS_CONTRADICTED = 'contradicted'
    STATUS_PARTIALLY_SUPPORTED = 'partially_supported'
    STATUS_UNCERTAIN = 'uncertain'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUPPORTED, 'Supported'),
        (STATUS_CONTRADICTED, 'Contradicted'),
        (STATUS_PARTIALLY_SUPPORTED, 'Partially Supported'),
        (STATUS_UNCERTAIN, 'Uncertain'),
    ]

    text = models.TextField()
    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    confidence = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
    )
    reviewer_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_claims',
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_from_note = models.ForeignKey(
        "notes.Note",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='claims',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text[:80]

class SourceDocument(models.Model):
    DOCUMENT_TYPE_NOTE = "note"
    DOCUMENT_TYPE_WEBPAGE = "web_page"
    DOCUMENT_TYPE_PDF ="pdf"
    DOCUMENT_TYPE_DOC = "doc"
    DOCUMENT_TYPE_OTHER = "other"

    DOCUMENT_TYPE_CHOICES = [
        (DOCUMENT_TYPE_NOTE, "Note"),
        (DOCUMENT_TYPE_WEBPAGE, "Web Page"),
        (DOCUMENT_TYPE_PDF, "PDF"),
        (DOCUMENT_TYPE_DOC, "DOC"),
        (DOCUMENT_TYPE_OTHER, "Other"),
    ]

    source = models.ForeignKey(
        Source,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents',
    )
    uploaded_note = models.ForeignKey(
        "notes.Note",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_documents',
    )
    title = models.CharField(max_length=255)
    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES,
        default=DOCUMENT_TYPE_OTHER,
    )
    url = models.URLField(blank=True)
    raw_text = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    retrieved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExtractedClaim(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_SUPPORTED = 'supported'
    STATUS_CONTRADICTED = 'contradicted'
    STATUS_PARTIALLY_SUPPORTED = 'partially_supported'
    STATUS_UNCERTAIN = 'uncertain'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUPPORTED, 'Supported'),
        (STATUS_CONTRADICTED, 'Contradicted'),
        (STATUS_PARTIALLY_SUPPORTED, 'Partially Supported'),
        (STATUS_UNCERTAIN, 'Uncertain'),
    ]

    source_document = models.ForeignKey(
        SourceDocument,
        on_delete=models.CASCADE,
        related_name='extracted_claims',
    )
    text = models.TextField()
    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    confidence = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
    )
    reviewed_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_extracted_claims',
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:80]

class Concept(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)    
    description = models.TextField(blank=True)
    prerequisites = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='dependent_concepts',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class CanonicalClaim(models.Model):
    concept = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        related_name='canonical_claims',
    )
    text = models.TextField()
    source_claim = models.ForeignKey(
        ExtractedClaim,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='canonical_claims',
    )
    confidence = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
    )
    is_active = models.BooleanField(default=True)
    created_by_ai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:80]

class Evidence(models.Model):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    RELATED = "related"

    RELATION_CHOICES = [
        (SUPPORTS, "Supports"),
        (CONTRADICTS, "Contradicts"),
        (RELATED, "Related"),
    ]

    claim = models.ForeignKey(
        ExtractedClaim,
        on_delete=models.CASCADE,
        related_name='evidences_items',
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name='evidence_items',
    )
    relation = models.CharField(
        max_length=30,
        choices=RELATION_CHOICES,
        default=RELATED,
    )
    url = models.URLField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    excerpt = models.TextField(blank=True)
    retrieved_at = models.DateTimeField(blank=True, null=True)
    relevance_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['relevance_score', '-created_at']

    def __str__(self):
        return f"{self.claim_id} - {self.source.name} ({self.relation})"