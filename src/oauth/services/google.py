import functools
import logging

import requests
from rest_framework.exceptions import AuthenticationFailed

from SoundApplication import settings
from src.oauth import serializer
from google.oauth2 import id_token

from src.oauth.models import AuthUser
from . import base_auth

logger = logging.getLogger(__name__)


def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with arguments: {args}, {kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned: {result}")
        return result

    return wrapper


@log_function_call
def check_google_auth(google_user: serializer.GoogleAuth) -> dict:
    try:
        id_token.verify_oauth2_token(
            google_user["token"], requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise AuthenticationFailed(code=403, detail="Dad data google")

    user, _ = AuthUser.objects.get_or_create(email=google_user["email"])
    return base_auth.create_token(user.id)
