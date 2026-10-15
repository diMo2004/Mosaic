import json
import logging
from django.conf import settings
from google import genai
from google.genai import types
from learning.models import Flashcard

logger = logging.getLogger(__name__)

class FlashcardGenerationService:
    def generate_from_canonical_claim(self, canonical_claim):
        """
        Generate flashcards from a given canonical claim.
        """
        if canonical_claim is None:
            raise ValueError("Flashcards can only be generated from a CanonicalClaim.")

        api_key = getattr(settings, "GEMINI_API_KEY", "")
        card_copy = self._generate_copy(canonical_claim.text, canonical_claim.concept.name, api_key)

        flashcard, _ = Flashcard.objects.get_or_create(
            source_claim=canonical_claim,
            defaults={
                "title": card_copy.get("title", canonical_claim.concept.name),
                "prompt": card_copy.get("prompt", f"What is the key takeaway regarding {canonical_claim.concept.name}?"),
                "answer": card_copy.get("answer", canonical_claim.text),
                "explanation": card_copy.get("explanation", "Verified canonical knowledge card."),
                "difficulty": card_copy.get("difficulty", Flashcard.DIFFICULTY_BEGINNER),
                "is_active": True,
                "created_by_ai": bool(api_key),
            },
        )
        return flashcard

    def _generate_copy(self, claim_text: str, concept_name: str, api_key: str) -> dict:
        if not api_key:
            return {
                "title": concept_name,
                "prompt": f"Explain the principle: {concept_name}",
                "answer": claim_text,
                "explanation": "Verified from source note.",
                "difficulty": Flashcard.DIFFICULTY_BEGINNER,
            }

        client = genai.Client(api_key=api_key)
        prompt = f"""You are an elite Computer Science educator creating an engaging, active-recall flashcard for university students.
Topic: {concept_name}
Canonical Knowledge: "{claim_text}"

Generate an interactive flashcard:
- "title": Catchy, modern 3-5 word card title.
- "prompt": An engaging active-recall question or technical scenario (avoid generic "What is X?").
- "answer": Clear, direct, high-yield answer.
- "explanation": 2-3 sentences explaining the underlying intuition or real-world system application.
- "difficulty": "beginner", "intermediate", or "advanced".
Output JSON strictly as:
{{
  "title": "...",
  "prompt": "...",
  "answer": "...",
  "explanation": "...",
  "difficulty": "beginner"
}}
"""
        try:
            res = client.models.generate_content(
                model=getattr(settings, "GEMINI_CLAIM_MODEL", "gemini-3.8-flash"),
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.3),
            )
            return json.loads(res.text)
        except Exception as e:
            logger.warning("Flashcard generation LLM error %s", e)
            return {
                "title": concept_name,
                "prompt": f"How does {concept_name} apply to: {claim_text}?",
                "difficulty": Flashcard.DIFFICULTY_BEGINNER,
            } 
