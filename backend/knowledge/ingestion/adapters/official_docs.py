"""First-party programming-language documentation adapter.

The registry is deliberately allow-listed: callers cannot turn the adapter into
an arbitrary web scraper, and every item retains its original source URL.
"""
import re
from decimal import Decimal

import requests
from django.utils.html import strip_tags

from knowledge.ingestion.base import BaseExternalAdapter, IngestionItem
from knowledge.models import Source


class OfficialDocumentationAdapter(BaseExternalAdapter):
    DOCUMENTATION = {
        "cpp": ("C++", "https://isocpp.org/", "isocpp.org"),
        "java": ("Java", "https://docs.oracle.com/en/java/", "docs.oracle.com"),
        "python": ("Python", "https://docs.python.org/3/", "docs.python.org"),
        "javascript": ("JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "developer.mozilla.org"),
        "typescript": ("TypeScript", "https://www.typescriptlang.org/docs/", "www.typescriptlang.org"),
    }

    def fetch(self, identifier: str, **kwargs) -> list[IngestionItem]:
        key = identifier.strip().lower().replace("++", "pp")
        if key not in self.DOCUMENTATION:
            raise ValueError("Supported official documentation: cpp, java, python, javascript, typescript.")
        language, url, domain = self.DOCUMENTATION[key]
        response = requests.get(url, headers={"User-Agent": "MosaicKnowledgeBot/1.0"}, timeout=15)
        response.raise_for_status()
        text = re.sub(r"\s+", " ", strip_tags(response.text)).strip()[:50000]
        return [IngestionItem(
            title=f"{language} official documentation",
            url=url,
            raw_text=text,
            source_name=f"{language} official documentation",
            source_domain=domain,
            source_type=Source.SOURCE_TYPE_OFFICIAL,
            authority_score=Decimal("0.95"),
            license_name="official-documentation",
            attribution_required=True,
            commercial_use_allowed=False,
            ai_use_allowed=True,
            scraping_allowed=True,
            document_type="web_page",
            metadata={"language": language, "adapter": "official_docs"},
        )]
