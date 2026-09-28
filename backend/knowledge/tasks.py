import logging
from celery import shared_task
from django.db import close_old_connections

from knowledge.models import Evidence
from knowledge.services.embeddings import (
    EmbeddingService,
    EmbeddingServiceError,
)

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    name="knowledge.embed_evidence",
    max_retries=3,
    acks_late=True,
)
def embed_evidence_task(
    self,
    evidence_id: int
) -> dict[str, object]:
    close_old_connections()
    try:
        evidence = (
            Evidence.objects
            .select_related("source")
            .get(pk=evidence_id)
        )
    except Evidence.DoesNotExist:
        logger.warning(
            "Skipping embedding task: evidence %s no longer exists.",
            evidence_id,
        )
        return {
            "status": "missing",
            "evidence_id": evidence_id,
        }

    if evidence.embedding is not None:
        return {
            "status": "already_embedded",
            "evidence_id": evidence_id,
        }

    if not evidence.excerpt or not evidence.excerpt.strip():
        logger.warning(
            "Skipping embedding task: evidence %s has no excerpt.",
            evidence_id,
        )
        return {
            "status": "skipped_empty_excerpt",
            "evidence_id": evidence_id,
        }

    embedding_text = "\n".join(
        part.strip()
        for part in [
            evidence.title,
            evidence.excerpt,
            evidence.source.name if evidence.source_id else "",
        ]
        if part and part.strip()
    )

    try:
        vector = EmbeddingService().embed_text(embedding_text)
    except EmbeddingServiceError as e:
        retry_number = self.request.retries + 1
        logger.warning(
            "Evidence embedding failed for evidence %s; retry %s/3.",
            evidence_id,
            retry_number,
            exc_info=True,
        )

        raise self.retry(
            exc=e,
            countdown=60 * (2 ** self.request.retries),
        )

    evidence.embedding = vector
    evidence.save(update_fields=["embedding", "updated_at"])

    logger.info(
        "Stored embedding for evidence %s.",
        evidence_id,
    )

    return {
        "status": "embedded",
        "evidence_id": evidence_id,
    }