import json
import os
import logging
import re
from typing import Any
from django.conf import settings
from google import genai
from knowledge.models import Evidence, CanonicalClaim
from knowledge.services.evidence_retrieval import EvidenceRetrievalService, EvidenceRetrievalError
from pgvector.django import CosineDistance

logger = logging.getLogger(__name__)

CITATION_PATTERN = re.compile(r"\[(\d+)\]")

class RAGExplanationServiceError(RuntimeError):
    """Raised when RAG explanation generation fails."""

class RAGExplanationService:
    def __init__(
            self,
            *,
            evidence_retriever: EvidenceRetrievalService | None = None,
            client: Any | None = None,
            ):
        api_key = getattr(settings, "GEMINI_API_KEY", "",) or os.getenv("GEMINI_API_KEY", "")
        if not api_key and client is None:
            raise RAGExplanationServiceError("GEMINI_API_KEY is not set in settings or environment variables.")
        self.client = client or genai.Client(api_key=api_key)
        self.model_name = getattr(settings, "GEMINI_CLAIM_MODEL", "gemini-3.6-flash")
        self.evidence_retriever = evidence_retriever or EvidenceRetrievalService()

    def generate_explanation(self, canonical_claim: CanonicalClaim, *, top_k: int = 4) -> dict[str, Any]:
        if not canonical_claim or not canonical_claim.text.strip():
            raise RAGExplanationServiceError("Canonical claim must have non-empty text.")
        evidence_items = self._retrieve_evidence(
            canonical_claim,
            top_k=top_k,
        )
        if not evidence_items:
            raise RAGExplanationServiceError(
                f"No evidence found for canonical claim ID {canonical_claim.id}."
            )

        prompt = self._build_prompt(
            canonical_claim,
            evidence_items,
        )
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
        except Exception as e:
            logger.exception(
                "RAG explanation generation failed for canonical claim ID %s.",
                canonical_claim.pk,
            )
            raise RAGExplanationServiceError(
                "The explanation provider request failed."
            ) from e
        explanation_text = getattr(response, "text", None)

        if not explanation_text or not explanation_text.strip():
            raise RAGExplanationServiceError(
                "RAG explanation provider returned no text."
            )

        explanation_text = explanation_text.strip()
        self._validate_citations(
            explanation_text,
            evidence_count=len(evidence_items),
        )

        return {
            "explanation": explanation_text,
            "evidence": evidence_items,
        }

    def _retrieve_evidence(
            self,
            canonical_claim: CanonicalClaim,
            *,
            top_k: int,
    ) -> list[Evidence]:
        try:
            evidence_items = self.evidence_retriever.retrieve(
                canonical_claim.text,
                top_k=top_k,
            )
        except EvidenceRetrievalError as e:
            logger.exception(
                "Evidence retrieval failed for canonical claim ID %s.",
                canonical_claim.pk,
            )
            raise RAGExplanationServiceError(
                "Evidence retrieval failed."
            ) from e

        if evidence_items:
            return evidence_items

        if not canonical_claim.source_claim_id:
            return []

        return list(
            canonical_claim.source_claim.evidence_items
            .filter(excerpt__isnull=False)
            .exclude(excerpt="")
            .select_related("source")
            .order_by("-relevance_score", "-created_at")[:top_k]
        )

    def _build_prompt(
            self,
            canonical_claim: CanonicalClaim,
            evidence_items: list[Evidence],
    ) -> str:
        evidence_context = []

        for citation_number, evidence in enumerate(evidence_items, start=1):
            source_name = (
                evidence.source.name 
                if evidence.source_id
                else "Unknown Source"
            )
            evidence_context.append(
                "\n".join(
                    [
                        f"Evidence [{citation_number}]",
                        f"Source: {source_name}",
                        f"Title: {evidence.title or 'No Title'}",
                        f"URL: {evidence.url or 'No URL'}",
                        f"Excerpt: {evidence.excerpt or 'No Excerpt'}",
                    ]
                )
            )
        return f"""
Tou are a computer science educator.

Explain the following canonical claim clearly for a computer science student.

Concept: {canonical_claim.concept.name}
Canonical Claim: "{canonical_claim.text}"
Use only the evidence supplied below.
Do not introduce facts that are not supported by the evidence.
Every factual statement based on evidence must include one or more
citations using the exact form [1], [2], and so on.
Use only the citation numbers that exist in the supplied evidence.
Do not invent sources or citation numbers.
If the evidence is insufficient, say exactly that the evidence is insufficient

Evidence:
{chr(10).join(evidence_context)}

Explanation:
""".strip()

    def _validate_citations(
        self,
        explanation: str,
        *,
        evidence_count: int,
    ) -> None:
        cited_numbers = {
            int(number)
            for number in CITATION_PATTERN.findall(explanation)
        }

        invalid_numbers = {
            number
            for number in cited_numbers
            if number < 1 or number > evidence_count
        }

        if invalid_numbers:
            raise RAGExplanationServiceError(
                f"Invalid citation numbers found in explanation: {invalid_numbers}. "
                f"Valid citation numbers are between 1 and {evidence_count}."
            )

        has_insufficient_evidence_statement = (
            "evidence is insufficient" in explanation.lower()
        )

        if not cited_numbers and not has_insufficient_evidence_statement:
            raise RAGExplanationServiceError(
                "Explanation must contain at least one valid citation or "
                "'evidence is insufficient' statement."
            )