from django.contrib.auth import authenticate
from rest_framework import serializers

from . import models
from .models import AuthUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = models.AuthUser
        fields = [
            "email",
            "password",
        ]

    def create(self, validated_data):
        return AuthUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        return {"email": user.email, "username": user.username, "token": user.token}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthUser
        fields = ("avatar", "country", "city", "bio", "display_name")
        ref_name = "CustomUserSerializer"


class SocialLinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SocialLink
        fields = (
            "id",
            "link",
        )


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.AuthUser
        fields = (
            "id",
            "avatar",
            "country",
            "city",
            "bio",
            "display_name",
            "social_links",
        )


class GoogleAuth(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
