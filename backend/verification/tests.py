from django.test import TestCase

# Create your tests here.
#Placeholder evidence is created if no evidence exists
#Supported evidence makes claim supported
#Contradicting evidence makes claim contradicted
#Related-only evidence makes claim uncertain
#CanonicalClaim is created only for supported claims
#Flashcard is created only from CanonicalClaim

from django.contrib.auth.models import User
from django.test import TestCase
from knowledge.models import (
    CanonicalClaim,
    Evidence,
    Source,
    ExtractedClaim,
    SourceDocument,
)
from learning.models import Flashcard
from verification.services.claim_verification import ClaimVerificationService

class ClaimVerificationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin")
        self.source = Source.objects.create(
            name="Test Source",
            source_type=Source.SOURCE_TYPE_EDUCATIONAL,
            authority_score=0.90,
        )
        self.document = SourceDocument.objects.create(
            source=self.source,
            title="Test Document",
            document_type=SourceDocument.DOCUMENT_TYPE_WEBPAGE,
            raw_text="BFS uses a queue.",
        )
        self.claim = ExtractedClaim.objects.create(
            source_document=self.document,
            text="BFS uses a queue.",
        )

    def test_supported_claim_creates_canonical_claim_and_flashcard(self):
        # Create supporting evidence
        Evidence.objects.create(
            claim=self.claim,
            source=self.source,
            relation=Evidence.SUPPORTS,
            excerpt="BFS uses a queue.",
            relevance_score=0.90,
        )
        result = ClaimVerificationService().verify_claim(self.claim)

        self.claim.refresh_from_db()
        self.assertEqual(self.claim.status, ExtractedClaim.STATUS_SUPPORTED)
        self.assertIsNotNone(result["canonical_claim"])

        canonical_claim = result["canonical_claim"]
        self.assertIsNotNone(canonical_claim)
        self.assertEqual(CanonicalClaim.objects.count(), 1)
        self.assertEqual(Flashcard.objects.count(), 1)

    def test_contradicted_claim_does_not_create_canonical_claim(self):
        Evidence.objects.create(
            claim=self.claim,
            source=self.source,
            relation=Evidence.CONTRADICTS,
            excerpt="BFS does not use a queue.",
            relevance_score=0.90,
        )
        result = ClaimVerificationService().verify_claim(self.claim)

        self.claim.refresh_from_db()
        self.assertEqual(self.claim.status, ExtractedClaim.STATUS_CONTRADICTED)
        self.assertIsNone(result["canonical_claim"])
        self.assertEqual(CanonicalClaim.objects.count(), 0)
        self.assertEqual(Flashcard.objects.count(), 0)