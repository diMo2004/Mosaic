from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, GoogleAuthSerializer, CompleteProfileSerializer
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
import os

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

def jwt_response_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class GoogleAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
        try:
            payload = google_id_token.verify_oauth2_token(
                serializer.validated_data['id_token'],
                google_requests.Request(),
                client_id,
            )
        except ValueError:
            return Response(
                {"detail": "Invalid Google token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = payload.get('email')
        if not email:
            return Response(
                {"detail": "Google account did not provide an email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": payload.get("given_name", ""),
                "last_name": payload.get("family_name", ""),
            },
        )

        profile, _ = UserProfile.objects.get_or_create(user=user)

        if created or profile.auth_provider != UserProfile.AUTH_PROVIDER_GOOGLE:
            profile.auth_provider = UserProfile.AUTH_PROVIDER_GOOGLE

        if not profile.full_name:
            profile.full_name = payload.get("name", "")

        if not profile.google_picture_url:
            profile.google_picture_url = payload.get("picture", "")

        profile.save()
        profile.update_completion_status()

        missing_fields = profile.missing_required_fields()

        if missing_fields:
            return Response(
                {
                    "status": "profile_required",
                    **jwt_response_for_user(user),
                    "missing_fields": missing_fields,
                    "prefill": {
                        "email": user.email,
                        "full_name": profile.full_name,
                        "google_picture_url": profile.google_picture_url,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "status": "authenticated",
                **jwt_response_for_user(user),
            },
            status=status.HTTP_200_OK,
        )

class CompleteProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CompleteProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = request.user.profile
        for field, value in serializer.validated_data.items():
            setattr(profile, field, value)

        profile.update_completion_status()

        if not profile.profile_completed:
            return Response(
                {
                    "status": "profile_required",
                    "missing_fields": profile.missing_required_fields(),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                **jwt_response_for_user(request.user),
                "status": "authenticated",
                "profile_completed": True,
            },
            status=status.HTTP_200_OK,
        )