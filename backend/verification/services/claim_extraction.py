import re
import json
import os
from google import genai
from google.genai import types
from django.conf import settings
from verification.prompts import CLAIM_EXTRACTION_PROMPT, CLAIM_EXTRACTION_USER_TEMPLATE

_CACHED_EXTRACTOR_CLIENT = None

def get_extractor_model():
    global _CACHED_EXTRACTOR_CLIENT

    if _CACHED_EXTRACTOR_CLIENT is None:
        api_key = getattr(
            settings,
            "GEMINI_API_KEY",
            os.getenv("GEMINI_API_KEY", ""),
        )

        if not api_key:
            return None

        client = genai.Client(api_key=api_key)

        model_name = getattr(
            settings,
            "GEMINI_CLAIM_MODEL",
            "gemini-3.6-flash",
        )

        class GeminiModelWrapper:
            def generate_content(self, prompt):
                return client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=CLAIM_EXTRACTION_PROMPT,
                        response_mime_type="application/json",
                        thinking_config=types.ThinkingConfig(
                            thinking_level="low",
                        ),
                    ),
                )

        _CACHED_EXTRACTOR_CLIENT = GeminiModelWrapper()

    return _CACHED_EXTRACTOR_CLIENT

class ClaimExtractionService:
    def __init__(self):
        self.model = get_extractor_model()

    def _fallback_sentence_split(self, text: str) ->list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        claims = []
        for sentence in sentences:
            cleaned = sentence.strip()
            if len(cleaned) >= 8:
                claims.append(cleaned)
        return claims

    def extract_claims_detailed(self, text: str) -> list[dict]:
        if not text or not text.strip():
            return []

        user_prompt = CLAIM_EXTRACTION_USER_TEMPLATE.format(text=text.strip())

        try:
            response = self.model.generate_content(user_prompt)
            if not response or not response.text:
                return [{"text": c, "confidence": 0.5, "reason": "Regex fallback"} for c in self._fallback_sentence_split(text)]
            data = json.loads(response.text)
            extracted = data.get("claims", [])
            results = []
            for item in extracted:
                claim_text = item.get("text", "").strip()
                if claim_text:
                    results.append({
                        "text": claim_text,
                        "confidence": float(item.get("confidence", 0.85)),
                        "reason": item.get("reason", "").strip(),
                    })
            return results if results else [{"text": c, "confidence": 0.5, "reason": "Regex fallback"} for c in self._fallback_sentence_split(text)]
        except Exception as exc:
            print(f"[ClaimExtractionService Warning] LLM extraction failed: {exc}. Using fallback.")
            return [{"text": c, "confidence": 0.5, "reason": "Regex fallback"} for c in self._fallback_sentence_split(text)]

    def extract_claims(self, text:str) -> list[str]:
        detailed_claims = self.extract_claims_detailed(text)
        return [c["text"] for c in detailed_claims if c.get("text")]