import base64
from decimal import Decimal
import requests
from knowledge.ingestion.base import BaseExternalAdapter, IngestionItem
from knowledge.models import Source
import os
from django.conf import settings

class GitHubAdapter(BaseExternalAdapter):
    """Fetches README and doc markdown from GitHub repositories."""
    def __init__(self, token: str | None = None):
        token = token or getattr(settings, "GITHUB_TOKEN", None) or os.getenv("GITHUB_TOKEN", "")
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            self.headers["Authorization"] = f"token {token}"

    def fetch(self, repo_full_name: str, **kwargs) -> list[IngestionItem]:
        repo_url = f"https://api.github.com/repos/{repo_full_name}"
        repo_resp = requests.get(repo_url, headers=self.headers, timeout=10)
        if repo_resp.status_code != 200:
            raise RuntimeError(f"GitHub API error: {repo_resp.status_code} {repo_resp.text}")

        repo_data = repo_resp.json()
        license_info = repo_data.get("license") or {}
        spdx_id = (license_info.get("spdx_id") or "other").lower()
        readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
        readme_resp = requests.get(readme_url, headers=self.headers, timeout=10)
        raw_text = ""
        if readme_resp.status_code == 200:
            content_b64 = readme_resp.json().get("content", "")
            raw_text = base64.b64decode(content_b64).decode("utf-8", errors="replace")

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
                commercial_use_allowed=spdx_id in {"mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause"},
                ai_use_allowed=True,
                scraping_allowed=True,
                document_type="doc",
                metadata={"stars": repo_data.get("stargazers_count"), "default_branch": repo_data.get("default_branch")},
            )
        ]