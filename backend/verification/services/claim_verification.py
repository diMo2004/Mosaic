import json
import logging
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from google import genai
from google.genai import types
from knowledge.models import CanonicalClaim, ExtractedClaim, Concept, Evidence
from .evidence_retrieval import EvidenceRetrievalService
from learning.services.flashcard_service import FlashcardGenerationService

logger = logging.getLogger(__name__)
class ClaimVerificationService:
    def __init__(self):
        self.evidence_retriever = EvidenceRetrievalService()

    @transaction.atomic
    def verify_claim(self, extracted_claim: ExtractedClaim):
        evidence_items = list(extracted_claim.evidence_items.select_related("source").all())

        if not evidence_items:
            evidence_items = self.evidence_retriever.retrieve_for_claim(extracted_claim)

        status, confidence, notes = self._decide_status(evidence_items)

        corrected_canonical_text = extracted_claim.text
        if status in (ExtractedClaim.STATUS_UNCERTAIN, ExtractedClaim.STATUS_PARTIALLY_SUPPORTED):
            llm_result = self._verify_with_gemini(extracted_claim.text)
            if llm_result.get("status") == ExtractedClaim.STATUS_SUPPORTED:
                status = ExtractedClaim.STATUS_SUPPORTED
                confidence = llm_result.get("confidence", confidence)
                notes = f"LLM Fact-Check: {llm_result.get('notes', '')}"
                corrected_canonical_text = llm_result.get("corrected_text", extracted_claim.text)
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

    def _verify_with_gemini(self, claim_text: str) -> dict:
        api_key = getattr(settings, "GEMINI_API_KEY", "")
        if not api_key:
            return {"status": ExtractedClaim.STATUS_UNCERTAIN}
        client = genai.Client(api_key=api_key)
        prompt = f"""You are a Computer Science expert fact-checker. Evaluate this statement extracted from university notes:
Statement: "{claim_text}"
1. Is this claim factually and technically correct in Computer Science?
2. If true, status is "SUPPORTED". If factually wrong, "CONTRADICTED".
3. Provide the clean, precise canonical form of this statement in "corrected_text".
4. Assign a confidence score from 0.00 to 1.00.
Output strict JSON:
{{
  "status": "SUPPORTED",
  "confidence": 0.95,
  "corrected_text": "...",
  "explanation": "..."
}}
"""
        try:
            response = client.models.generate_content(
                model=getattr(settings, "GEMINI_CLAIM_MODEL", "gemini-3.8-flash"),
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1),
            )
            data = json.loads(response.text)
            return {
                "status": ExtractedClaim.STATUS_SUPPORTED if data.get("status") == "SUPPORTED" else ExtractedClaim.STATUS_CONTRADICTED,
                "confidence": Decimal(str(min(max(float(data.get("confidence", 0.85)), 0.0), 1.0))).quantize(Decimal("0.01")),
                "corrected_text": data.get("corrected_text", claim_text),
                "notes": data.get("explanation", ""),
            }
        except Exception as e:
            logger.warning("Gemini claim verification failed: %s", e)
            return {"status": ExtractedClaim.STATUS_UNCERTAIN}

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

    def create_canonical_claim(self, extracted_claim: ExtractedClaim, confidence, text_override=None):
        from verification.services.concept_assignment import ConceptAssignmentService
        assignment_service = ConceptAssignmentService()
        concept = assignment_service.assign_concept(
            claim_text=text_override or extracted_claim.text,
            source_claim=extracted_claim,
        )
        canonical_claim, _ = CanonicalClaim.objects.get_or_create(
            source_claim=extracted_claim,
            defaults={
                "concept": concept,
                "text": text_override or extracted_claim.text,
                "confidence": confidence,
                "is_active": True,
                "created_by_ai": False,
            },
        )
        return canonical_claim

  