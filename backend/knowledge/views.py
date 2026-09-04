from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import permissions, viewsets
from .models import CanonicalClaim, Evidence, Source, ExtractedClaim, SourceDocument
from .serializers import (
    CanonicalClaimSerializer, 
    EvidenceSerializer, 
    SourceSerializer,
    ExtractedClaimSerializer, 
    SourceDocumentSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.select_related("claim", "source")
    serializer_class = EvidenceSerializer
    permission_classes = [permissions.IsAdminUser]

class ExtractedClaimReviewViewSet(viewsets.ModelViewSet):
    queryset = ExtractedClaim.objects.select_related(
        "source_document",
        "reviewed_by",
        )
    serializer_class = ExtractedClaimSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(
            reviewed_by=self.request.user, 
            reviewed_at=timezone.now()
            )

class CanonicalClaimViewSet(viewsets.ModelViewSet):
    queryset = CanonicalClaim.objects.select_related(
        "concept",
        "source_claim",
        )
    serializer_class = CanonicalClaimSerializer
    permission_classes = [permissions.IsAdminUser]

class SourceDocumentViewSet(viewsets.ModelViewSet):
    queryset = SourceDocument.objects.select_related("source")
    serializer_class = SourceDocumentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)