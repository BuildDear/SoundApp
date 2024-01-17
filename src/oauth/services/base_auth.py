from datetime import timedelta, datetime

import jwt
from django.conf import settings

from src.oauth.services.google import log_function_call

@log_function_call
def create_token(user_id: int) -> dict[str, str | int]:
    """Token creation"""
    access_token_expires: timedelta = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE
    )
    return {
        "user_id": user_id,
        "access_token": create_access_token(
            data={"user_id": user_id}, expires_delta=access_token_expires
        ),
        "token_type": "Token",
    }

@log_function_call
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Access token creation"""
    to_encode = data.copy()
    if expires_delta is not None:
        expire: datetime = datetime.utcnow() + expires_delta
    else:
        expire: datetime = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": "access"})
    encoded_jwt: str = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
