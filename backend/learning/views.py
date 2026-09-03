from django.shortcuts import render
from django.db.models import Count,Sum
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Flashcard, FlashcardFeedback, SavedFlashcard, UserProgress
from .serializers import FlashcardSerializer, FlashcardFeedbackSerializer
# Create your views here.

class FlashcardFeedView(generics.ListAPIView):
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Flashcard.objects.filter(is_active=True)

class FlashcardDetailView(generics.RetrieveAPIView):
    serializer_class = FlashcardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Flashcard.objects.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            flashcard=instance,
        )
        progress.view_count += 1
        progress.last_viewed_at = timezone.now()
        progress.save(update_fields=['view_count', 'last_viewed_at'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class SaveFlashCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        flashcard = generics.get_object_or_404(
            Flashcard, 
            pk=pk, 
            is_active=True,
            )

        SavedFlashcard.objects.get_or_create(
            user=request.user,
            flashcard=flashcard,
        )

        return Response(
            {"status": "saved"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        flashcard = generics.get_object_or_404(
            Flashcard,
            pk=pk,
            is_active=True,
        )

        SavedFlashcard.objects.filter(
            user=request.user,
            flashcard=flashcard,
        ).delete()

        return Response(
            {"status": "unsaved"},
            status=status.HTTP_200_OK,
        )

class FlashcardFeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        flashcard = generics.get_object_or_404(
            Flashcard,
            pk=pk,
            is_active=True,
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
        total_viewed = progress.count()
        total_views = progress.aggregate(total=Sum('view_count'))['total'] or 0
        understood_count = progress.filter(understood=True).count()
        saved_count = SavedFlashcard.objects.filter(user=request.user).count()
        feedback_count = FlashcardFeedback.objects.filter(user=request.user).count()

        progress_summary = {
            "total_flashcards_viewed": total_viewed,
            "total_views": total_views,
            "understood_count": understood_count,
            "saved_count": saved_count,
            "feedback_count": feedback_count,
        }

        return Response(progress_summary, status=status.HTTP_200_OK)