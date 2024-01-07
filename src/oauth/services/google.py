import requests
from rest_framework.exceptions import AuthenticationFailed

from SoundApplication import settings
from src.oauth import serializer
from google.oauth2 import id_token

from src.oauth.models import AuthUser
from . import base_auth


def check_google_auth(google_user: serializer.GoogleAuth) -> dict:
    try:
        id_token.verify_oauth2_token(google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise AuthenticationFailed(code=403, detail='Dad data google')

    user, _ = AuthUser.objects.get_or_create(email=google_user['email'])
    return base_auth.create_token(user.id)