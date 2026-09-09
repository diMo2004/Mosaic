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
        evidence_items = list(extracted_claim.evidence_items.select_related("source").all())

        if not evidence_items:
            evidence_items = self.evidence_retriever.retrieve_for_claim(extracted_claim)

        status, confidence, notes = self._decide_status(evidence_items)

        extracted_claim.status = status
        extracted_claim.confidence = confidence
        extracted_claim.reviewed_at = timezone.now()
        extracted_claim.reviewed_notes = notes
        extracted_claim.save(
            update_fields=[
                "status",
                "confidence",
                "reviewed_at",
                "reviewed_notes",
            ]
        )
        canonical_claim = None
        if status == ExtractedClaim.STATUS_SUPPORTED:
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

    def _score_evidence(self, evidence_items, relation):
        matching = [
            item for item in evidence_items
            if item.relation == relation
        ]

        if not matching:
            return Decimal("0.0"), 0

        weights = []
        for item in matching:
            authority = item.source.authority_score or Decimal("0.50")
            relevance = item.relevance_score or Decimal("0.50")
            weights.append(authority * relevance)

        weights.sort(reverse=True)
        primary_weight = weights[0]
        corroboration_bonus = Decimal("0.00")
        for w in weights[1:]:
            corroboration_bonus += (Decimal("1.00") - (primary_weight + corroboration_bonus)) * Decimal("0.20") * w

        total_strength = min(primary_weight + corroboration_bonus, Decimal("0.99"))
        return total_strength.quantize(Decimal("0.01")), len(matching)


    def _decide_status(self, evidence_items):
        supporting_strength, supporting_count = self._score_evidence(evidence_items, Evidence.SUPPORTS)
        contradicting_strength, contradicting_count = self._score_evidence(evidence_items, Evidence.CONTRADICTS)

        notes = (
            f"Evidence analysis: {supporting_count} supporting (strength {supporting_strength}), "
            f"{contradicting_count} contradicting (strength {contradicting_strength})."
        )
        if supporting_count == 0 and contradicting_count == 0:
            return ExtractedClaim.STATUS_UNCERTAIN, Decimal("0.00"), notes
        is_clear_support = (
            supporting_strength >= Decimal("0.65") and (
                contradicting_count == 0
                or contradicting_strength < Decimal("0.35")
                or (
                    supporting_count >= 2
                    and supporting_count >= 2 * contradicting_count
                    and supporting_strength >= contradicting_strength + Decimal("0.25")
                )
            )
        )
        if is_clear_support:
            net_confidence = supporting_strength - (contradicting_strength * Decimal("0.40"))
            if supporting_count == 1:
                net_confidence = min(net_confidence, Decimal("0.85"))
            return ExtractedClaim.STATUS_SUPPORTED, max(net_confidence, Decimal("0.50")).quantize(Decimal("0.01")), notes
        is_clear_contradiction = (
            contradicting_strength >= Decimal("0.65") and (
                supporting_count == 0
                or supporting_strength < Decimal("0.35")
                or (
                    contradicting_count >= 2
                    and contradicting_count >= 2 * supporting_count
                    and contradicting_strength >= supporting_strength + Decimal("0.25")
                )
            )
        )
        if is_clear_contradiction:
            net_confidence = contradicting_strength - (supporting_strength * Decimal("0.40"))
            if contradicting_count == 1:
                net_confidence = min(net_confidence, Decimal("0.85"))
            return ExtractedClaim.STATUS_CONTRADICTED, max(net_confidence, Decimal("0.50")).quantize(Decimal("0.01")), notes

        if supporting_strength >= Decimal("0.40") and contradicting_strength >= Decimal("0.40"):
            conflict_diff = abs(supporting_strength - contradicting_strength)
            return ExtractedClaim.STATUS_PARTIALLY_SUPPORTED, max(conflict_diff, Decimal("0.30")).quantize(Decimal("0.01")), notes

        max_strength = max(supporting_strength, contradicting_strength, Decimal("0.10"))
        return ExtractedClaim.STATUS_UNCERTAIN, max_strength.quantize(Decimal("0.01")), notes

    def create_canonical_claim(self, extracted_claim: ExtractedClaim, confidence):
        from verification.services.concept_assignment import ConceptAssignmentService
        assignment_service = ConceptAssignmentService()
        concept, _ = assignment_service.assign_concept(
            claim_text=extracted_claim.text,
            source_claim=extracted_claim,
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