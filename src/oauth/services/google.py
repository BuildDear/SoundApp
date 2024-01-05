import requests
from rest_framework.exceptions import AuthenticationFailed

from src.oauth import serializer
from google.oauth2 import id_token


def check_google_auth(google_user: serializer.GoogleAuth):
    try:
        id_token.verify_oauth2_token(google_user['token'], requests.Request())
    except ValueError:
        return AuthenticationFailed(code=403, detail='Dad data google')
