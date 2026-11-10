from datetime import timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import IntegrityError
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APITestCase

from knowledge.ingestion.normalize import claim_hash
from knowledge.models import CanonicalClaim, Concept, ConceptRelationship, Evidence, ExtractedClaim, Source, SourceDocument
from learning.models import Flashcard, FlashcardFeedEvent, UserProgress
from learning.services.flashcard_service import FlashcardGenerationService
from learning.tasks import backfill_missing_flashcards_task, generate_flashcard_for_claim_task
from verification.services.claim_verification import ClaimVerificationService
from verification.services.concept_assignment import ConceptAssignmentService, invalidate_cached_graph

FEED_URL = "/api/learning/flashcards/"


def make_claim(concept, text, *, document=None, active=True):
    document = document or SourceDocument.objects.create(title="Doc", raw_text=text)
    extracted = ExtractedClaim.objects.create(source_document=document, text=text, status=ExtractedClaim.STATUS_SUPPORTED)
    return CanonicalClaim.objects.create(concept=concept, text=text, text_hash=claim_hash(text), source_claim=extracted, is_active=active)


def make_card(concept, text, **claim_kwargs):
    claim = make_claim(concept, text, **claim_kwargs)
    return Flashcard.objects.create(title=text[:20], prompt=f"Q: {text}?", answer=text, source_claim=claim)


class FeedPaginationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reader", password="pass12345")
        self.user.profile.profile_completed = True
        self.user.profile.save()
        self.client.force_authenticate(user=self.user)
        self.graphs = Concept.objects.create(name="Graphs", slug="graphs")
        self.trees = Concept.objects.create(name="Trees", slug="trees")

    def get(self, session, limit=2):
        return self.client.get(FEED_URL, {"session_id": session, "limit": limit})

    def test_pages_never_repeat_within_a_session(self):
        cards = [make_card(self.graphs if i % 2 else self.trees, f"Fact number {i}") for i in range(5)]
        session = str(uuid4())
        seen = []
        for _ in range(3):
            response = self.get(session)
            self.assertEqual(response.status_code, 200)
            seen.extend(card["id"] for card in response.data["results"])
        self.assertEqual(sorted(seen), sorted(card.id for card in cards))
        self.assertEqual(len(seen), len(set(seen)))
        self.assertTrue(response.data["session_exhausted"])
        self.assertFalse(response.data["has_more"])
        self.assertEqual(response.data["cursor"], session)
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_new_cards_appear_in_same_session_after_exhaustion(self):
        make_card(self.graphs, "BFS uses a queue")
        session = str(uuid4())
        self.get(session)
        exhausted = self.get(session)
        self.assertEqual(exhausted.data["results"], [])
        self.assertTrue(exhausted.data["session_exhausted"])
        self.assertEqual(exhausted.data["retry_after_seconds"], 120)

        new_card = make_card(self.trees, "AVL trees stay balanced")
        replenished = self.get(session)
        self.assertEqual([card["id"] for card in replenished.data["results"]], [new_card.id])

    def test_ineligible_cards_are_excluded(self):
        eligible = make_card(self.graphs, "Dijkstra needs non-negative weights")
        inactive_claim_card = make_card(self.graphs, "Inactive claim fact", active=False)
        inactive_card = make_card(self.trees, "Inactive card fact")
        inactive_card.is_active = False
        inactive_card.save(update_fields=["is_active"])
        orphan = Flashcard.objects.create(title="Orphan", prompt="?", answer="!", source_claim=None)
        ids = [card["id"] for card in self.get(str(uuid4()), limit=10).data["results"]]
        self.assertEqual(ids, [eligible.id])
        self.assertNotIn(inactive_claim_card.id, ids)
        self.assertNotIn(orphan.id, ids)

    def test_cross_session_ranking_prefers_unseen_then_least_recent(self):
        recent = make_card(self.graphs, "Recently viewed fact")
        older = make_card(self.graphs, "Viewed long ago fact")
        unseen = make_card(self.trees, "Never seen fact")
        now = timezone.now()
        UserProgress.objects.create(user=self.user, flashcard=recent, view_count=1, last_viewed_at=now - timedelta(hours=1))
        UserProgress.objects.create(user=self.user, flashcard=older, view_count=1, last_viewed_at=now - timedelta(days=30))
        response = self.get(str(uuid4()), limit=3)
        ids = [card["id"] for card in response.data["results"]]
        self.assertEqual(ids, [unseen.id, older.id, recent.id])
        self.assertEqual(response.data["repeated_count"], 1)

    def test_recently_served_cards_are_penalised_across_sessions(self):
        served = make_card(self.graphs, "Served in another session fact")
        fresh = make_card(self.graphs, "Fresh fact")
        FlashcardFeedEvent.objects.create(user=self.user, flashcard=served, session_id=uuid4(), event_type=FlashcardFeedEvent.EVENT_SERVED)
        ids = [card["id"] for card in self.get(str(uuid4()), limit=2).data["results"]]
        self.assertEqual(ids, [fresh.id, served.id])

    def test_page_interleaves_concepts(self):
        for i in range(3):
            make_card(self.graphs, f"Graph fact {i}")
        for i in range(3):
            make_card(self.trees, f"Tree fact {i}")
        results = self.get(str(uuid4()), limit=4).data["results"]
        concepts = [card["concept_name"] for card in results]
        self.assertTrue(all(a != b for a, b in zip(concepts, concepts[1:])), concepts)

    def test_invalid_session_and_limit_are_tolerated(self):
        make_card(self.graphs, "Some fact here")
        response = self.client.get(FEED_URL, {"session_id": "not-a-uuid", "limit": "abc"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_attribution_and_placeholder_evidence(self):
        source = Source.objects.create(name="Wikipedia", license="cc-by-sa-4.0")
        placeholder = Source.objects.create(name="Placeholder Educational Source", access_method="placeholder")
        document = SourceDocument.objects.create(
            source=source, title="Wikipedia: BFS", url="https://en.wikipedia.org/wiki/BFS", raw_text="BFS uses a queue.",
            metadata={"policy": {"license": "cc-by-sa-4.0", "attribution_text": "Wikipedia contributors"}},
        )
        card = make_card(self.graphs, "BFS uses a queue.", document=document)
        extracted = card.source_claim.source_claim
        Evidence.objects.create(claim=extracted, source=source, relation=Evidence.SUPPORTS, url=document.url)
        Evidence.objects.create(claim=extracted, source=placeholder, relation=Evidence.RELATED, url="https://example.com")
        result = self.get(str(uuid4()), limit=1).data["results"][0]
        self.assertEqual(result["attribution"]["license"], "cc-by-sa-4.0")
        self.assertEqual(result["attribution"]["attribution"], "Wikipedia contributors")
        self.assertEqual([item["source"] for item in result["evidence"]], ["Wikipedia"])

    def test_viewed_events_still_recorded_per_session(self):
        card = make_card(self.graphs, "Viewed fact")
        session = str(uuid4())
        self.client.post(f"/api/learning/flashcards/{card.id}/viewed/", {"session_id": session}, format="json")
        self.assertTrue(FlashcardFeedEvent.objects.filter(flashcard=card, event_type="viewed").exists())
        # A card viewed in this session is not served again in it.
        self.assertEqual(self.get(session).data["results"], [])


@override_settings(GEMINI_API_KEY="")
class FlashcardGenerationIdempotencyTests(TestCase):
    def setUp(self):
        self.concept = Concept.objects.create(name="Queues", slug="queues")
        self.claim = make_claim(self.concept, "A queue is first-in first-out.")

    def test_existing_card_short_circuits_llm(self):
        first = FlashcardGenerationService().generate_from_canonical_claim(self.claim)
        with patch.object(FlashcardGenerationService, "_generate_copy") as generate:
            second = FlashcardGenerationService().generate_from_canonical_claim(self.claim)
        generate.assert_not_called()
        self.assertEqual(first.id, second.id)
        self.assertEqual(Flashcard.objects.count(), 1)

    def test_fallback_without_key_is_labelled(self):
        card = FlashcardGenerationService().generate_from_canonical_claim(self.claim)
        self.assertEqual(card.generation_method, Flashcard.GENERATION_FALLBACK)
        self.assertFalse(card.created_by_ai)

    @override_settings(GEMINI_API_KEY="configured-key")
    @patch("learning.services.flashcard_service.genai.Client")
    def test_llm_failure_with_key_is_not_marked_ai(self, client_class):
        client_class.return_value.models.generate_content.side_effect = RuntimeError("quota")
        card = FlashcardGenerationService().generate_from_canonical_claim(self.claim)
        self.assertEqual(card.generation_method, Flashcard.GENERATION_FALLBACK)
        self.assertFalse(card.created_by_ai)

    @override_settings(GEMINI_API_KEY="configured-key")
    @patch("learning.services.flashcard_service.genai.Client")
    def test_gemini_success_is_labelled(self, client_class):
        client_class.return_value.models.generate_content.return_value = MagicMock(text=(
            '{"title": "FIFO", "prompt": "Which element leaves a queue first?", "answer": "The oldest one.",'
            ' "explanation": "Queues are FIFO.", "difficulty": "beginner", "card_type": "recall",'
            ' "quiz_options": [], "key_points": [], "visual_hint": ""}'
        ))
        card = FlashcardGenerationService().generate_from_canonical_claim(self.claim)
        self.assertEqual(card.generation_method, Flashcard.GENERATION_GEMINI)
        self.assertTrue(card.created_by_ai)

    def test_database_rejects_second_active_card(self):
        Flashcard.objects.create(title="a", prompt="p", answer="a", source_claim=self.claim)
        with self.assertRaises(IntegrityError):
            Flashcard.objects.create(title="b", prompt="p", answer="a", source_claim=self.claim)

    def test_concurrent_insert_returns_winner(self):
        winner = Flashcard.objects.create(title="w", prompt="p", answer="a", source_claim=self.claim)
        service = FlashcardGenerationService()
        # Simulate the race: the pre-check misses, the insert collides.
        with patch.object(FlashcardGenerationService, "_existing_card", side_effect=[None, winner]), \
                patch("learning.services.flashcard_service.Flashcard.objects.get_or_create", side_effect=IntegrityError):
            self.assertEqual(service.generate_from_canonical_claim(self.claim), winner)


@override_settings(GEMINI_API_KEY="")
class FlashcardTaskTests(TestCase):
    def setUp(self):
        # Tasks call close_old_connections(); inside a TestCase transaction that
        # would close the test connection, so it is disabled here.
        patcher = patch("learning.tasks.close_old_connections")
        patcher.start()
        self.addCleanup(patcher.stop)
        self.concept = Concept.objects.create(name="Stacks", slug="stacks")
        self.claim = make_claim(self.concept, "A stack is last-in first-out.")

    def test_task_is_idempotent_under_retries(self):
        self.assertEqual(generate_flashcard_for_claim_task(self.claim.id)["status"], "created")
        self.assertEqual(generate_flashcard_for_claim_task(self.claim.id)["status"], "exists")
        self.assertEqual(Flashcard.objects.filter(source_claim=self.claim).count(), 1)

    def test_task_failure_records_error_and_bounds_attempts(self):
        with patch.object(FlashcardGenerationService, "generate_from_canonical_claim", side_effect=RuntimeError("db down")), \
                patch.object(generate_flashcard_for_claim_task, "retry", side_effect=RuntimeError("retry scheduled")):
            with self.assertRaisesMessage(RuntimeError, "retry scheduled"):
                generate_flashcard_for_claim_task(self.claim.id)
        self.claim.refresh_from_db()
        self.assertEqual(self.claim.flashcard_attempts, 1)
        self.assertIn("db down", self.claim.flashcard_error)
        CanonicalClaim.objects.filter(pk=self.claim.pk).update(flashcard_attempts=4)
        self.assertEqual(generate_flashcard_for_claim_task(self.claim.id)["status"], "exhausted")

    @patch("learning.tasks.generate_flashcard_for_claim_task.delay")
    def test_backfill_dispatches_only_due_claims(self, delay):
        CanonicalClaim.objects.filter(pk=self.claim.pk).update(created_at=timezone.now() - timedelta(hours=1))
        fresh = make_claim(self.concept, "A fresh claim still within grace.")
        exhausted = make_claim(self.concept, "A claim whose retries ran out.")
        CanonicalClaim.objects.filter(pk=exhausted.pk).update(created_at=timezone.now() - timedelta(hours=1), flashcard_attempts=9)
        carded = make_claim(self.concept, "A claim that already has a card.")
        Flashcard.objects.create(title="c", prompt="p", answer="a", source_claim=carded)
        CanonicalClaim.objects.filter(pk=carded.pk).update(created_at=timezone.now() - timedelta(hours=1))
        self.assertEqual(backfill_missing_flashcards_task()["dispatched"], 1)
        delay.assert_called_once_with(self.claim.id)
        self.assertNotIn(fresh.id, [call.args[0] for call in delay.call_args_list])


@override_settings(GEMINI_API_KEY="")
@patch("verification.services.concept_assignment.ConceptAssignmentService")
class DeferredVerificationTests(TestCase):
    def setUp(self):
        self.concept = Concept.objects.create(name="BFS", slug="bfs")
        self.source = Source.objects.create(name="Wikipedia", authority_score=0.90)
        self.document = SourceDocument.objects.create(source=self.source, title="Doc", raw_text="BFS uses a queue.")

    def _claim(self, text="BFS uses a queue."):
        claim = ExtractedClaim.objects.create(source_document=self.document, text=text)
        Evidence.objects.create(claim=claim, source=self.source, relation=Evidence.SUPPORTS, excerpt=text, relevance_score=0.90)
        return claim

    @patch("learning.tasks.generate_flashcard_for_claim_task.delay")
    def test_deferred_generation_dispatches_after_commit(self, delay, concept_service):
        concept_service.return_value.assign_concept.return_value = self.concept
        with self.captureOnCommitCallbacks(execute=False) as callbacks:
            result = ClaimVerificationService().verify_claim(self._claim(), defer_flashcard=True)
        self.assertIsNotNone(result["canonical_claim"])
        self.assertTrue(result["flashcard_deferred"])
        self.assertEqual(Flashcard.objects.count(), 0)
        delay.assert_not_called()  # nothing dispatched before commit
        for callback in callbacks:
            callback()
        delay.assert_called_once_with(result["canonical_claim"].id)

    @patch("learning.tasks.generate_flashcard_for_claim_task.delay", side_effect=ConnectionError("broker down"))
    def test_broker_failure_does_not_fail_verification(self, _delay, concept_service):
        concept_service.return_value.assign_concept.return_value = self.concept
        with self.captureOnCommitCallbacks(execute=True):
            result = ClaimVerificationService().verify_claim(self._claim(), defer_flashcard=True)
        self.assertTrue(CanonicalClaim.objects.filter(pk=result["canonical_claim"].pk).exists())

    def test_same_fact_from_two_sources_yields_one_card(self, concept_service):
        concept_service.return_value.assign_concept.return_value = self.concept
        other_source = Source.objects.create(name="Python docs", authority_score=0.95)
        first = ClaimVerificationService().verify_claim(self._claim("BFS uses a queue."))
        second_claim = ExtractedClaim.objects.create(
            source_document=SourceDocument.objects.create(source=other_source, title="Doc 2", raw_text="x"),
            text="BFS uses a queue!",
        )
        Evidence.objects.create(claim=second_claim, source=other_source, relation=Evidence.SUPPORTS,
                                url="https://docs.python.org/x", relevance_score=0.90)
        second = ClaimVerificationService().verify_claim(second_claim)
        self.assertEqual(first["canonical_claim"].id, second["canonical_claim"].id)
        self.assertFalse(second["canonical_created"])
        self.assertEqual(Flashcard.objects.count(), 1)
        # Corroborating evidence is attached to the original claim.
        self.assertTrue(first["claim"].evidence_items.filter(source=other_source).exists())

    def test_synchronous_default_still_creates_card(self, concept_service):
        concept_service.return_value.assign_concept.return_value = self.concept
        result = ClaimVerificationService().verify_claim(self._claim())
        self.assertIsNotNone(result["flashcard"])
        self.assertEqual(result["flashcard"].source_claim_id, result["canonical_claim"].id)


@override_settings(GEMINI_API_KEY="")
class ConceptAssignmentTests(TestCase):
    def setUp(self):
        cache.clear()
        self.root = Concept.objects.create(name="Computer Science & Engineering", slug="cse")
        self.ds = Concept.objects.create(name="Data Structures", slug="data-structures")
        self.tree = Concept.objects.create(name="Tree", slug="tree")
        self.bst = Concept.objects.create(name="Binary Search Tree", slug="binary-search-tree")
        ConceptRelationship.objects.create(from_concept=self.ds, to_concept=self.tree, relation_type="parent")
        ConceptRelationship.objects.create(from_concept=self.tree, to_concept=self.bst, relation_type="parent")
        invalidate_cached_graph()

    def test_graph_is_built_from_database(self):
        service = ConceptAssignmentService()
        self.assertEqual(service.graph.number_of_nodes(), 4)
        self.assertTrue(service.graph.has_edge(self.tree.id, self.bst.id))

    def test_longest_name_anchor_wins_without_llm(self):
        concept = ConceptAssignmentService().assign_concept("A binary search tree keeps keys ordered.")
        self.assertEqual(concept, self.bst)

    def test_no_anchor_falls_back_to_root_not_arbitrary_concept(self):
        self.assertEqual(ConceptAssignmentService().assign_concept("Monads compose effects."), self.root)

    def test_topic_hint_is_used_when_text_has_no_anchor(self):
        concept = ConceptAssignmentService().assign_concept("Rotations restore balance.", hint_concept_id=self.bst.id)
        self.assertEqual(concept, self.bst)

    @override_settings(GEMINI_API_KEY="k")
    @patch("verification.services.concept_assignment.genai.Client")
    def test_llm_cannot_pick_a_concept_outside_candidates(self, client_class):
        outsider = Concept.objects.create(name="Networking", slug="networking")
        invalidate_cached_graph()
        client_class.return_value.models.generate_content.return_value = MagicMock(
            text=f'{{"concept_id": {outsider.id}, "unmapped_concept_name": null}}'
        )
        concept = ConceptAssignmentService().assign_concept("A binary search tree keeps keys ordered.")
        self.assertEqual(concept, self.bst)
