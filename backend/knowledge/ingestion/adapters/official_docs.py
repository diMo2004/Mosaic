"""First-party programming-language documentation adapter.

The registry is deliberately allow-listed: callers cannot turn the adapter into
an arbitrary web scraper, and every item retains its original source URL.

Discovery walks each language's official index (Sphinx ``objects.inv`` for
Python, published sitemaps for MDN and TypeScript). Page fetches must stay on
the configured domain and path prefix and are checked against robots.txt.
Oracle Java and isocpp.org are retained in the registry, but their terms do not
license reuse, so the source policy blocks them until a documented review.
"""
import gzip
import html
import re
import time
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from urllib.parse import urljoin, urlsplit

from django.utils.html import strip_tags

from knowledge.ingestion.base import BaseExternalAdapter, DiscoveryCandidate, DiscoveryPage, IngestionItem
from knowledge.ingestion.http import AccessDisallowedError, PermanentProviderError, provider_get, robots_allows
from knowledge.models import Source

MAX_INDEX_URLS = 3000
INDEX_REFRESH_SECONDS = 7 * 24 * 3600
_SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


@dataclass(frozen=True)
class DocSource:
    language: str
    url: str
    domain: str
    license_name: str
    license_url: str
    attribution: str
    path_prefix: str
    index_url: Optional[str] = None
    index_format: str = ""  # "sphinx_inventory" | "sitemap"


class OfficialDocumentationAdapter(BaseExternalAdapter):
    name = "official_docs"

    DOCUMENTATION = {
        "cpp": DocSource(
            "C++", "https://isocpp.org/", "isocpp.org", "isocpp-terms-of-use",
            "https://isocpp.org/home/terms-of-use", "Standard C++ Foundation", "/",
        ),
        "java": DocSource(
            "Java", "https://docs.oracle.com/en/java/", "docs.oracle.com", "oracle-documentation",
            "https://docs.oracle.com/en/java/javase/21/docs/legal/copyright.html", "Oracle", "/en/java/",
        ),
        "python": DocSource(
            "Python", "https://docs.python.org/3/", "docs.python.org", "psf-2.0",
            "https://docs.python.org/3/license.html", "Python Software Foundation", "/3/",
            index_url="https://docs.python.org/3/objects.inv", index_format="sphinx_inventory",
        ),
        "javascript": DocSource(
            "JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "developer.mozilla.org",
            "cc-by-sa-2.5", "https://creativecommons.org/licenses/by-sa/2.5/", "Mozilla Contributors",
            "/en-US/docs/Web/JavaScript", index_url="https://developer.mozilla.org/sitemap.xml", index_format="sitemap",
        ),
        "typescript": DocSource(
            "TypeScript", "https://www.typescriptlang.org/docs/", "www.typescriptlang.org", "cc-by-4.0",
            "https://creativecommons.org/licenses/by/4.0/", "TypeScript documentation contributors", "/docs/",
            index_url="https://www.typescriptlang.org/sitemap-index.xml", index_format="sitemap",
        ),
    }

    @classmethod
    def _source(cls, identifier: str) -> tuple[str, DocSource]:
        key = identifier.strip().lower().replace("++", "pp")
        if key not in cls.DOCUMENTATION:
            raise ValueError("Supported official documentation: cpp, java, python, javascript, typescript.")
        return key, cls.DOCUMENTATION[key]

    @staticmethod
    def policy_key(key: str) -> str:
        return f"official_docs:{key}"

    @classmethod
    def fixed_topics(cls) -> list[str]:
        """Discovery is keyed by language, not by taxonomy topic."""
        return list(cls.DOCUMENTATION)

    def _check_url(self, doc: DocSource, url: str) -> str:
        parts = urlsplit(url)
        if parts.scheme != "https" or (parts.hostname or "").lower() != doc.domain or not parts.path.startswith(doc.path_prefix):
            raise AccessDisallowedError(f"{url} is outside the allow-listed {doc.language} documentation.")
        if not robots_allows(url):
            raise AccessDisallowedError(f"robots.txt disallows {url}.")
        return url.split("#", 1)[0]

    def fetch(self, identifier: str, url: str | None = None, **kwargs) -> list[IngestionItem]:
        key, doc = self._source(identifier)
        page_url = self._check_url(doc, url or doc.url)
        response = provider_get(page_url, timeout=15)
        title, text = extract_main_text(response.text)
        return [IngestionItem(
            title=(f"{doc.language} docs: {title}" if title else f"{doc.language} official documentation")[:255],
            url=page_url,
            raw_text=text[:50000],
            source_name=f"{doc.language} official documentation",
            source_domain=doc.domain,
            source_type=Source.SOURCE_TYPE_OFFICIAL,
            authority_score=Decimal("0.95"),
            license_name=doc.license_name,
            license_url=doc.license_url,
            attribution_required=True,
            commercial_use_allowed=key in {"python", "javascript", "typescript"},
            ai_use_allowed=True,
            scraping_allowed=True,
            document_type="web_page",
            metadata={"language": doc.language, "adapter": "official_docs", "last_modified": response.headers.get("Last-Modified", "")},
            policy_key=self.policy_key(key),
            external_id=f"docs:{key}:{urlsplit(page_url).path}",
            attribution_text=f"{doc.attribution}, {doc.language} documentation",
        )]

    def discover(self, topic: str, cursor=None, limit: int = 5) -> DiscoveryPage:
        key, doc = self._source(topic)
        if not doc.index_url:
            # No permitted index is configured; the landing page is the only page.
            if cursor:
                return DiscoveryPage(candidates=[], next_cursor=None)
            return DiscoveryPage(
                candidates=[DiscoveryCandidate(external_id=f"docs:{key}:{urlsplit(doc.url).path}", identifier=key, url=doc.url, fetch_kwargs={"url": doc.url})],
                next_cursor=None,
            )

        cursor = dict(cursor or {})
        urls = cursor.get("urls")
        if not urls or time.time() - float(cursor.get("indexed_at", 0)) > INDEX_REFRESH_SECONDS:
            urls = self._load_index(doc)
            cursor = {"urls": urls, "indexed_at": time.time(), "offset": 0}
        offset = int(cursor.get("offset", 0))
        batch = urls[offset:offset + limit]
        candidates = [
            DiscoveryCandidate(
                external_id=f"docs:{key}:{urlsplit(url).path}",
                identifier=key,
                url=url,
                fetch_kwargs={"url": url},
            )
            for url in batch
        ]
        cursor["offset"] = offset + len(batch)
        # Once the index is walked, discovery starts over after the index refresh
        # window so changed pages are re-checked (unchanged ones are deduplicated).
        next_cursor = cursor if cursor["offset"] < len(urls) else None
        return DiscoveryPage(candidates=candidates, next_cursor=next_cursor)

    def _load_index(self, doc: DocSource) -> list[str]:
        if doc.index_format == "sphinx_inventory":
            urls = parse_sphinx_inventory(provider_get(doc.index_url, timeout=20).content, base_url=doc.index_url)
        else:
            urls = self._sitemap_urls(doc.index_url, doc, depth=0)
        seen, result = set(), []
        for url in urls:
            parts = urlsplit(url)
            clean = url.split("#", 1)[0]
            if (parts.hostname or "").lower() == doc.domain and parts.path.startswith(doc.path_prefix) and clean not in seen:
                seen.add(clean)
                result.append(clean)
            if len(result) >= MAX_INDEX_URLS:
                break
        return result

    def _sitemap_urls(self, sitemap_url: str, doc: DocSource, depth: int) -> list[str]:
        content = provider_get(sitemap_url, timeout=30).content
        if content[:2] == b"\x1f\x8b":
            content = gzip.decompress(content)
        try:
            root = ET.fromstring(content)
        except ET.ParseError as exc:
            raise PermanentProviderError(f"Invalid sitemap at {sitemap_url}") from exc
        if root.tag.endswith("sitemapindex"):
            if depth >= 1:
                return []
            nested = [loc.text.strip() for loc in root.iter(f"{_SITEMAP_NS}loc") if loc.text]
            # Locale-specific sitemaps (e.g. MDN /sitemaps/en-us/) first.
            nested.sort(key=lambda loc: 0 if "en-us" in loc.lower() else 1)
            urls = []
            for loc in nested[:5]:
                urls.extend(self._sitemap_urls(loc, doc, depth + 1))
                if len(urls) >= MAX_INDEX_URLS * 4:
                    break
            return urls
        return [loc.text.strip() for loc in root.iter(f"{_SITEMAP_NS}loc") if loc.text]


