from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthUser
        fields = ('avatar', 'country', 'city', 'bio', 'display_name')


class GoogleAuth(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
