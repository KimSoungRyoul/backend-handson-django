from config.schema import OAS3Tag
from custom_oauth2.authentication import PyCon2023AppOAuthAuthentication
from custom_oauth2.models import JWTAccessToken, RedisRefreshToken
from custom_oauth2.serializers.revoke_schema import RevokeRequestBody
from custom_oauth2.serializers.token_schema import (
    EmptySerializer,
    IntrospectionSchema,
    TokenRequestBody,
    TokenSchema,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import EmptyQuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.views import extend_schema
from oauth2_provider.oauth2_backends import JSONOAuthLibCore, OAuthLibCore
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class DRFTokenViewSet(OAuthLibMixin, GenericViewSet):
    """
    OAuth2 API 표준 스펙 access Token 발급(provide) API
    refresh Token도 같이 발급합니다.

    Resource Owner Password Credentials
    -> grant_type은 password, refresh_token 2가지만 허용합니다.

    ref: https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.3
    """

    serializer_class = TokenRequestBody
    permission_classes = [AllowAny]
    queryset = EmptyQuerySet

    @extend_schema(
        summary="PyCon2023App 자체 인증(토큰 발급)",
        tags=[OAS3Tag.PyCon2023Auth],
        request=TokenRequestBody,
        responses=TokenSchema,
    )
    def create(self, request: Request, *args, **kwargs):
        if request.content_type == "application/json":
            core: JSONOAuthLibCore = self.get_oauthlib_core()
        elif request.content_type == "application/x-www-form-urlencoded":
            server = self.get_server()
            core: OAuthLibCore = OAuthLibCore(server)
        else:
            raise ValidationError(
                detail={"detail": "Content-Type은 application/json or application/x-www-form-urlencoded 만 허용합니다."}
            )

        url, headers, data, http_status = core.create_token_response(request)
        if http_status == 200:
            access_token = data.get("access_token")
            if access_token is not None:
                token = JWTAccessToken(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        return Response(data=data, status=http_status, headers=headers)


class DRFRevokeTokenView(OAuthLibMixin, GenericViewSet):
    """
    OAuth2 API 표준 스펙 refresh 토큰(or access 토큰) 폐기(revoke) API
    ref: https://datatracker.ietf.org/doc/html/rfc7009

    access Token은 JWT라 폐기가 안 됩니다.
    """

    queryset = EmptyQuerySet
    serializer_class = RevokeRequestBody
    authentication_classes = [PyCon2023AppOAuthAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="pycon2023App 자체 로그아웃 (토큰 폐기)",
        tags=[OAS3Tag.PyCon2023Auth],
    )
    def create(self, request: Request, *args, **kwargs):
        _url, headers, _, http_stats = self.create_revocation_response(request)
        return Response(data={"detail": "토큰이 폐기되었습니다."}, status=http_stats, headers=headers)


class DRFIntrospectTokenViewSet(OAuthLibMixin, GenericViewSet):
    """
    OAuth2 API 표준 스펙 introspection API
    ref: RFC 7662 https://tools.ietf.org/html/rfc7662

    #### access Token은 JWT라 해당 API로 조회할 필요 없습니다.
    """

    queryset = EmptyQuerySet
    serializer_class = EmptySerializer
    required_scopes = ["introspection"]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="refresh Token이 가지고 있는 정보 조회 (토큰 검토용으로 사용하면될듯)",
        parameters=[
            OpenApiParameter(
                "refresh_token", OpenApiTypes.STR, OpenApiParameter.QUERY, description="refresh_token만 넣으세요."
            ),
        ],
        responses={status.HTTP_200_OK: IntrospectionSchema},
        tags=[OAS3Tag.PyCon2023Auth],
    )
    def list(self, request: Request, *args, **kwargs):
        if not (token_value := request.query_params.get("refresh_token")):
            raise ValidationError(detail="refresh_token을 QueryParam형식으로 채워주세요.")
        try:
            refresh_token: RedisRefreshToken = RedisRefreshToken.objects.get(token=token_value)
        except ObjectDoesNotExist:
            return Response(data={"active": False}, status=status.HTTP_200_OK)
        else:
            data = {
                "iss": "pycon2023app",
                "active": True,
                "scope": refresh_token.access_token.scope,
                #  "exp": int(calendar.timegm(refresh_token.expires.timetuple())),
                "token_type": "refresh_token",
            }
            if refresh_token.application:
                data["client_id"] = refresh_token.application.client_id
            if refresh_token.user:
                data["username"] = refresh_token.user.get_username()

            data["user"] = {
                "id": request.user.id,
                "username": request.user.username,
                "name": request.user.name,
            }

            return Response(data=data, status=status.HTTP_200_OK)
