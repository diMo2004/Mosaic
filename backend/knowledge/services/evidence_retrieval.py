from typing import Any
from math import sqrt

from django.db import connection
from pgvector.django import CosineDistance
from knowledge.models import Evidence
from knowledge.services.embeddings import EmbeddingService

class EvidenceRetrievalError(RuntimeError):
    """Raised when semantic evidence retrieval cannot be completed."""

class EvidenceRetrievalService:
    def __init__(self, embedder: EmbeddingService | None = None):
        self.embedder = embedder or EmbeddingService()

    def retrieve(self,query: str, *, top_k: int = 4) -> list[Evidence]:
        if not query or not query.strip():
            raise EvidenceRetrievalError(
                "Evidence retrieval requires a non-empty query."
            )

        if top_k < 1:
            raise EvidenceRetrievalError(
                "Evidence retrieval requires top_k to be a positive integer."
            )

        try:
            query_vector = self.embedder.embed_text(query)
        except Exception as e:
            raise EvidenceRetrievalError(
                f"Failed to generate embedding for query: {e}"
            ) from e

        try:
            queryset = (
                Evidence.objects
                .filter(embedding__isnull=False, excerpt__isnull=False)
                .exclude(excerpt="")
                .select_related("source", "claim", "claim__source_document")
            )
            # SQLite is used by the local fast test configuration and cannot
            # execute pgvector's <=> operator. Keep semantic ranking available
            # there with a small Python fallback; production PostgreSQL remains
            # database-ranked and indexed.
            if connection.vendor != "postgresql":
                evidence_items = list(queryset)
                for item in evidence_items:
                    item.distance = self._cosine_distance(item.embedding, query_vector)
                return sorted(
                    evidence_items,
                    key=lambda item: (item.distance, -item.relevance_score, -item.id),
                )[:top_k]
            evidence_items = list(
                queryset
                .annotate(
                    distance=CosineDistance(
                        "embedding",
                        query_vector,
                    )
                )
                .order_by(
                    "distance",
                    "-relevance_score",
                    "-created_at",
                )[:top_k]
            )
        except Exception as e:
            raise EvidenceRetrievalError(
                f"Failed to retrieve evidence from database: {e}"
            ) from e
        return evidence_items

    @staticmethod
    def _cosine_distance(left, right) -> float:
        left = [float(value) for value in left]
        right = [float(value) for value in right]
        denominator = sqrt(sum(value * value for value in left)) * sqrt(sum(value * value for value in right))
        if not denominator:
            return 1.0
        return 1.0 - sum(a * b for a, b in zip(left, right)) / denominator

    def retrieve_for_claim(
            self,
            claim_text: str,
            *,
            top_k: int = 4,
    ) -> list[Evidence]:
        return self.retrieve(
            claim_text,
            top_k=top_k,
        )
            
        
