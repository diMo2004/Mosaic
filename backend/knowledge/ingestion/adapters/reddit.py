"""Reddit evidence adapter (disabled unless legally cleared).

Reddit's Data API terms require OAuth access, prohibit using user content to
train AI models, and require a separate agreement for commercial use. This
adapter therefore:

* only runs when REDDIT_LEGAL_REVIEW_APPROVED=True and OAuth app credentials
  are configured (the license checker re-checks the setting per item);
* always marks items evidence_only=True and ai_use_allowed=False, so they never
  become canonical claims, are never sent to an LLM, and are never embedded.
"""
import time
from decimal import Decimal

import requests
from django.conf import settings
from django.core.cache import cache

from knowledge.ingestion.base import BaseExternalAdapter, DiscoveryCandidate, DiscoveryPage, IngestionItem
from knowledge.ingestion.http import PermanentProviderError, TransientProviderError, provider_get, user_agent, wait_for_slot
from knowledge.models import Source

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API_ROOT = "https://oauth.reddit.com"
_TOKEN_CACHE_KEY = "ingest:reddit:token"


class RedditAdapter(BaseExternalAdapter):
    """Fetches community discussion strictly for evidence attribution after legal verification."""
    name = "reddit"

    def _access_token(self) -> str:
        token = cache.get(_TOKEN_CACHE_KEY)
        if token:
            return token
        client_id = getattr(settings, "REDDIT_CLIENT_ID", "")
        client_secret = getattr(settings, "REDDIT_CLIENT_SECRET", "")
        if not (client_id and client_secret):
            raise PermanentProviderError("Reddit OAuth credentials (REDDIT_CLIENT_ID/REDDIT_CLIENT_SECRET) are not configured.")
        wait_for_slot("www.reddit.com")
        try:
            resp = requests.post(
                TOKEN_URL,
                auth=(client_id, client_secret),
                data={"grant_type": "client_credentials"},
                headers={"User-Agent": user_agent()},
                timeout=10,
            )
        except (requests.Timeout, requests.ConnectionError) as exc:
            raise TransientProviderError(f"Reddit token request failed: {exc}") from exc
        if resp.status_code != 200:
            raise PermanentProviderError(f"Reddit token request returned {resp.status_code}.")
        payload = resp.json()
        token = payload.get("access_token", "")
        cache.set(_TOKEN_CACHE_KEY, token, timeout=max(int(payload.get("expires_in", 3600)) - 60, 60))
        return token

    def _headers(self) -> dict:
        return {"Authorization": f"bearer {self._access_token()}"}

    def fetch(self, post_permalink_or_id: str, legal_review_approved: bool = False, **kwargs) -> list[IngestionItem]:
        clean_path = post_permalink_or_id.strip().strip("/")
        url = f"{API_ROOT}/{clean_path}" if clean_path.startswith("r/") else f"{API_ROOT}/comments/{clean_path}"
        data = provider_get(url, params={"limit": 1, "raw_json": 1}, headers=self._headers(), timeout=10, expect_json=True)
        try:
            post_data = data[0]["data"]["children"][0]["data"]
        except (IndexError, KeyError, TypeError) as exc:
            raise PermanentProviderError("Unexpected Reddit payload.") from exc
        approved = bool(legal_review_approved or getattr(settings, "REDDIT_LEGAL_REVIEW_APPROVED", False))

        return [
            IngestionItem(
                title=f"Reddit: {post_data.get('title')}",
                url=f"https://reddit.com{post_data.get('permalink')}",
                raw_text=f"{post_data.get('title')}\n\n{post_data.get('selftext', '')}",
                source_name="Reddit Community",
                source_domain="reddit.com",
                source_type=Source.SOURCE_TYPE_COMMUNITY,
                authority_score=Decimal("0.35"),
                license_name="reddit-data-api-terms",
                license_url="https://redditinc.com/policies/data-api-terms",
                attribution_required=True,
                commercial_use_allowed=False,
                ai_use_allowed=False,
                scraping_allowed=True,
                document_type="web_page",
                metadata={
                    "legal_review_approved": approved,
                    "subreddit": post_data.get("subreddit"),
                    "retrieved_epoch": int(time.time()),
                },
                evidence_only=True,  # STRICT: Never produces canonical claims
                policy_key="reddit",
                external_id=f"reddit:{post_data.get('id')}" if post_data.get("id") else "",
                attribution_text=f"r/{post_data.get('subreddit')} on Reddit",
            )
        ]

    def discover(self, topic: str, cursor=None, limit: int = 5) -> DiscoveryPage:
        subreddits = getattr(settings, "INGESTION_REDDIT_SUBREDDITS", ["compsci", "learnprogramming"])
        cursor = dict(cursor or {})
        sub_index = int(cursor.get("sub_index", 0))
        if sub_index >= len(subreddits):
            return DiscoveryPage(candidates=[], next_cursor=None)
        subreddit = subreddits[sub_index]
        params = {"q": topic, "restrict_sr": 1, "sort": "top", "t": "year", "limit": max(1, min(limit, 25)), "raw_json": 1}
        if cursor.get("after"):
            params["after"] = cursor["after"]
        data = provider_get(f"{API_ROOT}/r/{subreddit}/search", params=params, headers=self._headers(), timeout=10, expect_json=True)
        listing = data.get("data", {})
        candidates = [
            DiscoveryCandidate(
                external_id=f"reddit:{child['data']['id']}",
                identifier=child["data"]["id"],
                title=child["data"].get("title", ""),
                url=f"https://reddit.com{child['data'].get('permalink', '')}",
            )
            for child in listing.get("children", [])
            if child.get("data", {}).get("id")
        ]
        if listing.get("after"):
            next_cursor = {"sub_index": sub_index, "after": listing["after"]}
        else:
            next_cursor = {"sub_index": sub_index + 1} if sub_index + 1 < len(subreddits) else None
        return DiscoveryPage(candidates=candidates, next_cursor=next_cursor)
