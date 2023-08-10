from datetime import datetime, timedelta

from custom_oauth2.models import JWTAccessToken, RedisRefreshToken
from django.conf import settings
from django.utils import timezone
from oauth2_provider.exceptions import FatalClientError
from oauth2_provider.models import AccessToken
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import Request
from oauthlib.oauth2 import OAuth2Token
from rest_framework.exceptions import ValidationError
from users.models import User


class PyCon2023AppOAuth2Validator(OAuth2Validator):
    def _create_access_token(
        self, expires, request: Request, token: OAuth2Token, source_refresh_token=None
    ) -> JWTAccessToken:
        user: User = request.user
        iat = datetime.utcnow()
        exp = iat + timedelta(seconds=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"])
        return JWTAccessToken(
            user=user,
            application=request.client,
            expires=exp,
            token=token["access_token"],
            created=iat,
            updated=iat,
        )

    def _create_refresh_token(
        self, request: Request, refresh_token_code: str, access_token: JWTAccessToken
    ) -> RedisRefreshToken:
        user: User = request.user
        return RedisRefreshToken.objects.create(
            user=user,
            access_token=access_token,
            token=refresh_token_code,
            application=request.client,
        )

    def revoke_token(self, token, token_type_hint, request, *args, **kwargs):
        """
        Revoke an access or refresh token.

        :param token: The token string.
        :param token_type_hint: access_token or refresh_token.
        :param request: The HTTP Request (oauthlib.common.Request)
        """
        if token_type_hint not in ["access_token", "refresh_token"]:
            raise ValidationError(detail={"detail": "token_type_hint는 refresh_token만 사용가능합니다"})
        try:
            refresh_token: RedisRefreshToken = RedisRefreshToken.objects.get(token=token)
        except RedisRefreshToken.DoesNotExist:
            raise ValidationError(detail={"detail": "존재하지 않는 token(refresh_token)입니다."})

        if refresh_token.revoke() is False:
            raise ValidationError(detail={"detail": "이미 만료되었거나 존재하지 않는 RefreshToken입니다."})

    def _load_access_token(self, token):
        return AccessToken.objects.select_related("application", "user").filter(token=token).first()

    def validate_bearer_token(self, token, scopes, request):
        """
        When users try to access resources, check that provided token is valid
        """
        if not token:
            return False

        introspection_url = oauth2_settings.RESOURCE_SERVER_INTROSPECTION_URL
        introspection_token = oauth2_settings.RESOURCE_SERVER_AUTH_TOKEN
        introspection_credentials = oauth2_settings.RESOURCE_SERVER_INTROSPECTION_CREDENTIALS

        access_token = self._load_access_token(token)

        # if there is no token or it's invalid then introspect the token if there's an external OAuth server
        if not access_token or not access_token.is_valid(scopes):
            if introspection_url and (introspection_token or introspection_credentials):
                access_token = self._get_token_from_authentication_server(
                    token, introspection_url, introspection_token, introspection_credentials
                )

        if access_token and access_token.is_valid(scopes):
            request.client = access_token.application
            request.user = access_token.user
            request.scopes = scopes

            # this is needed by django rest framework
            request.access_token = access_token
            return True
        else:
            self._set_oauth2_error_on_request(request, access_token, scopes)
            return False

    def validate_refresh_token(self, refresh_token, client, request, *args, **kwargs):
        """
        Check refresh_token exists and refers to the right client.
        Also attach User instance to the request object
        """
        try:
            rt = RedisRefreshToken.objects.get(token=refresh_token)
        except RedisRefreshToken.DoesNotExist:
            raise ValidationError({"detail": "존재하지 않거나 이미 만료된 refresh_token입니다."})

        if not rt:
            return False

        request.user = rt.user
        request.refresh_token = rt.token
        # Temporary store RefreshToken instance to be reused by get_original_scopes and save_bearer_token.
        request.refresh_token_instance = rt
        return rt.application == client

    def get_original_scopes(self, refresh_token, request, *args, **kwargs):
        # Avoid second query for RefreshToken since this method is invoked *after*
        # validate_refresh_token.
        rt = request.refresh_token_instance
        if not rt.access_token:
            return ""

        return rt.access_token.scope

    def save_bearer_token(self, token, request, *args, **kwargs):
        """
        Save access and refresh token, If refresh token is issued, remove or
        reuse old refresh token as in rfc:`6`

        @see: https://tools.ietf.org/html/draft-ietf-oauth-v2-31#page-43
        """

        if "scope" not in token:
            raise FatalClientError("access_token을 갱신할 권한(scope)이 없습니다")

        # expires_in is passed to Server on initialization
        # custom server class can have logic to override this
        expires = timezone.now() + timedelta(
            seconds=token.get(
                "expires_in",
                oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            )
        )

        if request.grant_type == "client_credentials":
            request.user = None
        # 재생성될 refresh_token Key값
        refresh_token_code = token.get("refresh_token", None)

        if refresh_token_code and self.rotate_refresh_token(request) is True:
            refresh_token_instance: RedisRefreshToken = getattr(request, "refresh_token_instance", None)
            # 기존에 생성되어있던 RefreshToken은 request에서 제거
            if refresh_token_instance:
                RedisRefreshToken.objects.get(token=refresh_token_instance.token).revoke()

            request.refresh_token_instance = RedisRefreshToken.objects.create(
                user=User.objects.get(id=request.user.id),
                access_token=JWTAccessToken.parse(token["access_token"]),
                token=refresh_token_code,
                application=request.client,
            )
        else:
            self._create_access_token(expires, request, token)
