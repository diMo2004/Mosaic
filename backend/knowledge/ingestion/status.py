"""Operational snapshot of ingestion, generation, inventory, and feed health.

Contains only aggregate counts and provider error messages, no user data.
"""
from datetime import timedelta
from statistics import median

from django.conf import settings
from django.db.models import Count, Exists, Min, OuterRef, Q
from django.utils import timezone

from knowledge.ingestion.registry import ADAPTERS, enabled_adapters
from knowledge.models import CanonicalClaim, IngestionJob, SourceDiscoveryCheckpoint
from learning.models import Flashcard, FlashcardFeedEvent


def ingestion_status(*, recent_failures: int = 10) -> dict:
    now = timezone.now()
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)

    jobs_by_status = {}
    for row in IngestionJob.objects.values("adapter", "status").annotate(n=Count("id")):
        jobs_by_status.setdefault(row["adapter"], {})[row["status"]] = row["n"]

    checkpoints = [
        {
            "adapter": cp.adapter,
            "topic": cp.topic,
            "runs": cp.runs,
            "candidates_total": cp.candidates_total,
            "last_candidates": cp.last_candidates,
            "exhausted": cp.exhausted,
            "consecutive_failures": cp.consecutive_failures,
            "last_error": cp.last_error[:300],
            "last_success_at": cp.last_success_at,
            "next_run_at": cp.next_run_at,
        }
        for cp in SourceDiscoveryCheckpoint.objects.order_by("-last_run_at")[:25]
    ]

    failures = [
        {
            "id": job.id,
            "adapter": job.adapter,
            "external_id": job.external_id,
            "status": job.status,
            "attempts": job.attempts,
            "error": job.last_error[:300],
            "updated_at": job.updated_at,
        }
        for job in IngestionJob.objects.filter(
            status__in=[IngestionJob.STATUS_FAILED, IngestionJob.STATUS_POLICY_REJECTED, IngestionJob.STATUS_RETRY]
        ).order_by("-updated_at")[:recent_failures]
    ]

    totals = {"claims_extracted": 0, "claims_supported": 0, "canonical_created": 0, "canonical_deduplicated": 0,
              "documents_created": 0, "documents_updated": 0, "unchanged": 0}
    for result in IngestionJob.objects.filter(completed_at__gte=day_ago).values_list("result", flat=True):
        for key in totals:
            totals[key] += int((result or {}).get(key, 0) or 0)

    eligible = Flashcard.objects.filter(is_active=True, source_claim__isnull=False, source_claim__is_active=True)
    by_method = dict(
        eligible.values("generation_method").annotate(n=Count("id")).values_list("generation_method", "n")
    )
    missing_cards = CanonicalClaim.objects.filter(is_active=True).exclude(
        Exists(Flashcard.objects.filter(source_claim=OuterRef("pk")))
    )
    max_attempts = int(getattr(settings, "FLASHCARD_GENERATION_MAX_ATTEMPTS", 4))

    # Discovery -> feed eligibility latency for cards created from ingestion jobs this week.
    latencies = []
    for created_at, discovered_at in (
        Flashcard.objects.filter(created_at__gte=week_ago)
        .annotate(discovered=Min("source_claim__source_claim__source_document__ingestion_jobs__discovered_at"))
        .filter(discovered__isnull=False)
        .values_list("created_at", "discovered")[:2000]
    ):
        latencies.append((created_at - discovered_at).total_seconds())

    served = FlashcardFeedEvent.objects.filter(event_type=FlashcardFeedEvent.EVENT_SERVED, created_at__gte=day_ago)
    served_total = served.count()
    repeats = served.filter(
        Exists(
            FlashcardFeedEvent.objects.filter(
                user_id=OuterRef("user_id"),
                flashcard_id=OuterRef("flashcard_id"),
                event_type=FlashcardFeedEvent.EVENT_SERVED,
                created_at__lt=OuterRef("created_at"),
                created_at__gte=week_ago,
            ).exclude(session_id=OuterRef("session_id"))
        )
    ).count()

    eligible_total = eligible.count()
    threshold = int(getattr(settings, "INGESTION_LOW_INVENTORY_THRESHOLD", 200))
    return {
        "generated_at": now,
        "schedule_enabled": bool(getattr(settings, "INGESTION_SCHEDULE_ENABLED", False)),
        "adapters": {"registered": sorted(ADAPTERS), "enabled": enabled_adapters()},
        "jobs_by_adapter_status": jobs_by_status,
        "last_24h": totals,
        "checkpoints": checkpoints,
        "recent_failures": failures,
        "inventory": {
            "eligible_flashcards": eligible_total,
            "low_inventory": eligible_total < threshold,
            "low_inventory_threshold": threshold,
            "created_last_24h": eligible.filter(created_at__gte=day_ago).count(),
            "by_generation_method": by_method,
            "canonical_claims_missing_cards": missing_cards.count(),
            "canonical_claims_generation_exhausted": missing_cards.filter(flashcard_attempts__gte=max_attempts).count(),
        },
        "discovery_to_feed_seconds": {
            "samples": len(latencies),
            "median": median(latencies) if latencies else None,
            "max": max(latencies) if latencies else None,
        },
        "feed_last_24h": {
            "cards_served": served_total,
            "cross_session_repeats": repeats,
            "repeat_rate": round(repeats / served_total, 3) if served_total else 0.0,
        },
    }


def pending_counts() -> dict:
    return dict(
        IngestionJob.objects.filter(~Q(status__in=IngestionJob.TERMINAL_STATUSES))
        .values("status").annotate(n=Count("id")).values_list("status", "n")
    )
