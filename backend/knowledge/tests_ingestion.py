import gzip
import zlib
from datetime import timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

import requests
from django.core.cache import cache
from django.db import IntegrityError
from django.test import TestCase, override_settings
from django.utils import timezone

from knowledge.ingestion.adapters.arxiv import ArxivAdapter
from knowledge.ingestion.adapters.github import GitHubAdapter
from knowledge.ingestion.adapters.official_docs import OfficialDocumentationAdapter, extract_main_text, parse_sphinx_inventory
from knowledge.ingestion.adapters.reddit import RedditAdapter
from knowledge.ingestion.adapters.stackexchange import StackExchangeAdapter, license_for_post
from knowledge.ingestion.adapters.wikimedia import WikimediaAdapter
from knowledge.ingestion.base import DiscoveryCandidate, DiscoveryPage, IngestionItem
from knowledge.ingestion.http import (
    AccessDisallowedError,
    PermanentProviderError,
    RateLimitedError,
    TransientProviderError,
    provider_get,
)
from knowledge.ingestion.jobs import DiscoveryService, IngestionJobService, JobRetry, recover_stale_jobs
from knowledge.ingestion.license_checker import LicenseChecker, LicensePolicyError
from knowledge.ingestion.pipeline import ExternalIngestionPipeline, InsufficientContentError
from knowledge.ingestion.registry import enabled_adapters
from knowledge.models import (
    Concept,
    Evidence,
    ExtractedClaim,
    IngestionJob,
    Source,
    SourceDiscoveryCheckpoint,
    SourceDocument,
)

NO_RATE_LIMIT = override_settings(
    INGESTION_DEFAULT_MIN_INTERVAL_SECONDS=0,
    INGESTION_DOMAIN_MIN_INTERVAL_SECONDS={},
)
HTTP_GET = "knowledge.ingestion.http.requests.get"


def fake_response(status=200, json_data=None, text="", content=None, headers=None):
    response = MagicMock()
    response.status_code = status
    response.headers = headers or {}
    if json_data is not None:
        response.json.return_value = json_data
    else:
        response.json.side_effect = ValueError("not json")
    response.text = text
    response.content = content if content is not None else text.encode("utf-8")
    return response


def wiki_item(**overrides):
    values = dict(
        title="Wikipedia: Binary search tree",
        url="https://en.wikipedia.org/wiki/Binary_search_tree",
        raw_text="A binary search tree keeps keys in sorted order. Lookup takes time proportional to tree height.",
        source_name="Wikipedia",
        source_domain="en.wikipedia.org",
        source_type=Source.SOURCE_TYPE_EDUCATIONAL,
        authority_score=Decimal("0.80"),
        license_name="cc-by-sa-4.0",
        commercial_use_allowed=True,
        policy_key="wikimedia",
    )
    values.update(overrides)
    return IngestionItem(**values)


class ExternalIngestionTests(TestCase):
    def test_license_checker_blocks_unauthorized_reddit(self):
        item = IngestionItem(
            title="Reddit Discussion",
            url="https://reddit.com/r/compsci/123",
            raw_text="Some discussion",
            source_name="Reddit",
            source_domain="reddit.com",
            source_type=Source.SOURCE_TYPE_COMMUNITY,
            authority_score=Decimal("0.30"),
            license_name="reddit-license",
            evidence_only=False,  # Violation: Reddit must be evidence only
            metadata={"legal_review_approved": False},
        )
        with self.assertRaises(LicensePolicyError):
            LicenseChecker.validate(item)

    def test_license_checker_allows_open_source(self):
        item = IngestionItem(
            title="Wikipedia Article",
            url="https://en.wikipedia.org/wiki/Tree",
            raw_text="A tree is a data structure...",
            source_name="Wikipedia",
            source_domain="en.wikipedia.org",
            source_type=Source.SOURCE_TYPE_EDUCATIONAL,
            authority_score=Decimal("0.80"),
            license_name="cc-by-sa-4.0",
        )
        # Should not raise
        LicenseChecker.validate(item)

    @patch("verification.services.claim_verification.ClaimVerificationService.verify_claim")
    @patch("verification.services.claim_extraction.ClaimExtractionService.extract_claims")
    def test_pipeline_creates_source_document_and_extracts_claims(self, mock_extract, mock_verify):
        mock_extract.return_value = ["A binary search tree has ordered nodes."]
        mock_verify.return_value = {"status": "supported"}

        pipeline = ExternalIngestionPipeline()
        item = IngestionItem(
            title="BST Guide",
            url="https://github.com/example/algo",
            raw_text="A binary search tree has ordered nodes.",
            source_name="GitHub: example/algo",
            source_domain="github.com",
            source_type=Source.SOURCE_TYPE_OFFICIAL,
            authority_score=Decimal("0.75"),
            license_name="mit",
        )

        res = pipeline.ingest_item(item)
        self.assertEqual(SourceDocument.objects.count(), 1)
        doc = SourceDocument.objects.first()
        self.assertIsNone(doc.uploaded_note)
        self.assertEqual(doc.title, "BST Guide")
        self.assertEqual(len(res["claims"]), 1)


