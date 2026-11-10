import html
import re
from datetime import datetime, timezone
from decimal import Decimal

from django.conf import settings
from django.utils.html import strip_tags

from knowledge.ingestion.base import BaseExternalAdapter, DiscoveryCandidate, DiscoveryPage, IngestionItem
from knowledge.ingestion.http import provider_get
from knowledge.models import Source

API_ROOT = "https://api.stackexchange.com/2.3"
_TOP_LEVEL_SITES = {"stackoverflow", "superuser", "serverfault", "askubuntu"}

# Stack Exchange content license depends on the contribution date.
_CC_BY_SA_3_START = datetime(2011, 4, 8, tzinfo=timezone.utc)
_CC_BY_SA_4_START = datetime(2018, 5, 2, tzinfo=timezone.utc)


def site_domain(site: str) -> str:
    return f"{site}.com" if site in _TOP_LEVEL_SITES else f"{site}.stackexchange.com"


def license_for_post(creation_epoch) -> tuple[str, str]:
    created = datetime.fromtimestamp(int(creation_epoch or 0), tz=timezone.utc) if creation_epoch else None
    if created is not None and created < _CC_BY_SA_3_START:
        return "cc-by-sa-2.5", "https://creativecommons.org/licenses/by-sa/2.5/"
    if created is not None and created < _CC_BY_SA_4_START:
        return "cc-by-sa-3.0", "https://creativecommons.org/licenses/by-sa/3.0/"
    return "cc-by-sa-4.0", "https://creativecommons.org/licenses/by-sa/4.0/"


def _plain_text(body_html: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(strip_tags(body_html or ""))).strip()


class StackExchangeAdapter(BaseExternalAdapter):
    """Fetches high-quality answers from Stack Overflow or CSE Stack Exchange."""
    name = "stackexchange"

    def _params(self, **params) -> dict:
        key = getattr(settings, "STACKEXCHANGE_API_KEY", "")
        if key:
            params["key"] = key
        return params

    def fetch(self, question_id: str, site: str = "stackoverflow", question_title: str = "", **kwargs) -> list[IngestionItem]:
        api_url = f"{API_ROOT}/questions/{question_id}/answers"
        data = provider_get(
            api_url,
            params=self._params(order="desc", sort="votes", site=site, filter="withbody", pagesize=5),
            timeout=10,
            expect_json=True,
        )
        domain = site_domain(site)
        min_score = int(getattr(settings, "INGESTION_STACKEXCHANGE_MIN_ANSWER_SCORE", 5))
        results = []
        for answer in data.get("items", [])[:3]:
            if not answer.get("is_accepted") and int(answer.get("score") or 0) < min_score:
                continue
            license_name, license_url = license_for_post(answer.get("creation_date"))
            author = (answer.get("owner") or {}).get("display_name", "")
            author_link = (answer.get("owner") or {}).get("link", "")
            answer_url = f"https://{domain}/a/{answer.get('answer_id')}"
            title = html.unescape(question_title) if question_title else f"Question {question_id}"
            results.append(
                IngestionItem(
                    title=f"StackExchange ({site}): {title}"[:255],
                    url=answer_url,
                    raw_text=_plain_text(answer.get("body", "")),
                    source_name=f"StackExchange: {site}",
                    source_domain=domain,
                    source_type=Source.SOURCE_TYPE_COMMUNITY,
                    authority_score=Decimal("0.65") if answer.get("is_accepted") else Decimal("0.55"),
                    license_name=license_name,
                    license_url=license_url,
                    attribution_required=True,
                    commercial_use_allowed=True,
                    ai_use_allowed=True,
                    scraping_allowed=True,
                    document_type="web_page",
                    metadata={
                        "score": answer.get("score"),
                        "is_accepted": answer.get("is_accepted"),
                        "author": author,
                        "author_link": author_link,
                        "question_id": question_id,
                        "last_activity_date": answer.get("last_activity_date"),
                    },
                    policy_key="stackexchange",
                    external_id=f"se:{site}:a:{answer.get('answer_id')}",
                    attribution_text=f"Answer by {author or 'a Stack Exchange user'} on Stack Exchange ({license_name.upper()})",
                )
            )
        return results

    def discover(self, topic: str, cursor=None, limit: int = 5, site: str = "stackoverflow") -> DiscoveryPage:
        page = int((cursor or {}).get("page", 1))
        data = provider_get(
            f"{API_ROOT}/search/advanced",
            params=self._params(
                order="desc", sort="votes", q=topic, accepted="True", answers=1,
                site=site, page=page, pagesize=max(1, min(limit, 50)),
            ),
            timeout=10,
            expect_json=True,
        )
        domain = site_domain(site)
        candidates = [
            DiscoveryCandidate(
                external_id=f"se:{site}:q:{question['question_id']}",
                identifier=str(question["question_id"]),
                title=html.unescape(question.get("title", "")),
                url=f"https://{domain}/q/{question['question_id']}",
                fetch_kwargs={"site": site, "question_title": question.get("title", "")[:200]},
            )
            for question in data.get("items", [])
            if question.get("question_id")
        ]
        return DiscoveryPage(candidates=candidates, next_cursor={"page": page + 1} if data.get("has_more") else None)
