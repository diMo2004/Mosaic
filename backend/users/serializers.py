from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ""),
            password=validated_data['password']
        )

        UserProfile.objects.create(
            user=user,
            auth_provider=UserProfile.AUTH_PROVIDER_DJANGO,
            full_name=validated_data.get('username', ""),
        )
        return user

class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class CompleteProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True, allow_blank=False)
    education_level = serializers.CharField(required=True, allow_blank=False)
    learning_goal = serializers.CharField(required=True, allow_blank=False)
    interests = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
    )