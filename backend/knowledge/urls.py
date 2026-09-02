from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ClaimReviewViewSet, EvidenceViewSet, SourceViewSet

router = DefaultRouter()
router.register("sources", SourceViewSet, basename="source")
router.register("evidence", EvidenceViewSet, basename="evidence")
router.register("claims", ClaimReviewViewSet, basename="claim")

urlpatterns = [
    path("", include(router.urls)),
]