from django.core.management.base import BaseCommand, CommandError

from knowledge.ingestion.jobs import DiscoveryService, IngestionJobService, JobRetry
from knowledge.ingestion.registry import ADAPTERS, enabled_adapters
from knowledge.models import CanonicalClaim, IngestionJob
from learning.tasks import generate_flashcard_for_claim_task

MAX_MANUAL_LIMIT = 25


class Command(BaseCommand):
    help = (
        "Run one bounded discovery + ingestion pass. By default jobs are enqueued for "
        "Celery workers; --sync processes them in this process (no worker needed)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--adapter", choices=sorted(ADAPTERS), action="append",
                            help="Adapter(s) to run. Defaults to all adapters enabled by policy/config.")
        parser.add_argument("--topic", help="Search this topic instead of planning topics from the CSE taxonomy.")
        parser.add_argument("--limit", type=int, default=3, help=f"Max new jobs per adapter (<= {MAX_MANUAL_LIMIT}).")
        parser.add_argument("--sync", action="store_true", help="Process discovered jobs synchronously.")

    def handle(self, *args, **options):
        limit = options["limit"]
        if not 1 <= limit <= MAX_MANUAL_LIMIT:
            raise CommandError(f"--limit must be between 1 and {MAX_MANUAL_LIMIT}.")
        adapters = options["adapter"] or enabled_adapters()
        if not adapters:
            raise CommandError("No adapters are enabled. Check INGESTION_ENABLED_ADAPTERS and source policies.")

        service = IngestionJobService()
        processed_ids = []
        for adapter_name in adapters:
            stats = DiscoveryService(adapter_name).run(topic=options["topic"], limit=limit, enqueue=not options["sync"])
            self.stdout.write(f"{adapter_name}: {stats.as_dict()}")
            if not options["sync"]:
                continue
            for job in IngestionJob.objects.filter(adapter=adapter_name, status=IngestionJob.STATUS_PENDING).order_by("-discovered_at")[:limit]:
                try:
                    processed = service.process(job.id)
                except JobRetry as retry:
                    job.refresh_from_db()
                    self.stdout.write(self.style.WARNING(f"  job {job.id}: will retry in {retry.countdown:.0f}s ({job.last_error})"))
                    continue
                if processed is None:
                    continue
                processed_ids.append(processed.id)
                style = self.style.SUCCESS if processed.status in (IngestionJob.STATUS_SUCCEEDED, IngestionJob.STATUS_UNCHANGED) else self.style.WARNING
                self.stdout.write(style(f"  job {processed.id} {processed.external_id}: {processed.status} {processed.last_error} {processed.result}"))
        if options["sync"] and processed_ids:
            # No worker in --sync mode: generate this run's cards inline (idempotent).
            claim_ids = CanonicalClaim.objects.filter(
                is_active=True,
                flashcards__isnull=True,
                source_claim__source_document__ingestion_jobs__id__in=processed_ids,
            ).values_list("id", flat=True).distinct()
            for claim_id in claim_ids:
                result = generate_flashcard_for_claim_task(claim_id)
                self.stdout.write(f"  flashcard for canonical claim {claim_id}: {result.get('status')}")
