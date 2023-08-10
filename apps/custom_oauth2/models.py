# Create your models here.
from __future__ import annotations

import uuid
from datetime import datetime

from django.conf import settings
from django.db import models
from django_mysql import models as mysql_models
from oauth2_provider.generators import generate_client_id, generate_client_secret
from oauth2_provider.models import (  # AccessToken,; Application,; IDToken as _IDToken,; RefreshToken,
    AbstractAccessToken,
    AbstractApplication,
    AbstractGrant,
    AbstractIDToken,
    AbstractRefreshToken,
)
from oauth2_provider.settings import oauth2_settings

from users.models import User


class RegisteredApplication(AbstractApplication):
    class ClientType(models.TextChoices):
        CLIENT_PUBLIC = "public", "퍼블릭"
        CLIENT_CONFIDENTIAL = "confidential", "외부비공개"

    class GrantType(models.TextChoices):
        REFRESH_TOKEN = "refresh_token", "refresh토큰으로 Access토큰 재발급받는방식"
        GRANT_AUTHORIZATION_CODE = "authorization-code", "인증"
        GRANT_IMPLICIT = "implicit", "명시적"
        GRANT_PASSWORD = "password", "비밀번호 인증"
        GRANT_CLIENT_CREDENTIALS = "client-credentials", "클라 검증"
        GRANT_OPENID_HYBRID = "openid-hybrid", "open id"

    NO_ALGORITHM = ""
    RS256_ALGORITHM = "RS256"
    HS256_ALGORITHM = "HS256"
    ALGORITHM_TYPES = (
        (NO_ALGORITHM, "No OIDC support"),
        (RS256_ALGORITHM, "RSA with SHA-2 256"),
        (HS256_ALGORITHM, "HMAC with SHA-2 256"),
    )

    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(max_length=100, unique=True, default=generate_client_id, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        #  related_name="%(app_label)s_%(class)s",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    redirect_uris = models.TextField(
        blank=True,
        help_text="Allowed URIs list, space separated",
    )
    client_type = models.CharField(max_length=32, choices=ClientType.choices)

    client_secret = models.CharField(max_length=255, blank=True, default=generate_client_secret, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    skip_authorization = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    algorithm = models.CharField(max_length=5, choices=ALGORITHM_TYPES, default=NO_ALGORITHM, blank=True)

    authorization_grant_type = mysql_models.ListCharField(
        base_field=models.CharField(max_length=20, choices=GrantType.choices),
        size=6,
        max_length=(6 * 21),
    )

    def allows_grant_type(self, *grant_types):
        return bool(set(self.authorization_grant_type) & set(grant_types))

    class Meta:
        db_table = "pycon2023app_application"


class JWTAccessToken(AbstractAccessToken):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s",
    )
    source_refresh_token = models.OneToOneField(
        # unique=True implied by the OneToOneField
        to="RedisRefreshToken",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="jwt_access_token",
    )
    token = models.CharField(
        max_length=255,
        unique=True,
    )
    id_token = models.OneToOneField(
        to="IDToken",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="jwt_access_token",
    )
    application = models.ForeignKey(
        to="RegisteredApplication",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    expires = models.DateTimeField()
    scope = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def parse(token: str) -> JWTAccessToken:
        from custom_oauth2.utils import JWTUtils

        payload = JWTUtils.get_payload(token)
        return JWTAccessToken(
            user=User(
                id=payload["jti"],
                username=payload["username"],
                name=payload["name"],
            ),
            scope=payload["scope"],
            expires=payload["exp"],
            token=token,
            id_token=None,
            application=RegisteredApplication(name="pycon-auth-server"),
            source_refresh_token=None,
        )

    def revoke(self):
        # raise NotImplementedError("JWT는 revoke 불가...")
        return

    class Meta:
        # db_table = "pycon2023app_access_token"
        managed = False


class RedisManager(models.Manager):
    def get(self, token) -> RedisRefreshToken:
        from django.core.cache import cache

        refresh_token: RedisRefreshToken = cache.get(
            key=f"{settings.OAUTH2_PROVIDER['REFRESH_TOKEN_REDIS_KEY_PREFIX']}:{token}",
        )
        if not refresh_token:
            raise RedisRefreshToken.DoesNotExist()
        return refresh_token

    def create(
        self, user: User, token: str, application: RegisteredApplication, access_token: JWTAccessToken = None
    ) -> RedisRefreshToken:
        from custom_oauth2.utils import RedisUtil

        return RedisUtil.generate_token(token_str=token, user=user, application=application, access_token=access_token)


class RedisRefreshToken(AbstractRefreshToken):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="refresh_token")
    token = models.CharField(max_length=255)
    application = models.ForeignKey(to="RegisteredApplication", on_delete=models.CASCADE)
    access_token = models.OneToOneField(
        to="JWTAccessToken",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    revoked = models.DateTimeField(null=True)
    objects = RedisManager()

    def revoke(self) -> bool:
        """
        Mark this refresh token revoked and revoke related access token
        """
        from custom_oauth2.utils import RedisUtil

        # access_token_model = get_access_token_model()
        return RedisUtil.revoke(token=self.token)

    def save(self, *args, **kwargs) -> None:
        from django.core.cache import cache

        self.updated = datetime.utcnow()
        cache.set(
            key=f"{settings.OAUTH2_PROVIDER['REFRESH_TOKEN_REDIS_KEY_PREFIX']}:{self.token}",
            value=self,
            timeout=settings.OAUTH2_PROVIDER["REFRESH_TOKEN_EXPIRE_SECONDS"],
        )

    class Meta:
        # db_table = "pycon2023app_refresh_token"
        managed = False


class IDToken(AbstractIDToken):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="id_token",
    )
    jti = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="JWT Token ID")
    application = models.ForeignKey(
        to="RegisteredApplication",
        related_name="id_token",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    expires = models.DateTimeField()
    scope = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pycon2023app_id_token"


class Grant(AbstractGrant):
    CODE_CHALLENGE_PLAIN = "plain"
    CODE_CHALLENGE_S256 = "S256"
    CODE_CHALLENGE_METHODS = ((CODE_CHALLENGE_PLAIN, "plain"), (CODE_CHALLENGE_S256, "S256"))

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)  # code comes from oauthlib
    application = models.ForeignKey(oauth2_settings.APPLICATION_MODEL, on_delete=models.CASCADE, related_name="grants")
    expires = models.DateTimeField()
    redirect_uri = models.TextField()
    scope = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    code_challenge = models.CharField(max_length=128, blank=True, default="")
    code_challenge_method = models.CharField(max_length=10, blank=True, default="", choices=CODE_CHALLENGE_METHODS)

    nonce = models.CharField(max_length=255, blank=True, default="")
    claims = models.TextField(blank=True)

    class Meta:
        db_table = "pycon2023app_grant"