class LicensePolicyTests(TestCase):
    def test_unknown_domain_fails_closed(self):
        with self.assertRaisesMessage(LicensePolicyError, "No reviewed source policy"):
            LicenseChecker.validate(wiki_item(policy_key="", source_domain="example.org"))

    def test_missing_license_rejected(self):
        with self.assertRaisesMessage(LicensePolicyError, "declares no license"):
            LicenseChecker.validate(wiki_item(license_name=""))

    def test_license_must_match_policy(self):
        item = wiki_item(policy_key="github", source_domain="github.com", license_name="gpl-3.0")
        with self.assertRaisesMessage(LicensePolicyError, "not accepted"):
            LicenseChecker.validate(item)

    def test_policy_key_must_cover_domain(self):
        with self.assertRaisesMessage(LicensePolicyError, "not covered"):
            LicenseChecker.validate(wiki_item(source_domain="github.com"))

    def test_arxiv_requires_cc0_metadata_license(self):
        item = wiki_item(policy_key="arxiv", source_domain="arxiv.org", license_name="arxiv-nonexclusive")
        with self.assertRaises(LicensePolicyError):
            LicenseChecker.validate(item)
        LicenseChecker.validate(wiki_item(policy_key="arxiv", source_domain="arxiv.org", license_name="cc0-1.0"))

    def test_official_docs_python_allowed_java_and_cpp_require_review(self):
        LicenseChecker.validate(wiki_item(policy_key="official_docs:python", source_domain="docs.python.org", license_name="psf-2.0"))
        java = wiki_item(policy_key="official_docs:java", source_domain="docs.oracle.com", license_name="oracle-documentation")
        cpp = wiki_item(policy_key="official_docs:cpp", source_domain="isocpp.org", license_name="isocpp-terms-of-use")
        for item in (java, cpp):
            with self.assertRaisesMessage(LicensePolicyError, "requires a documented legal review"):
                LicenseChecker.validate(item)
        with override_settings(INGESTION_REVIEWED_SOURCES=["official_docs:java"]):
            LicenseChecker.validate(java)

    def test_generic_official_documentation_license_rejected(self):
        item = wiki_item(policy_key="official_docs:python", source_domain="docs.python.org", license_name="official-documentation")
        with self.assertRaises(LicensePolicyError):
            LicenseChecker.validate(item)

    def test_ai_use_and_scraping_flags_enforced(self):
        with self.assertRaisesMessage(LicensePolicyError, "AI processing"):
            LicenseChecker.validate(wiki_item(ai_use_allowed=False))
        with self.assertRaisesMessage(LicensePolicyError, "Automated retrieval"):
            LicenseChecker.validate(wiki_item(scraping_allowed=False))

    def test_attribution_cannot_be_disabled_for_cc_by_sa(self):
        with self.assertRaisesMessage(LicensePolicyError, "requires attribution"):
            LicenseChecker.validate(wiki_item(attribution_required=False))

    def test_commercial_requirement_is_configurable(self):
        item = wiki_item(policy_key="github", source_domain="github.com", license_name="mit", commercial_use_allowed=False)
        LicenseChecker.validate(item)
        with override_settings(INGESTION_REQUIRE_COMMERCIAL_USE=True):
            with self.assertRaisesMessage(LicensePolicyError, "Commercial use"):
                LicenseChecker.validate(item)

    def _reddit_item(self, **overrides):
        values = dict(
            title="Reddit: thread", url="https://reddit.com/r/compsci/comments/abc", raw_text="Discussion text here.",
            source_name="Reddit Community", source_domain="reddit.com", source_type=Source.SOURCE_TYPE_COMMUNITY,
            authority_score=Decimal("0.35"), license_name="reddit-data-api-terms", ai_use_allowed=False,
            evidence_only=True, metadata={"legal_review_approved": True}, policy_key="reddit",
        )
        values.update(overrides)
        return IngestionItem(**values)

    def test_reddit_blocked_without_settings_flag(self):
        with self.assertRaisesMessage(LicensePolicyError, "REDDIT_LEGAL_REVIEW_APPROVED"):
            LicenseChecker.validate(self._reddit_item())

    @override_settings(REDDIT_LEGAL_REVIEW_APPROVED=True)
    def test_reddit_evidence_only_rules(self):
        decision = LicenseChecker.evaluate(self._reddit_item())
        self.assertEqual(decision.mode, "evidence_only")
        with self.assertRaisesMessage(LicensePolicyError, "evidence only"):
            LicenseChecker.validate(self._reddit_item(evidence_only=False))
        with self.assertRaisesMessage(LicensePolicyError, "does not permit"):
            LicenseChecker.validate(self._reddit_item(ai_use_allowed=True))
        with self.assertRaisesMessage(LicensePolicyError, "legal_review_approved"):
            LicenseChecker.validate(self._reddit_item(metadata={}))

    def test_decision_metadata_records_attribution(self):
        decision = LicenseChecker.evaluate(wiki_item(attribution_text="by Wikipedia contributors"))
        meta = decision.as_metadata(wiki_item(attribution_text="by Wikipedia contributors"))
        self.assertEqual(meta["policy_key"], "wikimedia")
        self.assertEqual(meta["license"], "cc-by-sa-4.0")
        self.assertEqual(meta["redistribution"], "share_alike_with_attribution")
        self.assertTrue(meta["self_attestation"])

    def test_enabled_adapters_excludes_unapproved_reddit(self):
        self.assertNotIn("reddit", enabled_adapters())
        self.assertIn("wikimedia", enabled_adapters())


