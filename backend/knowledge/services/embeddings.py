import os
from django.conf import settings
from google import genai


class EmbeddingServiceError(RuntimeError):
    """Raised when an embedding cannot be generated."""

class EmbeddingService:
    DIMENSIONS = 768
    def __init__(self):
        api_key = getattr(settings, "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
        if not api_key:
            raise EmbeddingServiceError("GEMINI_API_KEY is not set in settings or environment variables.")
        self.client = genai.Client(api_key=api_key)
        self.model_name = getattr(
            settings, 
            "GEMINI_EMBEDDING_MODEL", 
            "gemini-embedding-001",
        )

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise EmbeddingServiceError("Cannot embed empty text.")
        try:
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=text.strip(),
                config={"output_dimensionality": self.DIMENSIONS},
            )
        except Exception as e:
            raise EmbeddingServiceError("Embedding provider request failed.") from e

        embeddings = getattr(result, "embeddings", None)
        if not embeddings:
            raise EmbeddingServiceError("Embedding provider returned no vector.")

        vector = list(embeddings[0].values)

        if len(vector) != self.DIMENSIONS:
            raise EmbeddingServiceError(
                f"Expected {self.DIMENSIONS}-dimensional embedding, "
                f"received {len(vector)} dimensions."
            )
        return vector
                