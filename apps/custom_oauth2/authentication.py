from typing import Any, Dict

from drf_spectacular.contrib.django_oauth_toolkit import DjangoOAuthToolkitScheme
from oauth2_provider import exceptions
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.oauth2_backends import get_oauthlib_core

from custom_oauth2.utils import JWTUtils
from users.models import User


class PyCon2023AppOAuthAuthentication(OAuth2Authentication):
    def authenticate(self, request):
        oauthlib_core = get_oauthlib_core()
        valid, r = oauthlib_core.verify_request(request, scopes=[])
        if valid:
            return self.authenticate_credentials(r.access_token)
        request.oauth2_error = getattr(r, "oauth2_error", {})
        return None

    def authenticate_credentials(self, access_token: str):
        if JWTUtils.verify(token=access_token) is False:
            raise exceptions.AuthenticationFailed("Invalid token.")

        payload: Dict[str, Any] = JWTUtils.get_payload(token=access_token)

        return User(id=payload["jti"], name=payload["name"], username=payload["username"]), None


class PyCon2023AppOAuthToolkitScheme(DjangoOAuthToolkitScheme):
    target_class = "custom_oauth2.authentication.PyCon2023AppOAuthAuthentication"
