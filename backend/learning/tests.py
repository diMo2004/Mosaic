from urllib import response

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from knowledge.models import CanonicalClaim, Concept, Evidence, Source, ExtractedClaim, SourceDocument
from learning.models import Flashcard, Playlist, PlaylistItem, UserProgress
from learning.services import FlashcardGenerationService

# Create your tests here.

class FlashcardAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="learner", password="pass12345")
        self.other = User.objects.create_user(username="other", password="pass12345")
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