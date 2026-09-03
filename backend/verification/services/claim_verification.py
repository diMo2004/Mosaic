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
        extracted_claim.reviewer_notes = "Placeholder verification result."
        extracted_claim.save(
            update_field=[
                "status",
                "confidence",
                "reviewed_at",
                "reviewer_notes",
            ]
        )
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


    def _decide_status(self, evidence_items):
        supporting = [
            item for item in evidence_items
            if item.relation == Evidence.SUPPORTS
        ]

        contradicting = [
            item for item in evidence_items
            if item.relation == Evidence.CONTRADICTS
        ]

        if supporting and not contradicting:
            return ExtractedClaim.STATUS_SUPPORTED, Decimal("0.80")

        if contradicting and not supporting:
            return ExtractedClaim.STATUS_CONTRADICTED, Decimal("0.80")

        if supporting and contradicting:
            return ExtractedClaim.STATUS_PARTIALLY_SUPPORTED, Decimal("0.50")

        return ExtractedClaim.STATUS_UNCERTAIN, Decimal("0.30")

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