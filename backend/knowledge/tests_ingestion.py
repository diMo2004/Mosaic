from decimal import Decimal
from unittest.mock import MagicMock, patch
from django.test import TestCase
from knowledge.ingestion.adapters.arxiv import ArxivAdapter
from knowledge.ingestion.adapters.wikimedia import WikimediaAdapter
from knowledge.ingestion.base import IngestionItem
from knowledge.ingestion.license_checker import LicenseChecker, LicensePolicyError
from knowledge.ingestion.pipeline import ExternalIngestionPipeline
from knowledge.models import Source, SourceDocument


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