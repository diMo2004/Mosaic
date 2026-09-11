from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count,Sum
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Flashcard, FlashcardFeedback, Playlist, PlaylistItem, UserProgress
from .serializers import FlashcardSerializer, FlashcardFeedbackSerializer, PlaylistDetailSerializer, PlaylistSerializer
from knowledge.models import CanonicalClaim
# Create your views here.

def active_flashcards():
    return Flashcard.objects.filter(
        is_active=True
    ).select_related(
        "source_claim__concept",
        "source_claim__source_claim",
    )

class FlashcardFeedView(generics.ListAPIView):
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return active_flashcards()
    
class FlashcardDetailView(generics.RetrieveAPIView):
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return active_flashcards()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            flashcard=instance,
        )
        progress.view_count += 1
        progress.last_viewed_at = timezone.now()
        progress.save(update_fields=['view_count', 'last_viewed_at', 'updated_at'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class SaveFlashCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        Playlist.get_default_for_user(self.request.user)  # Ensure default playlist exists
        return Playlist.objects.filter(user=self.request.user).annotate(
            item_count=Count('items')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_default=False)

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        canonical_claim = get_object_or_404(
            CanonicalClaim.objects.select_related('concept','source_claim'),
            pk=pk,
            is_active=True,
        )
        evidence_items = []
        if canonical_claim.source_claim:
            evidence_items = canonical_claim.source_claim.evidence_items.select_related('source').all()

        return Response(
            {
                "canonical_claim": {
                    "id": canonical_claim.id,
                    "concept": canonical_claim.concept.name,
                    "text": canonical_claim.text,
                    "confidence": str(canonical_claim.confidence),
                },
                "explanation": (
                    f"{canonical_claim.text}\n\n"
                    "This explanation is grounded in the evidence listed below."
                    "LLM-generated explanation will be added later."
                ),
                "evidence": [
                    {
                        "source": evidence.source.name,
                        "title": evidence.title,
                        "url": evidence.url,
                        "excerpt": evidence.excerpt,
                        "relation": evidence.relation,
                        "relevance_score": str(evidence.relevance_score),
                    }
                    for evidence in evidence_items
                ],
            }
        )
    