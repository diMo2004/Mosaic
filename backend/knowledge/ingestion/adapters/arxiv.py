from decimal import Decimal
import xml.etree.ElementTree as ET
import requests
from knowledge.ingestion.base import BaseExternalAdapter, IngestionItem
from knowledge.models import Source

class ArxivAdapter(BaseExternalAdapter):
    """Fetches academic computer science preprints from arXiv."""
    def fetch(self, arxiv_id: str, **kwargs) -> list[IngestionItem]:
        url = f"https://export.arxiv.org/api/query?id_list={arxiv_id.strip()}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError(f"arXiv API error: {resp.status_code}")
        root = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entry = root.find("atom:entry", ns)
        if entry is None:
            raise RuntimeError(f"No arXiv record found for id {arxiv_id}")
        title = (entry.find("atom:title", ns).text or "").strip().replace("\n", " ")
        summary = (entry.find("atom:summary", ns).text or "").strip()
        published = entry.find("atom:published", ns).text
        return [
            IngestionItem(
                title=f"arXiv: {title}",
                url=f"https://arxiv.org/abs/{arxiv_id}",
                raw_text=f"Title: {title}\n\nAbstract:\n{summary}",
                source_name="arXiv",
                source_domain="arxiv.org",
                source_type=Source.SOURCE_TYPE_ACADEMIC,
                authority_score=Decimal("0.90"),
                license_name="arxiv-nonexclusive",
                license_url="https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html",
                attribution_required=True,
                commercial_use_allowed=False,
                ai_use_allowed=True,
                scraping_allowed=True,
                document_type="pdf",
                metadata={"arxiv_id": arxiv_id, "published": published},
            )
        ]