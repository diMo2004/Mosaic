from django.shortcuts import render
from django.shortcuts import get_object_or_404
import logging

from django.db.models import Case, Count, Exists, F, IntegerField, OuterRef, Q, Subquery, Sum, Value, When
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta
from uuid import UUID, uuid4
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Flashcard, FlashcardFeedEvent, FlashcardFeedback, Playlist, PlaylistItem, UserProgress, MasteryBadge, Questionnaire
from .serializers import FlashcardSerializer, FlashcardFeedbackSerializer, PlaylistDetailSerializer, PlaylistSerializer, MasteryBadgeSerializer, QuestionnaireQuestionClientSerializer, QuestionnaireQuestionReviewSerializer
from knowledge.models import CanonicalClaim, Concept
from .services.rag_explanation import RAGExplanationServiceError
from users.permissions import IsProfileComplete
from .services.mastery_service import MasteryService

logger = logging.getLogger(__name__)

def active_flashcards():
    return Flashcard.objects.filter(
        is_active=True
    ).select_related(
        "source_claim__concept",
        "source_claim__source_claim__source_document__source",
    )


def feed_eligible_flashcards():
    """Cards the public feed may serve: active, with an active verified canonical claim."""
    return active_flashcards().filter(
        source_claim__isnull=False,
        source_claim__is_active=True,
    )


FEED_REPEAT_COOLDOWN = timedelta(days=7)
FEED_RECENT_SERVE_PENALTY = timedelta(hours=24)
FEED_EXHAUSTED_RETRY_SECONDS = 120


