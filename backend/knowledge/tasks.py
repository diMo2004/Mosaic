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

# --- Scheduled external ingestion -------------------------------------------
# Imports are local to the task bodies: the ingestion pipeline imports this
# module (embed_evidence_task), so module-level imports would be circular.


@shared_task(name="knowledge.schedule_external_discovery", ignore_result=True)
def schedule_external_discovery_task() -> dict:
    """Beat entry point: fan out one discovery task per enabled adapter."""
    from knowledge.ingestion.registry import enabled_adapters

    adapters = enabled_adapters()
    for adapter_name in adapters:
        discover_adapter_task.delay(adapter_name)
    logger.info("ingestion.schedule.dispatched adapters=%s", adapters)
    return {"adapters": adapters}


@shared_task(name="knowledge.discover_adapter", acks_late=True, ignore_result=True)
def discover_adapter_task(adapter_name: str, topic: str | None = None, limit: int | None = None) -> dict:
    close_old_connections()
    from knowledge.ingestion.jobs import DiscoveryService

    return DiscoveryService(adapter_name).run(topic=topic, limit=limit).as_dict()


@shared_task(
    bind=True,
    name="knowledge.process_ingestion_job",
    acks_late=True,
    ignore_result=True,
    max_retries=None,  # bounded by IngestionJob.max_attempts
)
def process_ingestion_job_task(self, job_id: int) -> dict:
    close_old_connections()
    from knowledge.ingestion.jobs import IngestionJobService, JobRetry

    try:
        job = IngestionJobService().process(job_id)
    except JobRetry as retry:
        raise self.retry(countdown=retry.countdown)
    if job is None:
        return {"job_id": job_id, "status": "not_claimed"}
    return {"job_id": job_id, "status": job.status}


@shared_task(name="knowledge.recover_ingestion_jobs", ignore_result=True)
def recover_ingestion_jobs_task() -> dict:
    close_old_connections()
    from knowledge.ingestion.jobs import recover_stale_jobs

    return recover_stale_jobs()
