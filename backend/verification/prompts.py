CLAIM_EXTRACTION_PROMPT = """
You extract atomic factual claims from study material.
Return only structured JSON.
Do not add facts that are not present in the source text.
"""

CLAIM_EXTRACTION_USER_TEMPLATE = """
Source Text:
{text}

Extracted atomic claims. Each claim should be independently verifiable.
Return JSON in this shape:
{{
    "claims": [
    {{
        "text": "Claim text",
        "confidence": 0.0,
        "reason": "short reason"
    }},
    ]
}}
"""

CLAIM_VERIFICATION_SYSTEM_PROMPT = """
You verify claims using only the provided evidence.
Do not use outside knowledge.
If evidence is insufficient, return UNCERTAIN.
"""

CLAIM_VERIFICATION_USER_TEMPLATE = """
Claim:
{claim}

Evidence:
{evidence}

Return JSON:
{{
  "status": "SUPPORTED | CONTRADICTED | PARTIALLY_SUPPORTED | UNCERTAIN",
  "confidence": 0.0,
  "reason": "short explanation"
}}
"""

FLASHCARD_GENERATION_SYSTEM_PROMPT = """
You create concise educational flashcards from verified canonical knowledge.
Do not introduce unsupported facts.
"""

FLASHCARD_GENERATION_USER_TEMPLATE = """
Canonical claim:
{claim}

Concept:
{concept}

Create a flashcard as JSON:
{{
  "title": "...",
  "prompt": "...",
  "answer": "...",
  "explanation": "..."
}}
"""