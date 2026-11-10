from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from pgvector.django import VectorField
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

    @property
    def is_ai_usable(self) -> bool:
        """Determines if content from this source can be fed to external LLMs"""
        return bool(self.ai_use_allowed or self.source_type == self.SOURCE_TYPE_USER)

    @property
    def can_redistribute(self) -> bool:
        """Determines if derived excerpts/flashcards can be shared publicly."""
        if self.source_type == self.SOURCE_TYPE_OFFICIAL:
            return True
        return bool(self.commercial_use_allowed or "cc" in (self.license or "").lower())

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

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
    # Incremental external ingestion: provider ID, normalized-content hash, and
    # version chain. A changed source creates a new current version; the old
    # version and the knowledge derived from it are retained for provenance.
    external_id = models.CharField(max_length=255, blank=True, db_index=True)
    content_hash = models.CharField(max_length=64, blank=True, db_index=True)
    is_current = models.BooleanField(default=True)
    superseded_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_versions',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['source', 'url'],
                condition=models.Q(is_current=True) & ~models.Q(url=''),
                name='unique_current_document_per_source_url',
            ),
        ]

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
    # SHA-256 of the normalized claim text; used to avoid duplicate canonical
    # claims (and cards) when several sources state the same fact.
    text_hash = models.CharField(max_length=64, blank=True, db_index=True)
    # Asynchronous flashcard generation bookkeeping (bounded retries).
    flashcard_attempts = models.PositiveSmallIntegerField(default=0)
    flashcard_error = models.TextField(blank=True)

    class Meta:
        indexes = [
            GinIndex(name='claim_text_trgm_idx', fields=['text'], opclasses=['gin_trgm_ops']),
            ]
        
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
        related_name='evidence_items',
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
    embedding = VectorField(dimensions=768, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['relevance_score', '-created_at']

    def __str__(self):
        return f"{self.claim_id} - {self.source.name} ({self.relation})"

class ConceptRelationship(models.Model):
    RELATION_PARENT = "parent"
    RELATION_RELATED = "related"
    RELATION_IMPLEMENTS = "implements"
    RELATION_BUILDS_ON = "builds_on"
    RELATION_USED_BY = "used_by"
    RELATION_ALTERNATIVE = "alternative"

    RELATION_CHOICES = [
        (RELATION_PARENT, "Parent"),
        (RELATION_RELATED, "Related"),
        (RELATION_IMPLEMENTS, "Implements"),
        (RELATION_BUILDS_ON, "Builds On"),
        (RELATION_USED_BY, "Used By"),
        (RELATION_ALTERNATIVE, "Alternative"),
    ]

    from_concept = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        related_name='outgoing_relations',
    )
    to_concept = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        related_name='incoming_relations',
    )
    relation_type = models.CharField(
        max_length=30,
        choices=RELATION_CHOICES,
        default=RELATION_RELATED,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_concept', 'to_concept', 'relation_type')
        ordering = ["from_concept__name"]

    def __str__(self):
        return f"{self.from_concept.name} --({self.relation_type})--> {self.to_concept.name}"

class UnmappedConceptReview(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Developer Review'),
        (STATUS_APPROVED, 'Approved & Added to Taxonomy'),
        (STATUS_REJECTED, 'Rejected / Not a Valid Concept'),
    ]

    suggested_name = models.CharField(max_length=255)
    context_claim = models.ForeignKey(
        "knowledge.ExtractedClaim",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unmapped_reviews',
    )
    context_text = models.TextField(help_text="Snippet of text where the term was found")
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_concepts',
    )
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review of '{self.suggested_name}' - Status: {self.status}"

class SourceDiscoveryCheckpoint(models.Model):
    """Durable discovery position for one adapter + topic query."""

    adapter = models.CharField(max_length=32)
    topic_key = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    concept = models.ForeignKey(
        Concept,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='discovery_checkpoints',
    )
    cursor = models.JSONField(default=dict, blank=True)
    exhausted = models.BooleanField(default=False)
    # Lease prevents overlapping discovery runs from paging the same query.
    lease_until = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    last_success_at = models.DateTimeField(null=True, blank=True)
    runs = models.PositiveIntegerField(default=0)
    candidates_total = models.PositiveIntegerField(default=0)
    last_candidates = models.PositiveIntegerField(default=0)
    consecutive_failures = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['adapter', 'topic']
        constraints = [
            models.UniqueConstraint(fields=['adapter', 'topic_key'], name='unique_discovery_checkpoint'),
        ]

    def __str__(self):
        return f"{self.adapter}: {self.topic}"


class IngestionJob(models.Model):
    """One discovered provider record moving through fetch -> policy -> pipeline."""

    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_RETRY = 'retry'
    STATUS_SUCCEEDED = 'succeeded'
    STATUS_UNCHANGED = 'unchanged'
    STATUS_SKIPPED = 'skipped'
    STATUS_POLICY_REJECTED = 'policy_rejected'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_RETRY, 'Waiting to retry'),
        (STATUS_SUCCEEDED, 'Succeeded'),
        (STATUS_UNCHANGED, 'Unchanged (deduplicated)'),
        (STATUS_SKIPPED, 'Skipped (insufficient content)'),
        (STATUS_POLICY_REJECTED, 'Rejected by source policy'),
        (STATUS_FAILED, 'Failed permanently'),
    ]
    CLAIMABLE_STATUSES = (STATUS_PENDING, STATUS_RETRY)
    TERMINAL_STATUSES = (STATUS_SUCCEEDED, STATUS_UNCHANGED, STATUS_SKIPPED, STATUS_POLICY_REJECTED, STATUS_FAILED)

    adapter = models.CharField(max_length=32)
    external_id = models.CharField(max_length=255)
    identifier = models.CharField(max_length=512)
    fetch_kwargs = models.JSONField(default=dict, blank=True)
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=1000, blank=True)
    topic = models.CharField(max_length=255, blank=True)
    topic_concept = models.ForeignKey(
        Concept,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingestion_jobs',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    attempts = models.PositiveSmallIntegerField(default=0)
    max_attempts = models.PositiveSmallIntegerField(default=4)
    next_attempt_at = models.DateTimeField(null=True, blank=True)
    locked_until = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    source_document = models.ForeignKey(
        SourceDocument,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ingestion_jobs',
    )
    result = models.JSONField(default=dict, blank=True)
    discovered_at = models.DateTimeField(auto_now_add=True)
    enqueued_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-discovered_at']
        constraints = [
            models.UniqueConstraint(fields=['adapter', 'external_id'], name='unique_ingestion_job_per_record'),
        ]
        indexes = [
            models.Index(fields=['status', 'next_attempt_at']),
            models.Index(fields=['adapter', 'status']),
        ]

    def __str__(self):
        return f"{self.adapter}:{self.external_id} ({self.status})"
