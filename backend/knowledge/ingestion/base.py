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
    # Reviewed source-policy key (see license_checker.SOURCE_POLICIES). When
    # blank, the policy is resolved from source_domain, but the declared
    # license must still be one the policy accepts.
    policy_key: str = ""
    # Stable provider identifier (e.g. "enwiki:12345", "arxiv:2301.00001").
    external_id: str = ""
    # Human-readable attribution line (author / contributors) for CC BY-style licenses.
    attribution_text: str = ""


@dataclass
class DiscoveryCandidate:
    """A provider record found by discovery, to be fetched later by an ingestion job."""
    external_id: str
    identifier: str
    title: str = ""
    url: str = ""
    fetch_kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiscoveryPage:
    candidates: list[DiscoveryCandidate]
    # Opaque, JSON-serialisable checkpoint for the next page. None means the
    # query has no further results.
    next_cursor: Optional[dict[str, Any]] = None


class BaseExternalAdapter(ABC):
    #: Registry name; also the IngestionJob.adapter value.
    name: str = ""

    @abstractmethod
    def fetch(self, identifier: str, **kwargs) -> list[IngestionItem]:
        """Fetch content given an identifier (URL, repo, article title, etc.)."""
        pass

    def discover(self, topic: str, cursor: Optional[dict] = None, limit: int = 5) -> DiscoveryPage:
        """Return candidate records for a CSE taxonomy topic, resuming from cursor."""
        raise NotImplementedError(f"{type(self).__name__} does not support discovery.")
