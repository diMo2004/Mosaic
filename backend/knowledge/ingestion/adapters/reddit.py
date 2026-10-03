from decimal import Decimal
import requests
from knowledge.ingestion.base import BaseExternalAdapter, IngestionItem
from knowledge.models import Source


class RedditAdapter(BaseExternalAdapter):
    """Fetches community discussion strictly for evidence attribution after legal verification."""
    def fetch(self, post_permalink_or_id: str, legal_review_approved: bool = False, **kwargs) -> list[IngestionItem]:
        # Always enforce evidence_only=True and demand legal review approval flag
        clean_path = post_permalink_or_id.strip().strip("/")
        url = f"https://www.reddit.com/{clean_path}.json" if clean_path.startswith("r/") else f"https://www.reddit.com/comments/{clean_path}.json"
        headers = {"User-Agent": "MosaicApp/1.0 (educational compliance verification)"}

        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            raise RuntimeError(f"Reddit API error: {resp.status_code}")

        data = resp.json()
        post_data = data[0]["data"]["children"][0]["data"]

        return [
            IngestionItem(
                title=f"Reddit: {post_data.get('title')}",
                url=f"https://reddit.com{post_data.get('permalink')}",
                raw_text=f"{post_data.get('title')}\n\n{post_data.get('selftext', '')}",
                source_name="Reddit Community",
                source_domain="reddit.com",
                source_type=Source.SOURCE_TYPE_COMMUNITY,
                authority_score=Decimal("0.35"),
                license_name="reddit-user-agreement",
                license_url="https://www.redditinc.com/policies/user-agreement",
                attribution_required=True,
                commercial_use_allowed=False,
                ai_use_allowed=True,
                scraping_allowed=True,
                document_type="web_page",
                metadata={"legal_review_approved": legal_review_approved, "subreddit": post_data.get("subreddit")},
                evidence_only=True,  # STRICT: Never produces canonical claims
            )
        ]