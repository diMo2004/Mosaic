from urllib import response

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from .services.rag_explanation import RAGExplanationService, RAGExplanationServiceError
from knowledge.models import CanonicalClaim, Concept, Evidence, Source, ExtractedClaim, SourceDocument
from learning.models import Flashcard, Playlist, PlaylistItem, UserProgress
from learning.services.flashcard_service import FlashcardGenerationService

# Create your tests here.

class FlashcardAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="learner", password="pass12345")
        self.user.profile.profile_completed = True
        self.user.profile.save()
        self.other = User.objects.create_user(username="other", password="pass12345")
        self.other.profile.profile_completed = True
        self.other.profile.save()
        self.concept = Concept.objects.create(name="BFS", slug="bfs")
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
        self.extracted = ExtractedClaim.objects.create(
            source_document=self.document,
            text="BFS uses a queue.",
        )
        self.canonical = CanonicalClaim.objects.create(
            concept=self.concept,
            text="BFS uses a queue.",
            source_claim=self.extracted,
            is_active=True,
        )
        self.flashcard = FlashcardGenerationService().generate_from_canonical_claim(self.canonical)
        self.client.force_authenticate(user=self.user)

    def test_generator_sets_canonical_claim(self):
        self.assertEqual(self.flashcard.source_claim_id, self.canonical.id)
        self.assertEqual(self.flashcard.explanation, "This flashcard was generated from a canonical claim.")

    def test_feed_lists_active_canonical_flashcards(self):
        response = self.client.get("/api/learning/flashcards/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["canonical_claim_id"], self.canonical.id)
        self.assertEqual(response.data[0]["concept_name"], "BFS")

    def test_detail_increments_progress(self):
        response = self.client.get(f"/api/learning/flashcards/{self.flashcard.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        progress = UserProgress.objects.get(user=self.user, flashcard=self.flashcard)
        self.assertEqual(progress.view_count, 1)

    def test_save_uses_default_playlist(self):
        response = self.client.post(f"/api/learning/flashcards/{self.flashcard.id}/save/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        playlist = Playlist.objects.get(user=self.user, is_default=True)
        self.assertEqual(response.data["playlist_id"], playlist.id)
        self.assertTrue(
            PlaylistItem.objects.filter(
                playlist=playlist, flashcard=self.flashcard
            ).exists()
        )
        detail = self.client.get(f"/api/learning/flashcards/{self.flashcard.id}/")
        self.assertTrue(detail.data["is_saved"])

    def test_unsave_removes_from_playlist(self):
        self.client.post(f"/api/learning/flashcards/{self.flashcard.id}/save/")
        response = self.client.delete(f"/api/learning/flashcards/{self.flashcard.id}/save/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            PlaylistItem.objects.filter(
                playlist__user=self.user,
                flashcard=self.flashcard,
            ).exists()
        )

    def test_cannot_save_to_another_users_playlist(self):
        other_playlist = Playlist.objects.create(
            user=self.other,
            name="Other",
            is_default=False,
        )
        response = self.client.post(
            f"/api/learning/flashcards/{self.flashcard.id}/save/",
            {"playlist_id": other_playlist.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_feedback_and_progress(self):
        self.client.get(f"/api/learning/flashcards/{self.flashcard.id}/")
        self.client.post(f"/api/learning/flashcards/{self.flashcard.id}/save/")
        feedback = self.client.post(
            f"/api/learning/flashcards/{self.flashcard.id}/feedback/",
            {"feedback_type": "like", "comment": "clear"},
            format="json",
        )
        self.assertEqual(feedback.status_code, status.HTTP_201_CREATED)
        progress = self.client.get("/api/learning/progress/")
        self.assertEqual(progress.status_code, status.HTTP_200_OK)
        self.assertEqual(progress.data["total_flashcards_viewed"], 1)
        self.assertEqual(progress.data["saved_count"], 1)
        self.assertEqual(progress.data["feedback_count"], 1)

    def test_playlist_list_creates_default(self):
        response = self.client.get("/api/learning/playlists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Saved")
        self.assertTrue(response.data[0]["is_default"])

from knowledge.services.evidence_retrieval import (
    EvidenceRetrievalError,
    EvidenceRetrievalService,
)

from decimal import Decimal
from unittest.mock import Mock, patch

class FakeExplanationResponse:
    def __init__(self, text):
        self.text = text


class FakeExplanationModels:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error

    def generate_content(self, **kwargs):
        if self.error:
            raise self.error
        return self.response


class FakeExplanationClient:
    def __init__(self, response=None, error=None):
        self.models = FakeExplanationModels(
            response=response,
            error=error,
        )


class FakeEvidenceRetriever:
    def __init__(self, evidence_items):
        self.evidence_items = evidence_items

    def retrieve(self, query, *, top_k):
        return self.evidence_items[:top_k]

class EvidenceRetrievalServiceTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Algorithms Source",
            source_type=Source.SOURCE_TYPE_EDUCATIONAL,
            authority_score=Decimal("0.90"),
        )
        self.concept = Concept.objects.create(
            name="Breadth-First Search",
            slug="breadth-first-search",
        )
        self.document = SourceDocument.objects.create(
            source=self.source,
            title="BFS Documentation",
            document_type=SourceDocument.DOCUMENT_TYPE_DOC,
            raw_text="BFS uses a queue.",
        )
        self.claim = ExtractedClaim.objects.create(
            source_document=self.document,
            text="BFS uses a queue.",
        )

    def _vector(self, first_value):
        return [first_value] + [0.0] * 767

    def test_retrieve_rejects_empty_query(self):
        service = EvidenceRetrievalService(
            embedder=Mock(),
        )

        with self.assertRaises(EvidenceRetrievalError):
            service.retrieve("")

    def test_retrieve_rejects_invalid_top_k(self):
        service = EvidenceRetrievalService(
            embedder=Mock(),
        )

        with self.assertRaises(EvidenceRetrievalError):
            service.retrieve("BFS uses a queue.", top_k=0)

    def test_retrieve_returns_only_embedded_evidence(self):
        matching = Evidence.objects.create(
            claim=self.claim,
            source=self.source,
            relation=Evidence.SUPPORTS,
            title="Embedded BFS Evidence",
            excerpt="BFS uses a queue.",
            relevance_score=Decimal("0.90"),
            embedding=self._vector(1.0),
        )
        Evidence.objects.create(
            claim=self.claim,
            source=self.source,
            relation=Evidence.RELATED,
            title="Unembedded Evidence",
            excerpt="This record has no vector.",
            relevance_score=Decimal("0.80"),
        )

        embedder = Mock()
        embedder.embed_text.return_value = self._vector(1.0)

        service = EvidenceRetrievalService(embedder=embedder)
        results = service.retrieve(
            "BFS uses a queue.",
            top_k=4,
        )

        self.assertEqual([item.id for item in results], [matching.id])
        self.assertTrue(hasattr(results[0], "distance"))

    def test_retrieve_respects_top_k(self):
        for index in range(3):
            Evidence.objects.create(
                claim=self.claim,
                source=self.source,
                relation=Evidence.RELATED,
                title=f"Evidence {index}",
                excerpt=f"BFS evidence {index}.",
                relevance_score=Decimal("0.80"),
                embedding=self._vector(1.0),
            )

        embedder = Mock()
        embedder.embed_text.return_value = self._vector(1.0)

        service = EvidenceRetrievalService(embedder=embedder)
        results = service.retrieve(
            "BFS uses a queue.",
            top_k=2,
        )

        self.assertEqual(len(results), 2)

class RAGExplanationServiceTests(APITestCase):
    def setUp(self):
        self.source = Source.objects.create(
            name="Algorithms Source",
            source_type=Source.SOURCE_TYPE_EDUCATIONAL,
            authority_score=Decimal("0.90"),
        )
        self.concept = Concept.objects.create(
            name="Breadth-First Search",
            slug="breadth-first-search",
        )
        self.document = SourceDocument.objects.create(
            source=self.source,
            title="BFS Documentation",
            document_type=SourceDocument.DOCUMENT_TYPE_DOC,
            raw_text="BFS uses a queue.",
        )
        self.extracted_claim = ExtractedClaim.objects.create(
            source_document=self.document,
            text="BFS uses a queue.",
        )
        self.canonical_claim = CanonicalClaim.objects.create(
            concept=self.concept,
            source_claim=self.extracted_claim,
            text="BFS uses a queue.",
            confidence=Decimal("0.90"),
            is_active=True,
        )
        self.evidence = Evidence.objects.create(
            claim=self.extracted_claim,
            source=self.source,
            relation=Evidence.SUPPORTS,
            title="BFS Evidence",
            url="https://example.com/bfs",
            excerpt="BFS processes vertices using a queue.",
            relevance_score=Decimal("0.90"),
        )

    def test_valid_citation_is_accepted(self):
        response = FakeExplanationResponse(
            "BFS processes vertices using a queue [1]."
        )
        client = FakeExplanationClient(response=response)
        retriever = FakeEvidenceRetriever([self.evidence])

        service = RAGExplanationService(
            evidence_retriever=retriever,
            client=client,
        )

        result = service.generate_explanation(
            self.canonical_claim,
        )

        self.assertEqual(
            result["explanation"],
            "BFS processes vertices using a queue [1].",
        )
        self.assertEqual(
            [item.id for item in result["evidence"]],
            [self.evidence.id],
        )

    def test_invalid_citation_is_rejected(self):
        response = FakeExplanationResponse(
            "BFS processes vertices using a queue [2]."
        )
        client = FakeExplanationClient(response=response)
        retriever = FakeEvidenceRetriever([self.evidence])

        service = RAGExplanationService(
            evidence_retriever=retriever,
            client=client,
        )

        with self.assertRaises(RAGExplanationServiceError):
            service.generate_explanation(self.canonical_claim)

    def test_missing_citation_is_rejected(self):
        response = FakeExplanationResponse(
            "BFS processes vertices using a queue."
        )
        client = FakeExplanationClient(response=response)
        retriever = FakeEvidenceRetriever([self.evidence])

        service = RAGExplanationService(
            evidence_retriever=retriever,
            client=client,
        )

        with self.assertRaises(RAGExplanationServiceError):
            service.generate_explanation(self.canonical_claim)

    def test_provider_failure_is_wrapped(self):
        client = FakeExplanationClient(
            error=RuntimeError("provider unavailable"),
        )
        retriever = FakeEvidenceRetriever([self.evidence])

        service = RAGExplanationService(
            evidence_retriever=retriever,
            client=client,
        )

        with self.assertRaises(RAGExplanationServiceError) as context:
            service.generate_explanation(self.canonical_claim)

        self.assertEqual(
            str(context.exception),
            "The explanation provider request failed.",
        )

    def test_prompt_uses_canonical_claim_text(self):
        response = FakeExplanationResponse(
            "BFS processes vertices using a queue [1]."
        )
        generate_content = Mock(return_value=response)

        client = Mock()
        client.models.generate_content = generate_content

        retriever = FakeEvidenceRetriever([self.evidence])

        service = RAGExplanationService(
            evidence_retriever=retriever,
            client=client,
        )

        service.generate_explanation(self.canonical_claim)

        prompt = generate_content.call_args.kwargs["contents"]

        self.assertIn(
            self.canonical_claim.text,
            prompt,
        )
        self.assertIn(
            self.evidence.excerpt,
            prompt,
        )
        self.assertNotIn(
            "claim_text",
            prompt,
        )

class GroundedExplanationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="explanation-user",
            password="test-password-123",
        )
        self.user.profile.profile_completed = True
        self.user.profile.save(update_fields=["profile_completed"])

        self.source = Source.objects.create(
            name="Algorithms Source",
            source_type=Source.SOURCE_TYPE_EDUCATIONAL,
            authority_score=Decimal("0.90"),
        )
        self.concept = Concept.objects.create(
            name="Depth-First Search",
            slug="depth-first-search",
        )
        self.document = SourceDocument.objects.create(
            source=self.source,
            title="DFS Documentation",
            document_type=SourceDocument.DOCUMENT_TYPE_DOC,
            raw_text="DFS uses a stack.",
        )
        self.extracted_claim = ExtractedClaim.objects.create(
            source_document=self.document,
            text="DFS uses a stack.",
        )
        self.canonical_claim = CanonicalClaim.objects.create(
            concept=self.concept,
            source_claim=self.extracted_claim,
            text="DFS uses a stack.",
            confidence=Decimal("0.90"),
            is_active=True,
        )
        self.evidence = Evidence.objects.create(
            claim=self.extracted_claim,
            source=self.source,
            relation=Evidence.SUPPORTS,
            title="DFS Evidence",
            url="https://example.com/dfs",
            excerpt="DFS can use a stack to traverse a graph.",
            relevance_score=Decimal("0.90"),
        )

        self.client.force_authenticate(user=self.user)

    @patch("learning.services.rag_explanation.RAGExplanationService")
    def test_explanation_returns_evidence_used_by_rag(
        self,
        rag_service_class,
    ):
        rag_service_class.return_value.generate_explanation.return_value = {
            "explanation": (
                "DFS can use a stack to traverse a graph [1]."
            ),
            "evidence": [self.evidence],
        }

        response = self.client.get(
            f"/api/learning/canonical-claims/"
            f"{self.canonical_claim.id}/explain/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["evidence"][0]["id"],
            self.evidence.id,
        )
        self.assertEqual(
            response.data["evidence"][0]["citation"],
            1,
        )

    @patch("learning.services.rag_explanation.RAGExplanationService")
    def test_explanation_failure_returns_503(
        self,
        rag_service_class,
    ):
        rag_service_class.return_value.generate_explanation.side_effect = (
            RAGExplanationServiceError("provider unavailable")
        )

        response = self.client.get(
            f"/api/learning/canonical-claims/"
            f"{self.canonical_claim.id}/explain/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )
        self.assertEqual(
            response.data["detail"],
            "A grounded explanation is temporarily unavailable.",
        )

    def test_inactive_claim_returns_404(self):
        self.canonical_claim.is_active = False
        self.canonical_claim.save(update_fields=["is_active"])

        response = self.client.get(
            f"/api/learning/canonical-claims/"
            f"{self.canonical_claim.id}/explain/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_request_returns_401(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            f"/api/learning/canonical-claims/"
            f"{self.canonical_claim.id}/explain/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )