from django.conf import settings
from django.core.management.base import BaseCommand

from learning.models import Flashcard
from learning.services.flashcard_service import FlashcardGenerationService


class Command(BaseCommand):
    help = (
        "Backfill reel card metadata for canonical flashcards. Defaults to a dry run; "
        "use --apply to generate metadata and save it."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Generate and save card types and quiz metadata (may call Gemini).",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Process at most this many cards, oldest metadata first.",
        )

    def handle(self, *args, **options):
        if options["limit"] is not None and options["limit"] < 1:
            self.stderr.write(self.style.ERROR("--limit must be a positive integer."))
            return

        cards = (
            Flashcard.objects.filter(
                is_active=True,
                source_claim__isnull=False,
                card_metadata_version__lt=1,
            )
            .select_related("source_claim__concept")
            .order_by("created_at", "pk")
        )
        if options["limit"]:
            cards = cards[: options["limit"]]

        card_ids = list(cards.values_list("pk", flat=True))
        if not options["apply"]:
            self.stdout.write(f"Dry run: {len(card_ids)} flashcard(s) need metadata.")
            for card_id in card_ids:
                self.stdout.write(f"Would update flashcard {card_id}.")
            self.stdout.write("Rerun with --apply to generate and save metadata.")
            return

        service = FlashcardGenerationService()
        api_key = getattr(settings, "GEMINI_API_KEY", "")
        if card_ids and not api_key:
            self.stdout.write(self.style.WARNING(
                "GEMINI_API_KEY is not configured; no cards were changed. "
                "Configure it and rerun with --apply."
            ))
            return
        updated = 0
        for card in cards:
            generated = service._generate_copy(
                card.source_claim.text,
                card.source_claim.concept.name,
                api_key,
            )
            card.card_type = generated["card_type"]
            card.quiz_options = generated["quiz_options"]
            card.key_points = generated["key_points"]
            card.visual_hint = generated["visual_hint"]
            card.card_metadata_version = 1
            card.save(update_fields=[
                "card_type",
                "quiz_options",
                "key_points",
                "visual_hint",
                "card_metadata_version",
                "updated_at",
            ])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Updated {updated} flashcard(s)."))
