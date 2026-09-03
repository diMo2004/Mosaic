import re

class ClaimExtractionService:
    def extract_claims(self, text:str) -> list[str]:
        if not text:
            return []

        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        claims = []
        for sentence in sentences:
            cleaned = sentence.strip()
            if len(cleaned) < 8:
                continue
            claims.append(cleaned)

        return claims