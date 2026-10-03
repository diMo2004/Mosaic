from django.core.management.base import BaseCommand
from knowledge.ingestion.adapters.arxiv import ArxivAdapter
from knowledge.ingestion.adapters.github import GitHubAdapter
from knowledge.ingestion.adapters.reddit import RedditAdapter
from knowledge.ingestion.adapters.stackexchange import StackExchangeAdapter
from knowledge.ingestion.adapters.wikimedia import WikimediaAdapter
from knowledge.ingestion.pipeline import ExternalIngestionPipeline


class Command(BaseCommand):
    help = "Ingest external CSE knowledge or evidence from GitHub, arXiv, Wikimedia, StackExchange, or Reddit"

    def add_arguments(self, parser):
        parser.add_argument("adapter", choices=["github", "arxiv", "wikimedia", "stackexchange", "reddit"])
        parser.add_argument("target", help="Target ID, slug, or title (e.g., 'django/django', '2301.00001', 'Binary search')")
        parser.add_argument("--legal-approved", action="store_true", help="Authorize legal review for Reddit evidence")

    def handle(self, *args, **options):
        adapter_type = options["adapter"]
        target = options["target"]
        pipeline = ExternalIngestionPipeline()

        self.stdout.write(f"Fetching from {adapter_type} for target: '{target}'...")

        if adapter_type == "github":
            items = GitHubAdapter().fetch(target)
        elif adapter_type == "arxiv":
            items = ArxivAdapter().fetch(target)
        elif adapter_type == "wikimedia":
            items = WikimediaAdapter().fetch(target)
        elif adapter_type == "stackexchange":
            items = StackExchangeAdapter().fetch(target)
        elif adapter_type == "reddit":
            items = RedditAdapter().fetch(target, legal_review_approved=options["legal_approved"])

        for item in items:
            result = pipeline.ingest_item(item)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully ingested '{item.title}' (Mode: {result['mode']}). Extracted {len(result['claims'])} claims."
                )
            )