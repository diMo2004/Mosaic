from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import permissions, viewsets
from .models import Claim, Evidence, Source
from .serializers import ClaimSerializer, EvidenceSerializer, SourceSerializer

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

class ClaimReviewViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.select_related("created_from_note","reviewed_by")
    serializer_class = ClaimSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(
            reviewed_by=self.request.user, 
            reviewed_at=timezone.now()
            )
        