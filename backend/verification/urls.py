from django.urls import path
from .views import VerifyClaimView

urlpatterns = [
    path("claims/<int:pk>/verify/", VerifyClaimView.as_view(), name="verify-claim"),
]