def parse_sphinx_inventory(data: bytes, base_url: str) -> list[str]:
    """Return documentation page URLs (std:doc entries) from a Sphinx objects.inv."""
    lines = data.split(b"\n", 4)
    if len(lines) < 5 or not lines[0].startswith(b"# Sphinx inventory version 2"):
        raise PermanentProviderError("Unsupported Sphinx inventory format.")
    try:
        body = zlib.decompress(lines[4]).decode("utf-8", errors="replace")
    except zlib.error as exc:
        raise PermanentProviderError("Corrupt Sphinx inventory.") from exc
    urls = []
    entry = re.compile(r"^(?P<name>.+?)\s+std:doc\s+-?\d+\s+(?P<uri>\S+)")
    for line in body.splitlines():
        match = entry.match(line)
        if not match:
            continue
        uri = match.group("uri")
        if uri.endswith("$"):
            uri = uri[:-1] + match.group("name")
        urls.append(urljoin(base_url, uri))
    return urls


_DROP_BLOCKS = re.compile(r"<(script|style|noscript|nav|header|footer|aside|svg|form)\b.*?</\1\s*>", re.IGNORECASE | re.DOTALL)
_MAIN_START = re.compile(r'<main\b|<article\b|<[a-z]+\b[^>]*\brole="main"', re.IGNORECASE)
_MAIN_END = re.compile(r'</main>|</article>|<div class="sphinxsidebar"|<div class="footer"', re.IGNORECASE)
_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def extract_main_text(page_html: str) -> tuple[str, str]:
    title_match = _TITLE.search(page_html)
    title = " ".join(html.unescape(strip_tags(title_match.group(1))).split()) if title_match else ""
    title = re.split(r"\s+[|—–-]\s+", title)[0] if title else ""
    body = _DROP_BLOCKS.sub(" ", page_html)
    start = _MAIN_START.search(body)
    if start:
        body = body[start.start():]
        end = _MAIN_END.search(body)
        if end:
            body = body[:end.start()]
    text = re.sub(r"\s+", " ", html.unescape(strip_tags(body))).strip()
    return title, text
