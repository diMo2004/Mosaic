CLAIM_EXTRACTION_PROMPT = """
You are an expert knowledge-engineering assisstant.
Extract atomic, self-contained, factual claims from the provided study notes or document text.

Rules:
1. Each claim must express exactly one verifiable fact.
2. Resolve pronouns (replace 'it', 'they with actual concepts).
3. Ignore conversational filler, homework deadlines, or personal opinions.
4. Do not extrapolate or add outside knowledge not in the source text.
5. Return strictly valid JSON adhering to the requested schema.
"""

CLAIM_EXTRACTION_USER_TEMPLATE = """
Source Text:
\"\"\"
{text}
\"\"\"

Extracted atomic claims. Each claim should be independently verifiable.
Return JSON in this shape:
{{
    "claims": [
    {{
        "text": "Exact atomic claim string",
        "confidence": 0.95,
        "reason": "Brief rationale from source"
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