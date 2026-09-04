from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from knowledge.models import CanonicalClaim, ExtractedClaim, Concept, Evidence
from .evidence_retrieval import EvidenceRetrievalService
from learning.services import FlashcardGenerationService

class ClaimVerificationService:
    def __init__(self):
        self.evidence_retriever = EvidenceRetrievalService()

    @transaction.atomic
    def verify_claim(self, extracted_claim: ExtractedClaim):
        evidence_items = list(extracted_claim.evidence_items.all())

        if not evidence_items:
            evidence_items = self.evidence_retriever.retrieve_for_claim(extracted_claim)

        status, confidence = self._decide_status(evidence_items)

        extracted_claim.status = status
        extracted_claim.confidence = confidence
        extracted_claim.reviewed_at = timezone.now()
        extracted_claim.reviewed_notes = "Placeholder verification result."
        extracted_claim.save(
            update_fields=[
                "status",
                "confidence",
                "reviewed_at",
                "reviewed_notes",
            ]
        )
        canonical_claim = None
        if status != ExtractedClaim.STATUS_CONTRADICTED:
            canonical_claim = self.create_canonical_claim(extracted_claim, confidence)

        flashcard = None
        if canonical_claim:
            flashcard = FlashcardGenerationService().generate_from_canonical_claim(
                canonical_claim
            )

        return {
            "claim": extracted_claim,
            "canonical_claim": canonical_claim,
            "evidence": evidence_items,
            "flashcard": flashcard,
        }

    def _score_evidence(self, evidence_items,relation):
        matching = [
            item for item in evidence_items
            if item.relation == relation
        ]

        if not matching:
            return Decimal("0.0")

        total = Decimal("0.00")

        for item in matching:
            authority = item.source.authority_score or Decimal("0.50")
            relevance = item.relevance_score or Decimal("0.50")
            total += authority * relevance

        average = total / len(matching)

        if len(matching) >= 2:
            average += Decimal("0.10")

        return min(average, Decimal("0.95"))


    def _decide_status(self, evidence_items):
        supporting_score = self._score_evidence(evidence_items, Evidence.SUPPORTS)
        contradicting_score = self._score_evidence(evidence_items, Evidence.CONTRADICTS)

        if supporting_score > Decimal("0.65") and contradicting_score < Decimal("0.40"):
            return ExtractedClaim.STATUS_SUPPORTED, supporting_score

        if contradicting_score > Decimal("0.65") and supporting_score < Decimal("0.40"):
            return ExtractedClaim.STATUS_CONTRADICTED, contradicting_score

        if supporting_score > Decimal("0.40") and contradicting_score > Decimal("0.40"):
            return ExtractedClaim.STATUS_PARTIALLY_SUPPORTED, max(supporting_score, contradicting_score)

        return ExtractedClaim.STATUS_UNCERTAIN, max(supporting_score, contradicting_score, Decimal("0.30"))

    def create_canonical_claim(self, extracted_claim: ExtractedClaim, confidence):
        concept, _ = Concept.objects.get_or_create(
            name="General Knowledge",
            defaults={
                "slug": "general-knowledge",
                "description": "Temporary concept bucket for early MVP claims.",
            },
        )

        canonical_claim, _ = CanonicalClaim.objects.get_or_create(
            source_claim = extracted_claim,
            defaults={
                "concept": concept,
                "text": extracted_claim.text,
                "confidence": confidence,
                "is_active": True,
                "created_by_ai": False,
            },
        )
        return canonical_claim