from django.core.management.base import BaseCommand
from knowledge.ingestion.http import ProviderError
from knowledge.ingestion.license_checker import LicensePolicyError
from knowledge.ingestion.pipeline import ExternalIngestionPipeline, InsufficientContentError
from knowledge.ingestion.registry import get_adapter


class Command(BaseCommand):
    help = "Ingest external CSE knowledge from approved adapters and official language documentation"

    def add_arguments(self, parser):
        parser.add_argument("adapter", choices=["github", "arxiv", "wikimedia", "stackexchange", "reddit", "official-docs"])
        parser.add_argument("target", help="Target ID, slug, or title (e.g., 'django/django', '2301.00001', 'Binary search')")
        parser.add_argument("--legal-approved", action="store_true", help="Authorize legal review for Reddit evidence")
        parser.add_argument("--url", help="official-docs only: an allow-listed page URL within the language documentation")

    def handle(self, *args, **options):
        adapter_type = options["adapter"]
        target = options["target"]
        pipeline = ExternalIngestionPipeline()

        self.stdout.write(f"Fetching from {adapter_type} for target: '{target}'...")

        kwargs = {}
        if adapter_type == "reddit":
            kwargs["legal_review_approved"] = options["legal_approved"]
        if adapter_type == "official-docs" and options.get("url"):
            kwargs["url"] = options["url"]
        try:
            items = get_adapter(adapter_type).fetch(target, **kwargs)
        except ProviderError as exc:
            self.stderr.write(self.style.ERROR(f"Fetch failed: {exc}"))
            return

        for item in items:
            try:
                result = pipeline.ingest_item(item)
            except LicensePolicyError as exc:
                self.stderr.write(self.style.ERROR(f"Rejected by source policy: '{item.title}': {exc}"))
                continue
            except InsufficientContentError as exc:
                self.stderr.write(self.style.WARNING(f"Skipped '{item.title}': {exc}"))
                continue
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully ingested '{item.title}' (Mode: {result['mode']}). Extracted {len(result['claims'])} claims."
                )
            )
