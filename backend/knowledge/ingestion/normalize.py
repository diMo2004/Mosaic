"""Text normalization used for change detection, deduplication, and grounding."""
import hashlib
import re

_WS = re.compile(r"\s+")
_NON_WORD = re.compile(r"[^\w\s]")
_TOKEN = re.compile(r"[a-z0-9_+#]+")
_SENTENCE = re.compile(r"(?<=[.!?])\s+")
_STOPWORDS = frozenset(
    "a an the of to in on for and or is are was were be been being by with as at from that this these "
    "those it its into than then which who whom can may also not no".split()
)


def normalize_document_text(text: str) -> str:
    return _WS.sub(" ", (text or "").strip())


def content_hash(text: str) -> str:
    """Hash of whitespace-normalized document text; ignores formatting-only changes."""
    return hashlib.sha256(normalize_document_text(text).encode("utf-8")).hexdigest()


def normalize_claim_text(text: str) -> str:
    return _WS.sub(" ", _NON_WORD.sub(" ", (text or "").casefold())).strip()


def claim_hash(text: str) -> str:
    return hashlib.sha256(normalize_claim_text(text).encode("utf-8")).hexdigest()


def _content_tokens(text: str) -> list[str]:
    return [token for token in _TOKEN.findall((text or "").lower()) if token not in _STOPWORDS]


def best_supporting_passage(claim: str, document: str, *, window: int = 2) -> tuple[float, str]:
    """Return (coverage, passage): how much of the claim's vocabulary one passage contains.

    Coverage is the fraction of the claim's content tokens present in the best
    window of ``window`` consecutive sentences. It guards self-attestation: a
    claim the extractor paraphrased beyond recognition or hallucinated scores low.
    """
    claim_tokens = set(_content_tokens(claim))
    if not claim_tokens:
        return 0.0, ""
    sentences = [s.strip() for s in _SENTENCE.split(normalize_document_text(document)) if s.strip()]
    best_score, best_passage = 0.0, ""
    for index in range(len(sentences)):
        passage = " ".join(sentences[index:index + window])
        score = len(claim_tokens & set(_content_tokens(passage))) / len(claim_tokens)
        if score > best_score:
            best_score, best_passage = score, passage
            if score == 1.0:
                break
    return best_score, best_passage
