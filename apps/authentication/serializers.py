import logging
from typing import Any

from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.middleware.csrf import logger
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenBlacklistSerializer,
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    학습목적으로 drf simple jwt 동작을 이해하기 쉽도록 그대로 가져온 것 뿐입니다.
    아래 구현은 rest_framework_simplejwt 의 TokenObtainPairSerializer 와 내부 동작이 동일합니다.
    """

    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        logger.info(f"로그인시 token에 담긴 정보11: {refresh}")
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if settings.SIMPLE_JWT["UPDATE_LAST_LOGIN"]:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        logger.info(
            f"로그인시 token에 담긴 정보:{token}",
        )

        return token


class AuthTokenBlacklistSerializer(TokenBlacklistSerializer):
    """
    학습목적으로 drf simple jwt 동작을 이해하기 쉽도록 그대로 가져온 것 뿐입니다.
    아래 구현은 rest_framework_simplejwt 의 TokenBlacklistSerializer 와 내부 동작이 동일합니다.
    """

    refresh = serializers.CharField(help_text="로그아웃 처리하고자 하는 refresh token을 넣어주세요.")
    token_class = RefreshToken

    def validate(self, attrs: dict[str, Any]):
        refresh: RefreshToken = RefreshToken(token=attrs["refresh"])
        try:
            refresh.blacklist()
        except AttributeError:
            pass
        return {}
