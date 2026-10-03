from decimal import Decimal
import requests
from knowledge.ingestion.base import BaseExternalAdapter, IngestionItem
from knowledge.models import Source

class StackExchangeAdapter(BaseExternalAdapter):
    """Fetches high-quality answers from Stack Overflow or CSE Stack Exchange."""
    def fetch(self, question_id: str, site: str = "stackoverflow", **kwargs) -> list[IngestionItem]:
        api_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
        params = {
            "order": "desc",
            "sort": "votes",
            "site": site,
            "filter": "!n0edRLqDYc",
        }
        resp = requests.get(api_url, params=params, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError(f"Stack Exchange API error: {resp.status_code} {resp.text}")

        items = resp.json().get("items", [])
        results = []
        for answer in items[:3]:
            body = answer.get("body_markdown") or answer.get("body", "")
            results.append(
                IngestionItem(
                    title=f"StackExchange ({site}) Question {question_id} Answer",
                    url=f"https://{site}.com/a/{answer.get('answer_id')}",
                    raw_text=body,
                    source_name=f"StackExchange: {site}",
                    source_domain=f"{site}.com",
                    source_type=Source.SOURCE_TYPE_COMMUNITY,
                    authority_score=Decimal("0.65") if answer.get("is_accepted") else Decimal("0.55"),
                    license_name="cc-by-sa-4.0",
                    license_url="https://creativecommons.org/licenses/by-sa/4.0/",
                    attribution_required=True,
                    commercial_use_allowed=True,
                    ai_use_allowed=True,
                    scraping_allowed=True,
                    document_type="web_page",
                    metadata={
                        "score": answer.get("score"),
                        "is_accepted": answer.get("is_accepted"),
                        "author": answer.get("owner", {}).get("display_name"),
                    },
                )
            )
        return results