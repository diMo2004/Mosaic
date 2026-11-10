"""Single registry of external adapters used by commands, jobs, and the scheduler."""
from django.conf import settings

from knowledge.ingestion.adapters.arxiv import ArxivAdapter
from knowledge.ingestion.adapters.github import GitHubAdapter
from knowledge.ingestion.adapters.official_docs import OfficialDocumentationAdapter
from knowledge.ingestion.adapters.reddit import RedditAdapter
from knowledge.ingestion.adapters.stackexchange import StackExchangeAdapter
from knowledge.ingestion.adapters.wikimedia import WikimediaAdapter
from knowledge.ingestion.base import BaseExternalAdapter
from knowledge.ingestion.license_checker import SOURCE_POLICIES, is_policy_enabled

ADAPTERS: dict[str, type[BaseExternalAdapter]] = {
    WikimediaAdapter.name: WikimediaAdapter,
    ArxivAdapter.name: ArxivAdapter,
    GitHubAdapter.name: GitHubAdapter,
    StackExchangeAdapter.name: StackExchangeAdapter,
    RedditAdapter.name: RedditAdapter,
    OfficialDocumentationAdapter.name: OfficialDocumentationAdapter,
}

# CLI spellings kept for backwards compatibility with `ingest_external`.
ALIASES = {"official-docs": OfficialDocumentationAdapter.name}


class UnknownAdapterError(KeyError):
    pass


def get_adapter(name: str) -> BaseExternalAdapter:
    name = ALIASES.get(name, name)
    try:
        return ADAPTERS[name]()
    except KeyError as exc:
        raise UnknownAdapterError(name) from exc


def policy_key_for(adapter_name: str, topic: str = "") -> str:
    if adapter_name == OfficialDocumentationAdapter.name:
        return OfficialDocumentationAdapter.policy_key(topic)
    return adapter_name


def topic_enabled(adapter_name: str, topic: str = "") -> bool:
    policy = SOURCE_POLICIES.get(policy_key_for(adapter_name, topic))
    return bool(policy and is_policy_enabled(policy))


def enabled_adapters() -> list[str]:
    """Adapters configured for scheduled discovery whose source policy allows ingestion."""
    configured = getattr(settings, "INGESTION_ENABLED_ADAPTERS", list(ADAPTERS))
    enabled = []
    for name in configured:
        name = ALIASES.get(name, name)
        if name not in ADAPTERS:
            continue
        if name == OfficialDocumentationAdapter.name:
            if any(topic_enabled(name, key) for key in OfficialDocumentationAdapter.fixed_topics()):
                enabled.append(name)
        elif topic_enabled(name):
            enabled.append(name)
    return enabled
