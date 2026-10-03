from decimal import Decimal
import requests
from knowledge.ingestion.base import BaseExternalAdapter, IngestionItem
from knowledge.models import Source


class WikimediaAdapter(BaseExternalAdapter):
    """Fetches articles from Wikipedia/Wikimedia REST API."""
    def fetch(self, page_title: str, **kwargs) -> list[IngestionItem]:
        formatted_title = page_title.strip().replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_title}"
        headers = {"User-Agent": "MosaicKnowledgeBot/1.0 (educational research bot)"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError(f"Wikimedia API error: {resp.status_code} {resp.text}")

        data = resp.json()
        extract = data.get("extract", "")

        return [
            IngestionItem(
                title=f"Wikipedia: {data.get('title')}",
                url=data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{formatted_title}"),
                raw_text=extract,
                source_name="Wikipedia",
                source_domain="en.wikipedia.org",
                source_type=Source.SOURCE_TYPE_EDUCATIONAL,
                authority_score=Decimal("0.80"),
                license_name="cc-by-sa-4.0",
                license_url="https://creativecommons.org/licenses/by-sa/4.0/",
                attribution_required=True,
                commercial_use_allowed=True,
                ai_use_allowed=True,
                scraping_allowed=True,
                document_type="web_page",
                metadata={"pageid": data.get("pageid"), "description": data.get("description")},
            )
        ]