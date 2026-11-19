from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knowledge.models import ExtractedClaim
from .services.claim_verification import ClaimVerificationService
from users.permissions import IsProfileComplete

class VerifyClaimView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProfileComplete]

    def post(self, request, pk):
        extracted_claim = get_object_or_404(
            ExtractedClaim.objects.filter(
                source_document__uploaded_note__owner=request.user,
            ),
            id=pk,
        )

        verification_service = ClaimVerificationService()
        result = verification_service.verify_claim(extracted_claim)

        return Response(
            {
                "status": result["claim"].status,
                "confidence": str(result["claim"].confidence),
                "canonical_claim_id": result["canonical_claim"].id if result["canonical_claim"] else None,
                "evidence": [e.id for e in result["evidence"]],
                "flashcard_id": (
                    result["flashcard"].id 
                    if result["flashcard"] 
                    else None,
                ),
            },
            status=status.HTTP_200_OK,
        )