@NO_RATE_LIMIT
class ProviderHttpTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_rate_limit_sets_cooldown(self):
        with patch(HTTP_GET, return_value=fake_response(429, headers={"Retry-After": "90"})):
            with self.assertRaises(RateLimitedError) as ctx:
                provider_get("https://api.example.com/x")
        self.assertGreaterEqual(ctx.exception.retry_after, 90)
        with patch(HTTP_GET) as get:
            with self.assertRaises(RateLimitedError):
                provider_get("https://api.example.com/y")
            get.assert_not_called()

    def test_failure_classification(self):
        with patch(HTTP_GET, return_value=fake_response(502)):
            with self.assertRaises(TransientProviderError):
                provider_get("https://a.example.com/")
        with patch(HTTP_GET, return_value=fake_response(404)):
            with self.assertRaises(PermanentProviderError):
                provider_get("https://b.example.com/")
        with patch(HTTP_GET, side_effect=requests.Timeout("slow")):
            with self.assertRaises(TransientProviderError):
                provider_get("https://c.example.com/")

    def test_stackexchange_backoff_and_throttle(self):
        with patch(HTTP_GET, return_value=fake_response(200, json_data={"items": [], "backoff": 30})):
            provider_get("https://api.stackexchange.com/2.3/search/advanced", expect_json=True)
        with self.assertRaises(RateLimitedError):
            provider_get("https://api.stackexchange.com/2.3/questions", expect_json=True)
        cache.clear()
        throttle = fake_response(400, json_data={"error_id": 502, "error_name": "throttle_violation"})
        with patch(HTTP_GET, return_value=throttle):
            with self.assertRaises(RateLimitedError):
                provider_get("https://api.stackexchange.com/2.3/questions", expect_json=True)

    def test_user_agent_is_sent(self):
        with override_settings(INGESTION_USER_AGENT="MosaicTest/1.0 (ops@example.com)"):
            with patch(HTTP_GET, return_value=fake_response(200, text="ok")) as get:
                provider_get("https://d.example.com/")
        self.assertEqual(get.call_args.kwargs["headers"]["User-Agent"], "MosaicTest/1.0 (ops@example.com)")


ARXIV_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
  <opensearch:totalResults>3</opensearch:totalResults>
  <entry>
    <id>http://arxiv.org/abs/2301.00001v2</id>
    <title>Fast  Binary
      Search Trees</title>
    <summary>We study binary search trees.</summary>
    <published>2023-01-01T00:00:00Z</published>
    <updated>2023-02-01T00:00:00Z</updated>
    <author><name>Ada Lovelace</name></author>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2301.00002v1</id>
    <title>Second</title>
    <summary>Another abstract.</summary>
  </entry>
