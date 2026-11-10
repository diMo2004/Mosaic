from decimal import Decimal
from urllib.parse import quote

from knowledge.ingestion.base import BaseExternalAdapter, DiscoveryCandidate, DiscoveryPage, IngestionItem
from knowledge.ingestion.http import PermanentProviderError, provider_get
from knowledge.models import Source

SEARCH_API = "https://en.wikipedia.org/w/api.php"


class WikimediaAdapter(BaseExternalAdapter):
    """Fetches articles from Wikipedia/Wikimedia REST API."""
    name = "wikimedia"

    def fetch(self, page_title: str, **kwargs) -> list[IngestionItem]:
        formatted_title = page_title.strip().replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(formatted_title, safe='')}"
        data = provider_get(url, timeout=10, expect_json=True)
        if data.get("type") == "disambiguation":
            raise PermanentProviderError(f"'{page_title}' is a disambiguation page.")
        extract = data.get("extract", "")
        page_url = data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{formatted_title}")

        return [
            IngestionItem(
                title=f"Wikipedia: {data.get('title')}",
                url=page_url,
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
                metadata={
                    "pageid": data.get("pageid"),
                    "description": data.get("description"),
                    "revision": data.get("revision"),
                    "timestamp": data.get("timestamp"),
                },
                policy_key="wikimedia",
                external_id=f"enwiki:{data.get('pageid')}" if data.get("pageid") else "",
                attribution_text=f"\"{data.get('title')}\" by Wikipedia contributors, CC BY-SA 4.0",
            )
        ]

    def discover(self, topic: str, cursor=None, limit: int = 5) -> DiscoveryPage:
        offset = int((cursor or {}).get("sroffset", 0))
        data = provider_get(
            SEARCH_API,
            params={
                "action": "query",
                "list": "search",
                "srsearch": topic,
                "srnamespace": 0,
                "srlimit": max(1, min(limit, 50)),
                "sroffset": offset,
                "format": "json",
                "formatversion": 2,
            },
            timeout=10,
            expect_json=True,
        )
        results = data.get("query", {}).get("search", [])
        candidates = [
            DiscoveryCandidate(
                external_id=f"enwiki:{result['pageid']}",
                identifier=result["title"],
                title=result["title"],
                url=f"https://en.wikipedia.org/wiki/{quote(result['title'].replace(' ', '_'))}",
            )
            for result in results
            if result.get("pageid") and result.get("title")
        ]
        next_offset = data.get("continue", {}).get("sroffset")
        return DiscoveryPage(
            candidates=candidates,
            next_cursor={"sroffset": int(next_offset)} if next_offset is not None else None,
        )
