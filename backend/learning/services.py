from learning.models import Flashcard

class FlashcardGenerationService:
    def generate_from_canonical_claim(self, canonical_claim):
        """
        Generate flashcards from a given canonical claim.
        """
        # Placeholder logic for generating flashcards
        flashcard, _ = Flashcard.objects.get_or_create(
            source_claim=canonical_claim,
            defaults={
                "title": canonical_claim.concept.name,
                "prompt": f"What should you know about: {canonical_claim.text}?",
                "answer": canonical_claim.text,
                "explanation": (
                    "This flashcard was generated from a canonical claim.",
                ),
                "difficulty": Flashcard.DIFFICULTY_BEGINNER,
                "is_active": True,
                "created_by_ai": False,
            },
        )
        return flashcard