</feed>"""


@NO_RATE_LIMIT
class AdapterDiscoveryTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_wikimedia_discovery_paginates_with_sroffset(self):
        payload = {"continue": {"sroffset": 2}, "query": {"search": [
            {"pageid": 1, "title": "Binary search tree"}, {"pageid": 2, "title": "AVL tree"},
        ]}}
        with patch(HTTP_GET, return_value=fake_response(json_data=payload)) as get:
            page = WikimediaAdapter().discover("binary search tree", cursor={"sroffset": 0}, limit=2)
        self.assertEqual([c.external_id for c in page.candidates], ["enwiki:1", "enwiki:2"])
        self.assertEqual(page.next_cursor, {"sroffset": 2})
        self.assertEqual(get.call_args.kwargs["params"]["srsearch"], "binary search tree")
        with patch(HTTP_GET, return_value=fake_response(json_data={"query": {"search": []}})):
            self.assertIsNone(WikimediaAdapter().discover("x", cursor={"sroffset": 2}).next_cursor)

    def test_wikimedia_fetch_rejects_disambiguation(self):
        with patch(HTTP_GET, return_value=fake_response(json_data={"type": "disambiguation", "title": "Tree"})):
            with self.assertRaises(PermanentProviderError):
                WikimediaAdapter().fetch("Tree")

    def test_arxiv_discovery_and_fetch(self):
        with patch(HTTP_GET, return_value=fake_response(text=ARXIV_FEED)):
            page = ArxivAdapter().discover("binary search tree", limit=2)
        self.assertEqual([c.identifier for c in page.candidates], ["2301.00001", "2301.00002"])
        self.assertEqual(page.next_cursor, {"start": 2})
        with patch(HTTP_GET, return_value=fake_response(text=ARXIV_FEED)):
            item = ArxivAdapter().fetch("2301.00001v2")[0]
        self.assertEqual(item.url, "https://arxiv.org/abs/2301.00001")
        self.assertEqual(item.license_name, "cc0-1.0")
        self.assertEqual(item.external_id, "arxiv:2301.00001")
        self.assertIn("Fast Binary Search Trees", item.raw_text)
        LicenseChecker.validate(item)

    def test_github_discovery_skips_non_permissive_licenses(self):
        payload = {"total_count": 2, "items": [
            {"id": 10, "full_name": "a/gpl", "license": {"spdx_id": "GPL-3.0"}},
            {"id": 11, "full_name": "b/mit", "html_url": "https://github.com/b/mit", "license": {"spdx_id": "MIT"}},
        ]}
        with patch(HTTP_GET, return_value=fake_response(json_data=payload)):
            page = GitHubAdapter(token="t").discover("graph algorithms", limit=5)
        self.assertEqual([c.external_id for c in page.candidates], ["github:11"])
        self.assertIsNone(page.next_cursor)

    def test_github_unknown_license_is_rejected_by_policy(self):
        def route(url, **kwargs):
            if url.endswith("/readme"):
                return fake_response(404)
            return fake_response(json_data={"id": 5, "html_url": "https://github.com/x/y", "license": None})
        with patch(HTTP_GET, side_effect=route):
            item = GitHubAdapter(token="t").fetch("x/y")[0]
        self.assertEqual(item.license_name, "other")
        with self.assertRaises(LicensePolicyError):
            LicenseChecker.validate(item)

    def test_stackexchange_discovery_and_license_by_date(self):
        payload = {"has_more": True, "items": [{"question_id": 42, "title": "What is a heap?"}]}
        with patch(HTTP_GET, return_value=fake_response(json_data=payload)):
            page = StackExchangeAdapter().discover("heap", limit=1)
        self.assertEqual(page.candidates[0].external_id, "se:stackoverflow:q:42")
        self.assertEqual(page.candidates[0].fetch_kwargs["site"], "stackoverflow")
        self.assertEqual(page.next_cursor, {"page": 2})
        self.assertEqual(license_for_post(1262304000)[0], "cc-by-sa-2.5")  # 2010-01-01
        self.assertEqual(license_for_post(1420070400)[0], "cc-by-sa-3.0")  # 2015-01-01
        self.assertEqual(license_for_post(1609459200)[0], "cc-by-sa-4.0")  # 2021-01-01

    def test_stackexchange_fetch_filters_low_score_and_sets_domain(self):
        payload = {"items": [
            {"answer_id": 1, "is_accepted": True, "score": 1, "body": "<p>A heap is a tree.</p>", "creation_date": 1609459200,
             "owner": {"display_name": "Grace"}},
            {"answer_id": 2, "is_accepted": False, "score": 0, "body": "<p>meh</p>"},
        ]}
        with patch(HTTP_GET, return_value=fake_response(json_data=payload)):
            items = StackExchangeAdapter().fetch("42", site="cs", question_title="What is a heap?")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].source_domain, "cs.stackexchange.com")
        self.assertEqual(items[0].raw_text, "A heap is a tree.")
        self.assertIn("Grace", items[0].attribution_text)
        LicenseChecker.validate(items[0])

    def test_reddit_requires_oauth_credentials(self):
        with override_settings(REDDIT_CLIENT_ID="", REDDIT_CLIENT_SECRET=""):
            with self.assertRaises(PermanentProviderError):
                RedditAdapter().discover("recursion")

    def test_sphinx_inventory_parsing(self):
        body = "tutorial/datastructures std:doc -1 tutorial/datastructures.html Data Structures\n" \
               "list.append py:method 1 library/stdtypes.html#$ -\n" \
               "library/functions std:doc -1 library/functions.html Built-in Functions\n"
        data = b"# Sphinx inventory version 2\n# Project: Python\n# Version: 3.13\n# zlib\n" + zlib.compress(body.encode())
        urls = parse_sphinx_inventory(data, base_url="https://docs.python.org/3/objects.inv")
        self.assertEqual(urls, [
            "https://docs.python.org/3/tutorial/datastructures.html",
            "https://docs.python.org/3/library/functions.html",
        ])

    def test_official_docs_discovery_walks_index_with_cursor(self):
        body = "".join(f"page{i} std:doc -1 page{i}.html P{i}\n" for i in range(3))
        inventory = b"# Sphinx inventory version 2\n# P\n# V\n# z\n" + zlib.compress(body.encode())
        with patch(HTTP_GET, return_value=fake_response(content=inventory)):
            first = OfficialDocumentationAdapter().discover("python", limit=2)
        self.assertEqual(len(first.candidates), 2)
        self.assertEqual(first.next_cursor["offset"], 2)
        with patch(HTTP_GET) as get:
            second = OfficialDocumentationAdapter().discover("python", cursor=first.next_cursor, limit=2)
            get.assert_not_called()  # cached index reused from the checkpoint
        self.assertEqual(second.candidates[0].fetch_kwargs["url"], "https://docs.python.org/3/page2.html")
        self.assertIsNone(second.next_cursor)

    def test_official_docs_sitemap_index_is_filtered_to_prefix(self):
        index = b"""<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://developer.mozilla.org/sitemaps/en-us/sitemap.xml.gz</loc></sitemap></sitemapindex>"""
        urlset = gzip.compress(b"""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url><loc>https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures</loc></url>
            <url><loc>https://developer.mozilla.org/en-US/docs/Web/CSS/color</loc></url></urlset>""")

        def route(url, **kwargs):
            return fake_response(content=urlset if url.endswith(".gz") else index)
        with patch(HTTP_GET, side_effect=route):
            page = OfficialDocumentationAdapter().discover("javascript", limit=10)
        self.assertEqual([c.url for c in page.candidates], ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures"])

    def test_official_docs_fetch_enforces_allowlist_and_robots(self):
        adapter = OfficialDocumentationAdapter()
        with self.assertRaises(AccessDisallowedError):
            adapter.fetch("python", url="https://evil.example.com/3/x.html")
        with self.assertRaises(AccessDisallowedError):
            adapter.fetch("python", url="https://docs.python.org/2.7/tutorial.html")

        def route(url, **kwargs):
            if url.endswith("robots.txt"):
                return fake_response(text="User-agent: *\nDisallow: /3/private/\n")
            return fake_response(text="<html><title>Data Structures — Python</title><nav>menu</nav>"
                                      '<div role="main"><p>Lists are mutable sequences.</p></div><footer>f</footer></html>')
        with patch(HTTP_GET, side_effect=route):
            with self.assertRaises(AccessDisallowedError):
                adapter.fetch("python", url="https://docs.python.org/3/private/a.html")
            item = adapter.fetch("python", url="https://docs.python.org/3/tutorial/datastructures.html")[0]
        self.assertEqual(item.raw_text, "Lists are mutable sequences.")
        self.assertEqual(item.policy_key, "official_docs:python")
        LicenseChecker.validate(item)

    def test_main_text_extraction_drops_scripts(self):
        title, text = extract_main_text("<title>T | Site</title><script>var x=1;</script><main>Body text</main>")
        self.assertEqual((title, text), ("T", "Body text"))


class FakeExtractor:
    def __init__(self, claims):
        self.claims = claims
        self.calls = 0

    def extract_claims(self, text):
        self.calls += 1
        return list(self.claims)


class FakeVerifier:
    def __init__(self):
        self.calls = []

    def verify_claim(self, claim, defer_flashcard=False):
        self.calls.append((claim.id, defer_flashcard))
        return {"claim": claim, "canonical_claim": None, "flashcard": None}


@patch("knowledge.ingestion.pipeline.embed_evidence_task")
class PipelineIncrementalTests(TestCase):
    def pipeline(self, claims=("A binary search tree keeps keys in sorted order.",)):
        self.extractor = FakeExtractor(claims)
        self.verifier = FakeVerifier()
        return ExternalIngestionPipeline(extractor=self.extractor, verifier=self.verifier)

    def test_unchanged_content_is_not_reprocessed(self, _embed):
        pipeline = self.pipeline()
        first = pipeline.ingest_item(wiki_item())
        second = pipeline.ingest_item(wiki_item(raw_text=wiki_item().raw_text + "   "))  # whitespace-only change
        self.assertEqual(first["mode"], "canonical_knowledge")
        self.assertEqual(second["mode"], "already_ingested")
        self.assertEqual(self.extractor.calls, 1)
        self.assertEqual(SourceDocument.objects.count(), 1)
        self.assertEqual(SourceDocument.objects.get().metadata["ingestion_state"], "verified")

    def test_changed_content_creates_new_current_version(self, _embed):
        pipeline = self.pipeline()
        first = pipeline.ingest_item(wiki_item())
        second = pipeline.ingest_item(wiki_item(raw_text="A binary search tree keeps keys in sorted order. It now has new text."))
        self.assertEqual(second["document_version"], "updated")
        old = SourceDocument.objects.get(pk=first["document"].pk)
        self.assertFalse(old.is_current)
        self.assertEqual(old.superseded_by_id, second["document"].pk)
        self.assertTrue(second["document"].is_current)
        self.assertEqual(ExtractedClaim.objects.filter(source_document=old).count(), 1)  # old knowledge retained

    def test_interrupted_document_is_resumed(self, _embed):
        pipeline = self.pipeline()
        result = pipeline.ingest_item(wiki_item())
        document = result["document"]
        claim = document.extracted_claims.get()
        document.metadata = {**document.metadata, "ingestion_state": "claims_extracted"}
        document.save(update_fields=["metadata"])
        resumed = pipeline.ingest_item(wiki_item())
        self.assertEqual(resumed["document_version"], "resumed")
        self.assertEqual(self.extractor.calls, 1)  # not re-extracted
        self.assertEqual(self.verifier.calls[-1][0], claim.id)

    def test_insufficient_content_is_not_stored(self, _embed):
        with self.assertRaises(InsufficientContentError):
            self.pipeline().ingest_item(wiki_item(raw_text="   tiny  "))
        self.assertEqual(SourceDocument.objects.count(), 0)

    def test_policy_rejection_stores_nothing(self, _embed):
        with self.assertRaises(LicensePolicyError):
            self.pipeline().ingest_item(wiki_item(license_name="proprietary"))
        self.assertEqual(SourceDocument.objects.count(), 0)

    def test_self_attestation_only_for_grounded_claims(self, _embed):
        pipeline = self.pipeline(claims=[
            "A binary search tree keeps keys in sorted order.",
            "Quantum computers factor integers in polynomial time.",
        ])
        with self.captureOnCommitCallbacks(execute=True):
            result = pipeline.ingest_item(wiki_item())
        grounded, ungrounded = result["claims"]
        evidence = grounded.evidence_items.get()
        self.assertEqual(evidence.relation, Evidence.SUPPORTS)
        self.assertIn("sorted order", evidence.excerpt)
        self.assertFalse(ungrounded.evidence_items.exists())
        _embed.delay.assert_called_once_with(evidence.id)

    def test_no_self_attestation_for_arxiv(self, _embed):
        pipeline = self.pipeline(claims=["We study binary search trees."])
        item = wiki_item(policy_key="arxiv", source_domain="arxiv.org", license_name="cc0-1.0",
                         url="https://arxiv.org/abs/1", raw_text="We study binary search trees and their balancing rules.",
                         authority_score=Decimal("0.90"))
        result = pipeline.ingest_item(item)
        self.assertFalse(result["claims"][0].evidence_items.exists())

    def test_duplicate_claims_in_one_document_are_collapsed(self, _embed):
        pipeline = self.pipeline(claims=["A BST is ordered.", "a bst is ordered!"])
        result = pipeline.ingest_item(wiki_item())
        self.assertEqual(len(result["claims"]), 1)

    def test_deferred_flashcards_flag_reaches_verifier(self, _embed):
        pipeline = self.pipeline()
        pipeline.ingest_item(wiki_item(), defer_flashcards=True, topic_concept_id=7)
        self.assertTrue(self.verifier.calls[0][1])
        self.assertEqual(SourceDocument.objects.get().metadata["topic_concept_id"], 7)

    @override_settings(REDDIT_LEGAL_REVIEW_APPROVED=True)
    def test_reddit_evidence_only_is_never_embedded_or_extracted(self, _embed):
        pipeline = self.pipeline()
        claim = ExtractedClaim.objects.create(
            source_document=SourceDocument.objects.create(title="Doc", raw_text="x"), text="Recursion uses a stack.",
        )
        item = IngestionItem(
            title="Reddit: recursion", url="https://reddit.com/r/compsci/comments/abc", raw_text="Recursion uses the call stack to remember pending calls.",
            source_name="Reddit Community", source_domain="reddit.com", source_type=Source.SOURCE_TYPE_COMMUNITY,
            authority_score=Decimal("0.35"), license_name="reddit-data-api-terms", ai_use_allowed=False,
            evidence_only=True, metadata={"legal_review_approved": True}, policy_key="reddit",
        )
        with self.captureOnCommitCallbacks(execute=True):
            result = pipeline.ingest_item(item, target_claim_for_evidence=claim)
        self.assertEqual(result["mode"], "evidence_only")
        self.assertEqual(self.extractor.calls, 0)
        self.assertEqual(len(result["evidence"]), 1)
        _embed.delay.assert_not_called()

    def test_current_document_uniqueness_is_enforced(self, _embed):
        source = Source.objects.create(name="S")
        SourceDocument.objects.create(source=source, title="a", url="https://en.wikipedia.org/wiki/A")
        with self.assertRaises(IntegrityError):
            SourceDocument.objects.create(source=source, title="b", url="https://en.wikipedia.org/wiki/A")


class FakeAdapter:
    name = "wikimedia"

    def __init__(self, pages=None, items=None, fetch_error=None):
        self.pages = list(pages or [])
        self.items = items or []
        self.fetch_error = fetch_error
        self.discover_calls = []

    def discover(self, topic, cursor=None, limit=5):
        self.discover_calls.append((topic, cursor, limit))
        return self.pages.pop(0) if self.pages else DiscoveryPage(candidates=[], next_cursor=None)

    def fetch(self, identifier, **kwargs):
        if self.fetch_error:
            raise self.fetch_error
        return self.items


class FakePipeline:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = 0

    def ingest_item(self, item, **kwargs):
        self.calls += 1
        if self.error:
            raise self.error
        return self.result


@patch("knowledge.ingestion.jobs.topic_enabled", return_value=True)
class IngestionJobTests(TestCase):
    def setUp(self):
        self.concept = Concept.objects.create(name="Binary Search Tree", slug="binary-search-tree")
        Concept.objects.create(name="Computer Science & Engineering", slug="cse")

    def _discover(self, adapter, **kwargs):
        with patch("knowledge.ingestion.jobs.get_adapter", return_value=adapter), \
                patch("knowledge.ingestion.jobs.enqueue_jobs") as enqueue:
            with self.captureOnCommitCallbacks(execute=True):
                stats = DiscoveryService("wikimedia").run(**kwargs)
        return stats, enqueue

    def test_discovery_creates_jobs_from_taxonomy_and_saves_checkpoint(self, _enabled):
        adapter = FakeAdapter(pages=[DiscoveryPage(
            candidates=[DiscoveryCandidate(external_id="enwiki:1", identifier="Binary search tree")],
            next_cursor={"sroffset": 1},
        )])
        stats, enqueue = self._discover(adapter, limit=5)
        self.assertEqual(adapter.discover_calls[0][0], "Binary Search Tree")  # root concept excluded
        self.assertEqual(stats.jobs_created, 1)
        job = IngestionJob.objects.get()
        self.assertEqual(job.topic_concept, self.concept)
        enqueue.assert_called_once_with((job.id,))
        checkpoint = SourceDiscoveryCheckpoint.objects.get()
        self.assertEqual(checkpoint.cursor, {"sroffset": 1})
        self.assertIsNone(checkpoint.lease_until)

        # Second run resumes from the cursor and does not duplicate the job.
        adapter.pages = [DiscoveryPage(
            candidates=[DiscoveryCandidate(external_id="enwiki:1", identifier="Binary search tree")], next_cursor=None,
        )]
        stats, _ = self._discover(adapter, limit=5)
        self.assertEqual(adapter.discover_calls[-1][1], {"sroffset": 1})
        self.assertEqual(stats.jobs_created, 0)
        self.assertEqual(IngestionJob.objects.count(), 1)
        checkpoint.refresh_from_db()
        self.assertTrue(checkpoint.exhausted)
        self.assertIsNotNone(checkpoint.next_run_at)

    def test_leased_checkpoint_is_skipped(self, _enabled):
        SourceDiscoveryCheckpoint.objects.create(
            adapter="wikimedia", topic_key="manual:bst", topic="bst", lease_until=timezone.now() + timedelta(minutes=5),
        )
        adapter = FakeAdapter()
        stats, _ = self._discover(adapter, topic="bst")
        self.assertEqual(stats.skipped_topics, 1)
        self.assertEqual(adapter.discover_calls, [])

    def test_discovery_failure_backs_off(self, _enabled):
        adapter = FakeAdapter()
        adapter.discover = MagicMock(side_effect=RateLimitedError("slow down", retry_after=120))
        stats, _ = self._discover(adapter, topic="bst")
        self.assertEqual(len(stats.errors), 1)
        checkpoint = SourceDiscoveryCheckpoint.objects.get()
        self.assertEqual(checkpoint.consecutive_failures, 1)
        self.assertGreater(checkpoint.next_run_at, timezone.now() + timedelta(seconds=100))

    def _job(self, **kwargs):
        values = dict(adapter="wikimedia", external_id="enwiki:1", identifier="Binary search tree", topic_concept=self.concept)
        values.update(kwargs)
        return IngestionJob.objects.create(**values)

    def _process(self, job, adapter, pipeline):
        with patch("knowledge.ingestion.jobs.get_adapter", return_value=adapter):
            return IngestionJobService(pipeline=pipeline).process(job.id)

    def test_successful_job_records_counts(self, _enabled):
        document = SourceDocument.objects.create(title="d", raw_text="x")
        claim = ExtractedClaim.objects.create(source_document=document, text="c")
        pipeline = FakePipeline(result={
            "document": document, "mode": "canonical_knowledge", "document_version": "new", "claims": [claim],
            "verification_results": [{"canonical_claim": object(), "canonical_created": True, "flashcard_deferred": True}],
        })
        job = self._process(self._job(), FakeAdapter(items=[wiki_item()]), pipeline)
        self.assertEqual(job.status, IngestionJob.STATUS_SUCCEEDED)
        self.assertEqual(job.result["canonical_created"], 1)
        self.assertEqual(job.result["flashcards_deferred"], 1)
        self.assertEqual(job.source_document, document)
        # A duplicate message for the same job is a no-op.
        self.assertIsNone(self._process(job, FakeAdapter(items=[wiki_item()]), pipeline))
        self.assertEqual(pipeline.calls, 1)

    def test_policy_rejection_and_permanent_failures_are_recorded(self, _enabled):
        job = self._process(self._job(), FakeAdapter(items=[wiki_item()]), FakePipeline(error=LicensePolicyError("nope")))
        self.assertEqual(job.status, IngestionJob.STATUS_POLICY_REJECTED)
        self.assertIn("nope", job.last_error)
        job = self._process(self._job(external_id="enwiki:2"), FakeAdapter(fetch_error=PermanentProviderError("404")), FakePipeline())
        self.assertEqual(job.status, IngestionJob.STATUS_FAILED)
        job = self._process(self._job(external_id="enwiki:3"), FakeAdapter(items=[wiki_item()]),
                            FakePipeline(error=InsufficientContentError("short")))
        self.assertEqual(job.status, IngestionJob.STATUS_SKIPPED)

    def test_transient_failure_retries_then_fails_at_max_attempts(self, _enabled):
        job = self._job(max_attempts=2)
        adapter = FakeAdapter(fetch_error=TransientProviderError("timeout"))
        with self.assertRaises(JobRetry):
            self._process(job, adapter, FakePipeline())
        job.refresh_from_db()
        self.assertEqual(job.status, IngestionJob.STATUS_RETRY)
        self.assertEqual(job.attempts, 1)
        self.assertIsNotNone(job.next_attempt_at)
        job = self._process(job, adapter, FakePipeline())
        self.assertEqual(job.status, IngestionJob.STATUS_FAILED)
        self.assertEqual(job.attempts, 2)

    def test_disabled_policy_rejects_job(self, enabled):
        enabled.return_value = False
        job = self._process(self._job(), FakeAdapter(items=[wiki_item()]), FakePipeline())
        self.assertEqual(job.status, IngestionJob.STATUS_POLICY_REJECTED)

    def test_recovery_requeues_expired_and_lost_jobs(self, _enabled):
        now = timezone.now()
        crashed = self._job(status=IngestionJob.STATUS_PROCESSING, locked_until=now - timedelta(minutes=1), attempts=1)
        lost = self._job(external_id="enwiki:2")
        IngestionJob.objects.filter(pk=lost.pk).update(discovered_at=now - timedelta(hours=2))
        fresh = self._job(external_id="enwiki:3")
        exhausted = self._job(external_id="enwiki:4", status=IngestionJob.STATUS_RETRY, next_attempt_at=now, attempts=4, max_attempts=4)
        with patch("knowledge.ingestion.jobs.enqueue_jobs") as enqueue:
            result = recover_stale_jobs()
        requeued = set(enqueue.call_args.args[0])
        self.assertEqual(requeued, {crashed.id, lost.id})
        self.assertNotIn(fresh.id, requeued)
        self.assertEqual(result["expired_leases"], 1)
        exhausted.refresh_from_db()
        self.assertEqual(exhausted.status, IngestionJob.STATUS_FAILED)


class SchedulingConfigurationTests(TestCase):
    def test_ingestion_tasks_registered_and_routed(self):
        from config.celery import app
        from django.conf import settings

        app.loader.import_default_modules()
        for name in (
            "knowledge.schedule_external_discovery",
            "knowledge.discover_adapter",
            "knowledge.process_ingestion_job",
            "knowledge.recover_ingestion_jobs",
            "learning.generate_flashcard_for_claim",
            "learning.backfill_missing_flashcards",
        ):
            self.assertIn(name, app.tasks)
            self.assertEqual(settings.CELERY_TASK_ROUTES[name]["queue"], settings.INGESTION_TASK_QUEUE)

    @patch("knowledge.tasks.discover_adapter_task.delay")
    def test_schedule_fans_out_to_enabled_adapters(self, delay):
        from knowledge.tasks import schedule_external_discovery_task

        with override_settings(INGESTION_ENABLED_ADAPTERS=["wikimedia", "reddit", "official_docs"]):
            result = schedule_external_discovery_task()
        self.assertEqual(result["adapters"], ["wikimedia", "official_docs"])  # reddit blocked by policy
        self.assertEqual(delay.call_count, 2)

    # Tasks call close_old_connections(), which closes the non-autocommit TestCase connection.
    @patch("knowledge.tasks.close_old_connections")
    @patch("knowledge.ingestion.jobs.IngestionJobService.process", side_effect=JobRetry(30))
    def test_process_task_retries_with_countdown(self, _process, _close):
        from celery.exceptions import Retry
        from knowledge.tasks import process_ingestion_job_task

        with patch.object(process_ingestion_job_task, "retry", side_effect=Retry()) as retry:
            with self.assertRaises(Retry):
                process_ingestion_job_task.run(1)
        retry.assert_called_once_with(countdown=30)
