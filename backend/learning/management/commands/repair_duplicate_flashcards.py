from django.core.management.base import BaseCommand

from learning.models import Flashcard
from learning.services.flashcard_service import FlashcardGenerationService


class Command(BaseCommand):
    help = (
        "Replace legacy generic/duplicated canonical flashcard questions. "
        "Run with --apply to save changes."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Save repaired prompts. Without this flag, only report candidates.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        service = FlashcardGenerationService()
        repaired = 0

        cards = (
            Flashcard.objects.filter(source_claim__isnull=False)
            .select_related("source_claim__concept")
            .iterator()
        )
        for card in cards:
            claim = card.source_claim
            prompt = (card.prompt or "").strip()
            normalized_prompt = service._normalized_text(prompt)
            normalized_claim = service._normalized_text(claim.text)
            is_legacy_template = (
                normalized_prompt.startswith("how does ")
                and " apply to " in normalized_prompt
                and normalized_claim in normalized_prompt
            )

            if not is_legacy_template and not service._is_duplicate_prompt(
                prompt, card.answer or ""
            ):
                continue

            replacement = service._fallback_copy(claim.text, claim.concept.name)
            self.stdout.write(
                f"{'Repairing' if apply_changes else 'Would repair'} flashcard "
                f"{card.pk}: {prompt!r} -> {replacement['prompt']!r}"
            )
            if apply_changes:
                card.prompt = replacement["prompt"]
                card.save(update_fields=["prompt", "updated_at"])
            repaired += 1

        action = "Repaired" if apply_changes else "Found"
        self.stdout.write(self.style.SUCCESS(f"{action} {repaired} flashcard(s)."))
        if not apply_changes and repaired:
            self.stdout.write("Review this list, then rerun with --apply to save prompts.")
