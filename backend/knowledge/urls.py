from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SourceDocumentViewSet, CanonicalClaimViewSet, ExtractedClaimReviewViewSet, EvidenceViewSet, SourceViewSet, IngestionRunView, IngestionStatusView

router = DefaultRouter()
router.register("sources", SourceViewSet, basename="source")
router.register("evidence", EvidenceViewSet, basename="evidence")
router.register("extracted-claims", ExtractedClaimReviewViewSet, basename="extracted-claim")
router.register("canonical-claims", CanonicalClaimViewSet, basename="canonical-claim")
router.register("source-documents", SourceDocumentViewSet, basename="source-document")

urlpatterns = [
    path("ingestion/status/", IngestionStatusView.as_view(), name="ingestion-status"),
    path("ingestion/run/", IngestionRunView.as_view(), name="ingestion-run"),
    path("", include(router.urls)),
]