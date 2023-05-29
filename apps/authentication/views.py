from typing import Final

from django.shortcuts import render
from drf_spectacular import openapi
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

AUTH_TAG: Final[str] = "인증"


#  path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
#     path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),


@extend_schema_view(
    post=extend_schema(
        tags=[AUTH_TAG],
        summary="로그인 API 입니다",
        description="""
        사용법 \n
        * access(토큰)을 Swagger 1시방향 Authorize -> jwtAuth 에 넣으면 인증된(로그인된) 상태로 다른 API를 사용할 수 있습니다.\n
        * 계정생성은 `django-backend-starter/apps` 하위에서 `python manage.py createsuperuser --username root` 커맨드를 수행하거나
          users/ POST API(회원가입) 를 사용하세요.
        """,
        examples=[OpenApiExample(request_only=True, name="로그인 샘플 포맷", value={"username": "root", "password": "1234"})],
    )
)
class AuthLoginAPIView(TokenObtainPairView):
    ...


@extend_schema_view(
    post=extend_schema(
        tags=[AUTH_TAG],
        summary="JWT access 토큰을 재발급 API",
        description="""
        access 토큰이 만료된 경우 refresh 토큰을 사용해서 access 토큰을 재발급 받을수 있습니다.
        """,
        examples=[
            OpenApiExample(
                name="토큰 재발급 포맷",
                value={
                    "refresh": "실제 발급받은 refresh 토큰을 넣으세요 ex: eyJhbGciOiJ...VCJ9.eyJ0b2...Njg1MzUzMDE1LCJqdGkiO...9.Dy...GcMszbe8"
                },
            )
        ],
    )
)
class AuthRefreshAPIView(TokenRefreshView):
    ...


@extend_schema_view(
    post=extend_schema(
        tags=[AUTH_TAG],
        summary="로그아웃 API (refresh 토큰을 BlackList에 넣어서 로그아웃 시킵니다)",
        description="""
        JWT 특성상 한번 발급한 토큰은 만료시킬 수 없습니다.
        따라서 한번 발급된 access 토큰은 만료되기 전까지 유효합니다.
        이로 인해 SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]를 짧게 가져갈것을 권장합니다.
        자세한 내용은 JWT 공식문서 참고
        """,
    )
)
class AuthTokenBlacklistView(TokenBlacklistView):
    ...
