from datetime import datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from django.core.cache import cache

from custom_oauth2.models import (
    JWTAccessToken,
    RedisRefreshToken,
    RegisteredApplication,
)
from users.models import User


class JWTUtils:
    @staticmethod
    def generate_token(user: User, exp=None, iat=None) -> str:
        payload = {
            "iss": "pycon2023app",
            "exp": exp
            or datetime.utcnow() + timedelta(seconds=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"]),
            "name": user.name,
            "jti": user.id,
            "iat": iat or datetime.utcnow(),
            "username": user.username,
            "scope": ["read", "write"],
        }
        encoded_jwt: str = jwt.encode(
            payload=payload,
            key=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_SIGNING_KEY"],
            algorithm=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_ALGORITHM"],
        )
        return encoded_jwt

    @staticmethod
    def verify(token: str) -> bool:
        if not token:
            return False
        try:
            jwt.decode(
                token,
                key=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_SIGNING_KEY"],
                algorithms=[settings.OAUTH2_PROVIDER["ACCESS_TOKEN_ALGORITHM"]],
            )
        except jwt.ExpiredSignatureError:
            return False
        return True

    @staticmethod
    def get_payload(token: str) -> dict[str, Any]:
        return jwt.decode(
            token,
            key=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_SIGNING_KEY"],
            algorithms=[settings.OAUTH2_PROVIDER["ACCESS_TOKEN_ALGORITHM"]],
        )


REFRESH_PREFIX: str = "refresh_token"


class RedisUtil:
    @staticmethod
    def generate_token(
        token_str: str, user: User, application: RegisteredApplication = None, access_token: JWTAccessToken = None
    ) -> RedisRefreshToken:
        print("refresh_생성")
        redis_key: str = f"{settings.OAUTH2_PROVIDER['REFRESH_TOKEN_REDIS_KEY_PREFIX']}:{token_str}"
        now = datetime.utcnow()
        token_value = RedisRefreshToken(
            user=user,
            token=token_str,
            access_token=access_token,
            application=application or RegisteredApplication.objects.get(name="pycon-auth-server"),
            created=now,
            updated=now,
            revoked=now + timedelta(seconds=settings.OAUTH2_PROVIDER["REFRESH_TOKEN_EXPIRE_SECONDS"]),
        )
        cache.set(
            key=redis_key,
            value=token_value,
            timeout=settings.OAUTH2_PROVIDER["REFRESH_TOKEN_EXPIRE_SECONDS"],
        )

        return token_value

    @staticmethod
    def verify(token: str) -> bool:
        redis_key: str = f"{settings.OAUTH2_PROVIDER['REFRESH_TOKEN_REDIS_KEY_PREFIX']}:{token}"
        return bool(cache.pttl(redis_key))

    @staticmethod
    def get_payload(token: str) -> User:
        return cache.get(key=f"{settings.OAUTH2_PROVIDER['REFRESH_TOKEN_REDIS_KEY_PREFIX']}:{token}")

    @staticmethod
    def revoke(token: str) -> bool:
        return cache.delete(key=f"{settings.OAUTH2_PROVIDER['REFRESH_TOKEN_REDIS_KEY_PREFIX']}:{token}")
