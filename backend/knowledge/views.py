from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
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

class IngestionStatusView(APIView):
    """Staff-only operational status for external ingestion and card inventory."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from knowledge.ingestion.status import ingestion_status
        return Response(ingestion_status())


class IngestionRunView(APIView):
    """Staff-only: enqueue one bounded discovery run for an adapter."""
    permission_classes = [permissions.IsAdminUser]
    MAX_LIMIT = 10

    def post(self, request):
        from knowledge.ingestion.registry import ADAPTERS, topic_enabled
        from knowledge.tasks import discover_adapter_task

        adapter = str(request.data.get("adapter", ""))
        if adapter not in ADAPTERS:
            return Response({"detail": f"adapter must be one of {sorted(ADAPTERS)}"}, status=status.HTTP_400_BAD_REQUEST)
        topic = (request.data.get("topic") or "").strip()[:200] or None
        if adapter == "official_docs" and topic and not topic_enabled(adapter, topic):
            return Response({"detail": f"Source policy for official_docs:{topic} is not enabled."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            limit = min(max(int(request.data.get("limit", 3)), 1), self.MAX_LIMIT)
        except (TypeError, ValueError):
            return Response({"detail": "limit must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        result = discover_adapter_task.delay(adapter, topic=topic, limit=limit)
        return Response({"queued": True, "task_id": result.id, "adapter": adapter, "topic": topic, "limit": limit},
                        status=status.HTTP_202_ACCEPTED)
