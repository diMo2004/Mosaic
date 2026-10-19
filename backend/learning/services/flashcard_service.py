import json
import logging
import re
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
        card_copy = self._generate_copy(
            canonical_claim.text,
            canonical_claim.concept.name,
            api_key,
        )

        flashcard, _ = Flashcard.objects.get_or_create(
            source_claim=canonical_claim,
            defaults={
                "title": card_copy.get("title", canonical_claim.concept.name),
                "prompt": card_copy.get("prompt", f"What is the key takeaway regarding {canonical_claim.concept.name}?"),
                "answer": card_copy.get("answer", canonical_claim.text),
                "explanation": card_copy.get("explanation", "Verified canonical knowledge card."),
                "difficulty": card_copy.get("difficulty", Flashcard.DIFFICULTY_BEGINNER),
                "card_type": card_copy.get("card_type", Flashcard.CARD_TYPE_RECALL),
                "quiz_options": card_copy.get("quiz_options"),
                "key_points": card_copy.get("key_points"),
                "visual_hint": card_copy.get("visual_hint"),
                "card_metadata_version": 1,
                "is_active": True,
                "created_by_ai": bool(api_key),
            },
        )
        return flashcard

    def _generate_copy(self, claim_text: str, concept_name: str, api_key: str) -> dict:
        if not api_key:
            return self._fallback_copy(claim_text, concept_name)

        client = genai.Client(api_key=api_key)
        prompt = f"""You are an elite Computer Science educator creating an engaging, active-recall flashcard for university students.
Topic: {concept_name}
Canonical Knowledge: "{claim_text}"

Generate one useful active-recall flashcard from the canonical knowledge. The question must ask
about a specific fact supported by the claim. The answer must directly answer that question.
Do not put the full claim in the question, repeat the answer in the question, or use generic
wrappers such as "How does {concept_name} apply to:". The topic is displayed separately in the UI.

Generate an interactive flashcard:
- "title": Catchy, modern 3-5 word card title.
- "prompt": An engaging active-recall question or technical scenario (avoid generic "What is X?").
- "answer": Clear, direct, high-yield answer.
- "explanation": 2-3 sentences explaining the underlying intuition or real-world system application.
- "difficulty": "beginner", "intermediate", or "advanced".
- "card_type": "concept_visual", "recall", or "quick_quiz". Use quick_quiz only
  when you can produce one unambiguous correct option and three plausible distractors.
- Choose concept_visual for a process or relationship that benefits from a visual anchor;
  choose recall for a direct, open-ended question; choose quick_quiz for a clear contrast
  where distractors can be confidently ruled out from the canonical knowledge.
- "quiz_options": for quick_quiz, exactly four objects with "text", "is_correct",
  and a brief "explanation". Exactly one option is correct and it must express the answer;
  for other types use [].
- "key_points": zero to four short strings with useful takeaways.
- "visual_hint": a short diagram label or emoji for concept_visual, otherwise "".
Output JSON strictly as:
{{
  "title": "...",
  "prompt": "...",
  "answer": "...",
  "explanation": "...",
  "difficulty": "beginner",
  "card_type": "recall",
  "quiz_options": [],
  "key_points": [],
  "visual_hint": ""
}}
"""
        try:
            res = client.models.generate_content(
                model=getattr(settings, "GEMINI_CLAIM_MODEL", "gemini-3.8-flash"),
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.3),
            )
            generated = json.loads(res.text)
            if not isinstance(generated, dict):
                raise ValueError("Flashcard response must be a JSON object")

            fallback = self._fallback_copy(claim_text, concept_name)
            card_copy = {
                "title": self._text_or(generated.get("title"), fallback["title"]),
                "prompt": self._text_or(generated.get("prompt"), fallback["prompt"]),
                "answer": self._text_or(generated.get("answer"), claim_text),
                "explanation": self._text_or(
                    generated.get("explanation"), fallback["explanation"]
                ),
                "difficulty": generated.get(
                    "difficulty", Flashcard.DIFFICULTY_BEGINNER
                ),
                "card_type": generated.get("card_type", Flashcard.CARD_TYPE_RECALL),
                "quiz_options": self._validated_quiz_options(
                    generated.get("quiz_options"),
                ),
                "key_points": self._validated_key_points(generated.get("key_points")),
                "visual_hint": self._text_or(generated.get("visual_hint"), "")[:255],
            }
            if self._is_duplicate_prompt(card_copy["prompt"], card_copy["answer"]):
                logger.warning(
                    "Discarding duplicate flashcard copy for concept %s",
                    concept_name,
                )
                return fallback
            if card_copy["difficulty"] not in {
                Flashcard.DIFFICULTY_BEGINNER,
                Flashcard.DIFFICULTY_INTERMEDIATE,
                Flashcard.DIFFICULTY_ADVANCED,
            }:
                card_copy["difficulty"] = Flashcard.DIFFICULTY_BEGINNER
            if card_copy["card_type"] not in {
                Flashcard.CARD_TYPE_CONCEPT_VISUAL,
                Flashcard.CARD_TYPE_RECALL,
                Flashcard.CARD_TYPE_QUICK_QUIZ,
            }:
                card_copy["card_type"] = Flashcard.CARD_TYPE_RECALL
            if (
                card_copy["card_type"] == Flashcard.CARD_TYPE_QUICK_QUIZ
                and len(card_copy["quiz_options"]) != 4
            ):
                card_copy["card_type"] = Flashcard.CARD_TYPE_RECALL
            if card_copy["card_type"] != Flashcard.CARD_TYPE_QUICK_QUIZ:
                card_copy["quiz_options"] = None
            if card_copy["card_type"] == Flashcard.CARD_TYPE_CONCEPT_VISUAL:
                card_copy["visual_hint"] = card_copy["visual_hint"] or "💡"
            return card_copy
        except Exception as e:
            logger.warning("Flashcard generation LLM error %s", e)
            return self._fallback_copy(claim_text, concept_name)

    @staticmethod
    def _text_or(value, fallback: str) -> str:
        return value.strip() if isinstance(value, str) and value.strip() else fallback

    @staticmethod
    def _normalized_text(value: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", value.casefold())).strip()

    @classmethod
    def _is_duplicate_prompt(cls, prompt: str, answer: str) -> bool:
        normalized_prompt = cls._normalized_text(prompt)
        normalized_answer = cls._normalized_text(answer)
        if not normalized_prompt or not normalized_answer:
            return True
        return (
            normalized_prompt == normalized_answer
            or (len(normalized_answer) >= 24 and normalized_answer in normalized_prompt)
        )

    @classmethod
    def _validated_quiz_options(cls, options) -> list:
        if not isinstance(options, list) or len(options) != 4:
            return []
        validated = []
        for option in options:
            if not isinstance(option, dict) or not isinstance(option.get("is_correct"), bool):
                return []
            text = cls._text_or(option.get("text"), "")
            if not text:
                return []
            validated.append({
                "text": text,
                "is_correct": option["is_correct"],
                "explanation": cls._text_or(option.get("explanation"), ""),
            })
        normalized = [cls._normalized_text(option["text"]) for option in validated]
        if len(set(normalized)) != 4 or sum(item["is_correct"] for item in validated) != 1:
            return []
        return validated

    @classmethod
    def _validated_key_points(cls, points) -> list:
        if not isinstance(points, list):
            return []
        return [
            point.strip()
            for point in points
            if isinstance(point, str) and point.strip()
        ][:4]

    @staticmethod
    def _fallback_copy(claim_text: str, concept_name: str) -> dict:
        """Return a meaningful recall pair when model generation is unavailable."""
        claim = claim_text.strip().rstrip(".!? ")
        conditional = re.match(r"^If\s+(.+?),\s*(.+)$", claim, flags=re.IGNORECASE)
        continuation = re.match(
            r"^(.+?)\s+continues by\b", claim, flags=re.IGNORECASE
        )

        if conditional:
            prompt = f"What happens when {conditional.group(1).strip()}?"
        elif continuation:
            prompt = f"How does {continuation.group(1).strip()} continue?"
        else:
            prompt = f"What is one important rule about {concept_name.strip()}?"

        # A malformed/very short claim should never make the question itself the answer.
        if FlashcardGenerationService._is_duplicate_prompt(prompt, claim_text):
            prompt = f"What is one important rule about {concept_name.strip()}?"

        return {
            "title": concept_name,
            "prompt": prompt,
            "answer": claim_text.strip(),
            "explanation": "Verified from the canonical claim.",
            "difficulty": Flashcard.DIFFICULTY_BEGINNER,
            "card_type": Flashcard.CARD_TYPE_RECALL,
            "quiz_options": None,
            "key_points": [],
            "visual_hint": "",
        }
