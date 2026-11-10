import base64
import os
from decimal import Decimal

from django.conf import settings

from knowledge.ingestion.base import BaseExternalAdapter, DiscoveryCandidate, DiscoveryPage, IngestionItem
from knowledge.ingestion.http import PermanentProviderError, provider_get
from knowledge.ingestion.license_checker import PERMISSIVE_CODE_LICENSES
from knowledge.models import Source

SEARCH_URL = "https://api.github.com/search/repositories"


class GitHubAdapter(BaseExternalAdapter):
    """Fetches README and doc markdown from GitHub repositories."""
    name = "github"

    def __init__(self, token: str | None = None):
        token = token or getattr(settings, "GITHUB_TOKEN", None) or os.getenv("GITHUB_TOKEN", "")
        self.headers = {"Accept": "application/vnd.github.v3+json", "X-GitHub-Api-Version": "2022-11-28"}
        if token:
            self.headers["Authorization"] = f"token {token}"

    def fetch(self, repo_full_name: str, **kwargs) -> list[IngestionItem]:
        repo_url = f"https://api.github.com/repos/{repo_full_name}"
        repo_data = provider_get(repo_url, headers=self.headers, timeout=10, expect_json=True)
        license_info = repo_data.get("license") or {}
        spdx_id = (license_info.get("spdx_id") or "other").lower()
        readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
        raw_text = ""
        readme_sha = ""
        try:
            readme = provider_get(readme_url, headers=self.headers, timeout=10, expect_json=True)
            raw_text = base64.b64decode(readme.get("content", "")).decode("utf-8", errors="replace")
            readme_sha = readme.get("sha", "")
        except PermanentProviderError:
            # No README: the pipeline rejects the empty document.
            pass

        owner = (repo_data.get("owner") or {}).get("login", repo_full_name.split("/")[0])
        return [
            IngestionItem(
                title=f"{repo_full_name} Documentation",
                url=repo_data.get("html_url", f"https://github.com/{repo_full_name}"),
                raw_text=raw_text,
                source_name=f"GitHub: {repo_full_name}",
                source_domain="github.com",
                source_type=Source.SOURCE_TYPE_OFFICIAL if repo_data.get("stargazers_count", 0) > 1000 else Source.SOURCE_TYPE_COMMUNITY,
                authority_score=Decimal("0.75"),
                license_name=spdx_id,
                license_url=license_info.get("url") or "https://choosealicense.com",
                attribution_required=True,
                commercial_use_allowed=spdx_id in PERMISSIVE_CODE_LICENSES,
                ai_use_allowed=True,
                scraping_allowed=True,
                document_type="doc",
                metadata={
                    "stars": repo_data.get("stargazers_count"),
                    "default_branch": repo_data.get("default_branch"),
                    "repo_id": repo_data.get("id"),
                    "readme_sha": readme_sha,
                    "pushed_at": repo_data.get("pushed_at"),
                },
                policy_key="github",
                external_id=f"github:{repo_data['id']}" if repo_data.get("id") else "",
                attribution_text=f"{repo_full_name} by {owner} ({license_info.get('spdx_id') or 'unknown license'})",
            )
        ]

    def discover(self, topic: str, cursor=None, limit: int = 5) -> DiscoveryPage:
        page = int((cursor or {}).get("page", 1))
        min_stars = int(getattr(settings, "INGESTION_GITHUB_MIN_STARS", 500))
        query = f"{topic} in:name,description,readme stars:>={min_stars} archived:false fork:false"
        per_page = max(1, min(limit * 2, 50))
        data = provider_get(
            SEARCH_URL,
            params={"q": query, "sort": "stars", "order": "desc", "per_page": per_page, "page": page},
            headers=self.headers,
            timeout=15,
            expect_json=True,
        )
        candidates = []
        for repo in data.get("items", []):
            spdx = ((repo.get("license") or {}).get("spdx_id") or "").lower()
            # Skip repositories whose license would be rejected anyway; saves API quota.
            if spdx not in PERMISSIVE_CODE_LICENSES or not repo.get("id"):
                continue
            candidates.append(DiscoveryCandidate(
                external_id=f"github:{repo['id']}",
                identifier=repo["full_name"],
                title=repo["full_name"],
                url=repo.get("html_url", ""),
            ))
            if len(candidates) >= limit:
                break
        total = min(int(data.get("total_count", 0)), 1000)  # search API caps at 1000 results
        has_more = page * per_page < total
        return DiscoveryPage(candidates=candidates, next_cursor={"page": page + 1} if has_more else None)
