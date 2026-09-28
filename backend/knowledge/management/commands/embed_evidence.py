from django.core.management.base import BaseCommand, CommandError


from knowledge.models import Evidence
from knowledge.services.embeddings import (
    EmbeddingService,
    EmbeddingServiceError,
)

def build_embedding_text(evidence: Evidence) -> str:
    parts = [
        evidence.title,
        evidence.excerpt,
        evidence.source.name if evidence.source_id else "",
    ]
    return "\n".join(
        part.strip()
        for part in parts
        if part and part.strip()
    )

class Command(BaseCommand):
    help = "Generate and store vector embeddings for evidence excerpts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-embed all evidence that already has an embedding.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Process at most this many evidence records.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        limit = options["limit"]

        if limit is not None and limit < 1:
            raise CommandError("--limit must be a greater than zero.")

        queryset = (
            Evidence.objects
            .filter(excerpt__isnull=False)
            .exclude(excerpt="")
            .select_related("source")
            .order_by("id") 
        )

        if not force:
            queryset = queryset.filter(embedding__isnull=True)

        if limit is not None:
            queryset = queryset[:limit]

        evidence_items = list(queryset)

        if not evidence_items:
            self.stdout.write("No evidence records require embedding.")
            return

        embedder = EmbeddingService()
        processed = 0
        failed = 0

        for evidence in evidence_items:
            try:
                embedding_text = build_embedding_text(evidence)
                vector = embedder.embed_text(embedding_text)

                evidence.embedding = vector
                evidence.save(update_fields=["embedding", "updated_at"])
                processed += 1
                self.stdout.write(f"Embedded evidence {evidence.pk}.")
            except EmbeddingServiceError as e:
                failed += 1
                self.stderr.write(
                    self.style.ERROR(
                        f"Failed to embed evidence {evidence.pk}: {e}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Embedding process completed. "
                f"Processed: {processed}, Failed: {failed}."
            )
        )

        if failed:
            raise CommandError(
                f"Embedding process completed with {failed} failures."
            )