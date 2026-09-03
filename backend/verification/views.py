from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knowledge.models import ExtractedClaim
from .services.claim_verification import ClaimVerificationService

class VerifyClaimView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            extracted_claim = ExtractedClaim.objects.get(id=pk)
        except ExtractedClaim.DoesNotExist:
            return Response(
                {"error": "ExtractedClaim not found."},
                status=status.HTTP_404_NOT_FOUND,
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