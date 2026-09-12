from django.test import TestCase
from unittest.mock import patch, MagicMock

# Create your tests here.
#Placeholder evidence is created if no evidence exists
#Supported evidence makes claim supported
#Contradicting evidence makes claim contradicted
#Related-only evidence makes claim uncertain
#CanonicalClaim is created only for supported claims
#Flashcard is created only from CanonicalClaim

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase
from knowledge.models import (
    CanonicalClaim,
    Concept,
    Evidence,
    Source,
    ExtractedClaim,
    SourceDocument,
)
from learning.models import Flashcard
from notes.models import Note
from verification.models import NoteProcessingJob
from verification.services.note_processing import NoteProcessingService
from verification.services.claim_verification import ClaimVerificationService

class NoteProcessJobIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.note = Note.objects.create(
            owner=self.user,
            title="Data Structures Lecture Notes",
            file=SimpleUploadedFile("lecture.txt", b"Binary search operates on sorted arrays."),
        )

    @patch("verification.services.note_processing.HybridOCRProvider")
    @patch("verification.services.note_processing.ClaimExtractionService")
    @patch("verification.services.concept_assignment.ConceptAssignmentService")
    def test_processing_pipeline_completes_and_verifies(self, MockConceptService, MockClaimExtractor, MockOCRProvider):
        mock_ocr = MagicMock()
        mock_ocr.extract_text.return_value = "Binary search operates on sorted arrays in O(log n)."
        MockOCRProvider.return_value = mock_ocr

        mock_extractor = MagicMock()
        mock_extractor.extract_claims.return_value = [
            "Binary search operates on sorted arrays.",
        ]
        MockClaimExtractor.return_value = mock_extractor

        mock_concept_inst = MagicMock()
        mock_concept_inst.assign_concept.return_value = Concept.objects.create(
            name="Algorithms", slug="algorithms"
            )
        MockConceptService.return_value = mock_concept_inst

        job = NoteProcessingService().process(self.note.id)
        self.note.refresh_from_db()
        job.refresh_from_db()

        self.assertEqual(job.status, NoteProcessingJob.STATUS_VERIFIED)
        self.assertIsNotNone(job.completed_at)
        self.assertEqual(self.note.status, Note.STATUS_VERIFIED)
        self.assertEqual(self.note.extracted_text, "Binary search operates on sorted arrays in O(log n).")

        self.assertEqual(self.note.source_documents.count(), 1)
        doc = self.note.source_documents.first()
        self.assertEqual(doc.extracted_claims.count(), 1)
        claim = doc.extracted_claims.first()
        self.assertIn(claim.status, [ExtractedClaim.STATUS_SUPPORTED, ExtractedClaim.STATUS_UNCERTAIN])

    @patch("verification.services.note_processing.HybridOCRProvider")
    def test_processing_failure_records_error_and_status(self, MockOCRProvider):
        mock_ocr = MagicMock()
        mock_ocr.extract_text.side_effect = Exception("OCR connection timeout")
        MockOCRProvider.return_value = mock_ocr

        job = NoteProcessingService().process(self.note.id)
        self.note.refresh_from_db()
        job.refresh_from_db()

        self.assertEqual(job.status, NoteProcessingJob.STATUS_FAILED)
        self.assertIn("OCR connection timeout", job.error_message)
        self.assertIsNotNone(job.completed_at)
        self.assertEqual(self.note.status, Note.STATUS_FAILED)
        self.assertIn("OCR connection timeout", self.note.processing_error)


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
    @patch("verification.services.concept_assignment.ConceptAssignmentService")
    def test_supported_claim_creates_canonical_claim_and_flashcard(self, MockConceptService):
        # Create supporting evidence
        concept = Concept.objects.create(name="BFS", slug="bfs")
        mock_instance = MagicMock()
        mock_instance.assign_concept.return_value = concept
        MockConceptService.return_value = mock_instance
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
        self.assertEqual(
            Flashcard.objects.get().source_claim_id,
            result["canonical_claim"].id,
        )

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