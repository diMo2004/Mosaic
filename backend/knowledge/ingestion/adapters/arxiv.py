import re
import xml.etree.ElementTree as ET
from decimal import Decimal

from knowledge.ingestion.base import BaseExternalAdapter, DiscoveryCandidate, DiscoveryPage, IngestionItem
from knowledge.ingestion.http import PermanentProviderError, provider_get
from knowledge.models import Source

API_URL = "https://export.arxiv.org/api/query"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}
# Computer-science categories searched during discovery.
CS_CATEGORIES = ("cs.DS", "cs.PL", "cs.SE", "cs.DB", "cs.OS", "cs.NI", "cs.LG", "cs.AI", "cs.CR", "cs.DC")
_VERSION_SUFFIX = re.compile(r"v\d+$")


def _base_id(entry_id: str) -> str:
    """'http://arxiv.org/abs/2301.00001v2' -> '2301.00001'."""
    raw = entry_id.rsplit("/abs/", 1)[-1].strip()
    return _VERSION_SUFFIX.sub("", raw)


class ArxivAdapter(BaseExternalAdapter):
    """Fetches academic computer science preprint metadata (title + abstract) from arXiv.

    Only descriptive metadata is used: arXiv's API terms place it under CC0.
    Full-text e-prints keep their authors' licenses and are never fetched.
    """
    name = "arxiv"

    def fetch(self, arxiv_id: str, **kwargs) -> list[IngestionItem]:
        arxiv_id = _base_id(arxiv_id)
        resp = provider_get(API_URL, params={"id_list": arxiv_id}, timeout=15)
        root = ET.fromstring(resp.text)
        entry = root.find("atom:entry", ATOM)
        if entry is None or entry.find("atom:title", ATOM) is None:
            raise PermanentProviderError(f"No arXiv record found for id {arxiv_id}")
        title = " ".join((entry.find("atom:title", ATOM).text or "").split())
        summary = " ".join((entry.find("atom:summary", ATOM).text or "").split())
        published = entry.findtext("atom:published", default="", namespaces=ATOM)
        updated = entry.findtext("atom:updated", default="", namespaces=ATOM)
        authors = [
            name.text.strip()
            for name in entry.findall("atom:author/atom:name", ATOM)
            if name.text
        ]
        return [
            IngestionItem(
                title=f"arXiv: {title}",
                url=f"https://arxiv.org/abs/{arxiv_id}",
                raw_text=f"Title: {title}\n\nAbstract:\n{summary}",
                source_name="arXiv",
                source_domain="arxiv.org",
                source_type=Source.SOURCE_TYPE_ACADEMIC,
                authority_score=Decimal("0.90"),
                license_name="cc0-1.0",
                license_url="https://info.arxiv.org/help/api/tou.html",
                attribution_required=True,
                commercial_use_allowed=True,
                ai_use_allowed=True,
                scraping_allowed=True,
                document_type="other",
                metadata={"arxiv_id": arxiv_id, "published": published, "updated": updated, "authors": authors[:10]},
                policy_key="arxiv",
                external_id=f"arxiv:{arxiv_id}",
                attribution_text=f"{', '.join(authors[:3])}{' et al.' if len(authors) > 3 else ''} (arXiv:{arxiv_id})",
            )
        ]

    def discover(self, topic: str, cursor=None, limit: int = 5) -> DiscoveryPage:
        start = int((cursor or {}).get("start", 0))
        phrase = topic.replace('"', "").strip()
        categories = " OR ".join(f"cat:{cat}" for cat in CS_CATEGORIES)
        resp = provider_get(
            API_URL,
            params={
                "search_query": f'(abs:"{phrase}" OR ti:"{phrase}") AND ({categories})',
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "start": start,
                "max_results": max(1, min(limit, 50)),
            },
            timeout=20,
        )
        root = ET.fromstring(resp.text)
        candidates = []
        for entry in root.findall("atom:entry", ATOM):
            entry_id = entry.findtext("atom:id", default="", namespaces=ATOM)
            if "/abs/" not in entry_id:
                continue
            arxiv_id = _base_id(entry_id)
            candidates.append(DiscoveryCandidate(
                external_id=f"arxiv:{arxiv_id}",
                identifier=arxiv_id,
                title=" ".join((entry.findtext("atom:title", default="", namespaces=ATOM)).split()),
                url=f"https://arxiv.org/abs/{arxiv_id}",
            ))
        total = int(root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults", default="0") or 0)
        next_start = start + len(candidates)
        # arXiv rejects start beyond 30000; stop well before.
        has_more = candidates and next_start < min(total, 2000)
        return DiscoveryPage(candidates=candidates, next_cursor={"start": next_start} if has_more else None)
