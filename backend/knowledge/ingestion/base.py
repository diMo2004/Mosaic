from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Optional

@dataclass
class IngestionItem:
    title: str
    url: str
    raw_text: str
    source_name: str
    source_domain: str
    source_type: str
    authority_score: Decimal
    license_name: str
    license_url: str = ""
    attribution_required: bool = True
    commercial_use_allowed: bool = False
    ai_use_allowed: bool = True
    scraping_allowed: bool = True
    document_type: str = "web_page"
    metadata: dict[str, Any] = field(default_factory=dict)
    evidence_only: bool = False

class BaseExternalAdapter(ABC):
    @abstractmethod
    def fetch(self, identifier: str, **kwargs) -> list[IngestionItem]:
        """Fetch content given an identifier (URL, repo, article title, etc.)."""
        pass