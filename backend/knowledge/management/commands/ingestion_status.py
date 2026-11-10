import json

from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from knowledge.ingestion.status import ingestion_status


class Command(BaseCommand):
    help = "Show external ingestion jobs, discovery checkpoints, failures, card inventory, and feed repetition."

    def add_arguments(self, parser):
        parser.add_argument("--json", action="store_true", help="Print the full status as JSON.")
        parser.add_argument("--failures", type=int, default=10, help="Number of recent failures to list.")

    def handle(self, *args, **options):
        status = ingestion_status(recent_failures=options["failures"])
        if options["json"]:
            self.stdout.write(json.dumps(status, cls=DjangoJSONEncoder, indent=2))
            return

        self.stdout.write(f"Schedule enabled: {status['schedule_enabled']}")
        self.stdout.write(f"Adapters enabled by policy/config: {', '.join(status['adapters']['enabled']) or 'none'}")
        self.stdout.write("\nJobs by adapter/status:")
        for adapter, counts in sorted(status["jobs_by_adapter_status"].items()):
            self.stdout.write(f"  {adapter:15} " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        self.stdout.write("\nLast 24h: " + ", ".join(f"{k}={v}" for k, v in status["last_24h"].items()))

        inventory = status["inventory"]
        style = self.style.WARNING if inventory["low_inventory"] else self.style.SUCCESS
        self.stdout.write(style(
            f"\nEligible flashcards: {inventory['eligible_flashcards']} "
            f"(threshold {inventory['low_inventory_threshold']}), new in 24h: {inventory['created_last_24h']}"
        ))
        self.stdout.write(f"  by generation method: {inventory['by_generation_method']}")
        self.stdout.write(
            f"  canonical claims missing cards: {inventory['canonical_claims_missing_cards']} "
            f"(retries exhausted: {inventory['canonical_claims_generation_exhausted']})"
        )
        latency = status["discovery_to_feed_seconds"]
        if latency["samples"]:
            self.stdout.write(f"  discovery -> feed: median {latency['median']:.0f}s, max {latency['max']:.0f}s ({latency['samples']} cards)")
        feed = status["feed_last_24h"]
        self.stdout.write(f"\nFeed 24h: served={feed['cards_served']} cross-session repeats={feed['cross_session_repeats']} ({feed['repeat_rate']:.1%})")

        if status["recent_failures"]:
            self.stdout.write(self.style.WARNING("\nRecent failures / rejections:"))
            for failure in status["recent_failures"]:
                self.stdout.write(
                    f"  #{failure['id']} {failure['adapter']} {failure['external_id']} "
                    f"[{failure['status']}, attempts {failure['attempts']}]: {failure['error']}"
                )
        failing = [cp for cp in status["checkpoints"] if cp["consecutive_failures"]]
        if failing:
            self.stdout.write(self.style.WARNING("\nDiscovery checkpoints failing:"))
            for cp in failing:
                self.stdout.write(f"  {cp['adapter']} '{cp['topic']}' x{cp['consecutive_failures']}: {cp['last_error']}")