class FlashcardFeedView(generics.ListAPIView):
    """Server-ranked, continuously replenished feed.

    Pagination uses a server-side session cursor: ``session_id`` identifies the
    feed session and every card already served in it is excluded, so pages
    never repeat and newly persisted cards appear on the next page without a
    client reset. Ranking (all in the database):

    0. never viewed and not served to this user in the last 24h, newest first;
    1. viewed/served, but not within the 7-day cool-down, least recent first;
    2. viewed/served recently, least recent first (only when inventory is short).

    Within a page, cards are interleaved by concept to avoid runs of one topic.
    """
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        return feed_eligible_flashcards()

    def list(self, request, *args, **kwargs):
        raw_session_id = request.query_params.get("session_id") or request.query_params.get("cursor")
        try:
            session_id = UUID(raw_session_id) if raw_session_id else uuid4()
        except (TypeError, ValueError):
            session_id = uuid4()

        try:
            limit = min(max(int(request.query_params.get("limit", 20)), 1), 50)
        except ValueError:
            limit = 20

        now = timezone.now()
        user_events = FlashcardFeedEvent.objects.filter(user=request.user, flashcard=OuterRef("pk"))
        candidates = (
            self.get_queryset()
            .exclude(Exists(user_events.filter(session_id=session_id)))
            .annotate(
                last_viewed=Subquery(
                    UserProgress.objects.filter(user=request.user, flashcard=OuterRef("pk"))
                    .values("last_viewed_at")[:1]
                ),
                last_served=Subquery(
                    user_events.filter(event_type=FlashcardFeedEvent.EVENT_SERVED)
                    .order_by("-created_at").values("created_at")[:1]
                ),
            )
            .annotate(last_seen=Coalesce("last_viewed", "last_served"))
            .annotate(
                feed_tier=Case(
                    When(last_viewed__isnull=True, last_served__isnull=True, then=Value(0)),
                    When(last_viewed__isnull=True, last_served__lt=now - FEED_RECENT_SERVE_PENALTY, then=Value(0)),
                    When(last_seen__lt=now - FEED_REPEAT_COOLDOWN, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            )
            .order_by("feed_tier", F("last_seen").asc(nulls_first=True), "-created_at", "-id")
        )
        pool = list(candidates[: limit * 3])
        if not pool:
            logger.info("feed.page.empty eligible_total=%s", self.get_queryset().count())
            response = Response({
                "results": [],
                "session_id": str(session_id),
                "cursor": str(session_id),
                "has_more": False,
                "session_exhausted": True,
                "retry_after_seconds": FEED_EXHAUSTED_RETRY_SECONDS,
            })
            response["Cache-Control"] = "no-store"
            return response

        selected = self._interleave_by_concept(pool)[:limit]
        FlashcardFeedEvent.objects.bulk_create([
            FlashcardFeedEvent(
                user=request.user,
                flashcard=card,
                session_id=session_id,
                event_type=FlashcardFeedEvent.EVENT_SERVED,
            )
            for card in selected
        ])
        exhausted = len(selected) == len(pool)
        response = Response({
            "results": self.get_serializer(selected, many=True).data,
            "session_id": str(session_id),
            "cursor": str(session_id),
            "has_more": not exhausted,
            "session_exhausted": exhausted,
            "repeated_count": sum(1 for card in selected if card.feed_tier == 2),
            "retry_after_seconds": FEED_EXHAUSTED_RETRY_SECONDS if exhausted else None,
        })
        response["Cache-Control"] = "no-store"
        return response

    @staticmethod
    def _interleave_by_concept(cards):
        """Stable round-robin across concepts within each tier."""
        ordered = []
        for tier in sorted({card.feed_tier for card in cards}):
            buckets = {}
            for card in cards:
                if card.feed_tier == tier:
                    buckets.setdefault(card.source_claim.concept_id, []).append(card)
            queues = list(buckets.values())
            while queues:
                for queue in list(queues):
                    ordered.append(queue.pop(0))
                    if not queue:
                        queues.remove(queue)
        return ordered


class TopicSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get(self, request):
        import difflib
        query = " ".join(request.query_params.get("topic", "").split())
        if not query:
            return Response({"detail": "A topic query is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Exact match (case-insensitive)
        exact = Concept.objects.filter(name__iexact=query).first()
        if exact:
            cards = active_flashcards().filter(source_claim__concept=exact)
            return Response({
                "query": query,
                "taxonomy_match": {
                    "found": True,
                    "confidence": 1.0,
                    "match_type": "exact",
                    "concept_id": exact.id,
                    "name": exact.name,
                },
                "suggestions": [{"concept_id": exact.id, "name": exact.name, "score": 1.0}],
                "results": FlashcardSerializer(cards[:30], many=True, context={"request": request}).data,
            })

        # 2. Substring & Trigram/Fuzzy matching
        all_concepts = list(Concept.objects.values("id", "name", "slug"))
        scored = []
        normalized_query = query.lower()
        for c in all_concepts:
            c_name_lower = c["name"].lower()
            ratio = difflib.SequenceMatcher(None, normalized_query, c_name_lower).ratio()
            # Boost if substring match
            if normalized_query in c_name_lower:
                ratio = max(ratio, 0.85)
            if ratio >= 0.35:
                scored.append((ratio, c))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_matches = scored[:5]

        if top_matches:
            best_score, best_concept_dict = top_matches[0]
            target_id = best_concept_dict["id"]
            target_name = best_concept_dict["name"]
            is_confident = best_score >= 0.70

            cards = active_flashcards().filter(source_claim__concept_id=target_id)
            suggestions = [
                {"concept_id": item[1]["id"], "name": item[1]["name"], "score": round(item[0], 2)}
                for item in top_matches
            ]

            return Response({
                "query": query,
                "taxonomy_match": {
                    "found": is_confident,
                    "confidence": round(best_score, 2),
                    "match_type": "fuzzy" if is_confident else "none",
                    "concept_id": target_id,
                    "name": target_name,
                },
                "suggestions": suggestions,
                "results": FlashcardSerializer(cards[:30], many=True, context={"request": request}).data,
            })

        # 3. No match found
        return Response({
            "query": query,
            "taxonomy_match": {
                "found": False,
                "confidence": 0.0,
                "match_type": "none",
                "concept_id": None,
                "name": None,
            },
            "suggestions": [],
            "results": [],
        })

    
class FlashcardDetailView(generics.RetrieveAPIView):
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        return active_flashcards()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        record_flashcard_view(request.user, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


def record_flashcard_view(user, flashcard):
    now = timezone.now()
    UserProgress.objects.get_or_create(user=user, flashcard=flashcard)
    UserProgress.objects.filter(user=user, flashcard=flashcard).update(
        view_count=F("view_count") + 1,
        last_viewed_at=now,
        updated_at=now,
    )


class FlashcardViewedView(APIView):
    """Record a card impression from the paged feed."""

    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def post(self, request, pk):
        flashcard = get_object_or_404(active_flashcards(), pk=pk)
        record_flashcard_view(request.user, flashcard)
        try:
            session_id = UUID(request.data.get("session_id"))
        except (TypeError, ValueError):
            session_id = None
        if session_id:
            FlashcardFeedEvent.objects.get_or_create(
                user=request.user,
                flashcard=flashcard,
                session_id=session_id,
                event_type=FlashcardFeedEvent.EVENT_VIEWED,
            )
        progress = UserProgress.objects.get(user=request.user, flashcard=flashcard)
        return Response(
            {
                "flashcard_id": flashcard.id,
                "view_count": progress.view_count,
                "last_viewed_at": progress.last_viewed_at,
            },
            status=status.HTTP_200_OK,
        )

class SaveFlashCardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def post(self, request, pk):
        flashcard = get_object_or_404(
            active_flashcards(), 
            pk=pk, 
        )
        playlist_id = request.data.get("playlist_id")

        if playlist_id:
            playlist = get_object_or_404(
                Playlist,
                pk=playlist_id,
                user=request.user,
            )
        else:
            playlist = Playlist.get_default_for_user(request.user)

        PlaylistItem.objects.get_or_create(
            playlist=playlist,
            flashcard=flashcard,
        )

        return Response(
            {"status": "saved", "playlist_id": playlist.id},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        flashcard = get_object_or_404(
            active_flashcards(),
            pk=pk
        )

        playlist_id = request.query_params.get("playlist_id")
        items = PlaylistItem.objects.filter(
            flashcard=flashcard,
            playlist__user=request.user,
        )
        if playlist_id:
            items = items.filter(playlist_id=playlist_id, playlist__user=request.user)
        items.delete()

        return Response(
            {"status": "unsaved"},
            status=status.HTTP_200_OK,
        )

class FlashcardFeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def post(self, request, pk):
        flashcard = get_object_or_404(
            active_flashcards(),
            pk=pk
        )
        serializer = FlashcardFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            flashcard=flashcard,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProgressSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get(self, request):
        progress = UserProgress.objects.filter(user=request.user)
        saved_count = (
            PlaylistItem.objects.filter(playlist__user=request.user)
            .values("flashcard_id")
            .distinct()
            .count()
        )

        return Response(
            {
                "total_flashcards_viewed": progress.count(),
                "total_views": progress.aggregate(total=Sum("view_count"))['total'] or 0,
                "understood_count": progress.filter(understood=True).count(),
                "saved_count": saved_count,
                "feedback_count": FlashcardFeedback.objects.filter(user=request.user).count(),
            },
            status=status.HTTP_200_OK,
        )

class PlaylistListCreateView(generics.ListCreateAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        Playlist.get_default_for_user(self.request.user)  # Ensure default playlist exists
        return Playlist.objects.filter(user=self.request.user).annotate(
            item_count=Count('items')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_default=False)

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PlaylistDetailSerializer
        return PlaylistSerializer

    def perform_destroy(self, instance):
        if instance.is_default:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Default playlist cannot be deleted.")
        instance.delete()

class GroundedExplanationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def get(self, request, pk):
        canonical_claim = get_object_or_404(
            CanonicalClaim.objects.select_related('concept','source_claim'),
            pk=pk,
            is_active=True,
        )

        from learning.services.rag_explanation import RAGExplanationService

        try:
            rag_service = RAGExplanationService()
            result = rag_service.generate_explanation(canonical_claim)
        except RAGExplanationServiceError as e:
            return Response(
                {
                    "detail": (
                        "A grounded explanation is temporarily unavailable."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        
        return Response(
            {
                "canonical_claim": {
                    "id": canonical_claim.id,
                    "concept": canonical_claim.concept.name,
                    "text": canonical_claim.text,
                    "confidence": str(canonical_claim.confidence),
                },
                "explanation": result["explanation"],
                "evidence": [
                    self._serialize_evidence(
                        evidence,
                        citation_number=index,
                    )
                    for index, evidence in enumerate(
                        result["evidence"], 
                        start=1,
                    )
                ],
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _serialize_evidence(evidence, *, citation_number: int) -> dict:
        serialized = {
            "citation": citation_number,
            "id": evidence.id,
            "source": (
                evidence.source.name
                if evidence.source_id
                else "Unknown Source"
            ),
            "title": evidence.title,
            "url": evidence.url,
            "excerpt": evidence.excerpt,
            "relation": evidence.relation,
            "relevance_score": str(evidence.relevance_score)
        }

        distance = getattr(evidence, "distance", None)
        if distance is not None:
            serialized["distance"] = float(distance)

        return serialized


class ConceptMasteryStatusView(APIView):
    def get(self, request, pk):
        try:
            concept = Concept.objects.get(pk=pk)
        except Concept.DoesNotExist:
            return Response({"detail": "Concept not found"}, status=status.HTTP_404_NOT_FOUND)
        service = MasteryService()
        current_tier = service.get_user_current_tier(request.user, concept)
        eligibility = service.check_eligibility_for_tier(
            request.user, concept, min(current_tier, 5)
        )
        has_badge = MasteryBadge.objects.filter(user=request.user, concept=concept).exists()
        return Response({
            "concept_id": concept.id,
            "concept_name": concept.name,
            "current_tier": current_tier,
            "eligibility": eligibility,
            "is_mastered": has_badge,
        })
class StartQuestionnaireView(APIView):
    def post(self, request, pk):
        try:
            concept = Concept.objects.get(pk=pk)
        except Concept.DoesNotExist:
            return Response({"detail": "Concept not found"}, status=status.HTTP_404_NOT_FOUND)
        service = MasteryService()
        try:
            questionnaire = service.generate_questionnaire(request.user, concept)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        questions = questionnaire.questions.all()
        return Response({
            "questionnaire_id": questionnaire.id,
            "concept": concept.name,
            "tier": questionnaire.tier,
            "passing_threshold": questionnaire.passing_threshold,
            "questions": QuestionnaireQuestionClientSerializer(questions, many=True).data,
        })
class SubmitQuestionnaireView(APIView):
    def post(self, request, pk):
        try:
            questionnaire = Questionnaire.objects.get(pk=pk, user=request.user)
        except Questionnaire.DoesNotExist:
            return Response({"detail": "Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
        if questionnaire.status != Questionnaire.STATUS_IN_PROGRESS:
            return Response({"detail": "Questionnaire already submitted"}, status=status.HTTP_400_BAD_REQUEST)
        answers = request.data.get("answers", [])
        service = MasteryService()
        result = service.grade_questionnaire(questionnaire, answers)
        result["review"] = QuestionnaireQuestionReviewSerializer(
            questionnaire.questions.all(), many=True
        ).data
        return Response(result)
class UserMasteryBadgesView(APIView):
    def get(self, request):
        badges = MasteryBadge.objects.filter(user=request.user).select_related("concept")
        return Response(MasteryBadgeSerializer(badges, many=True).data)

class FlashcardUnderstoodView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def post(self, request, pk):
        flashcard = get_object_or_404(
            active_flashcards(),
            pk=pk
        )
        understood = request.data.get("understood", True)
        if isinstance(understood, str):
            understood = understood.lower() in ("true", "1", "yes")
        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            flashcard=flashcard,
        )

        now = timezone.now()
        progress.understood = bool(understood)
        progress.understood_at = now if progress.understood else None
        progress.updated_at = now
        progress.save(update_fields=['understood', 'understood_at', 'updated_at'])

        return Response(
            {
                "flashcard_id": flashcard.id,
                "understood": progress.understood,
                "understood_at": progress.understood_at,
            },
            status=status.HTTP_200_OK,
        )
