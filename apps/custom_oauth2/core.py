import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Tuple

from django.conf import settings
from oauthlib.common import Request
from oauthlib.oauth2 import Server
from oauthlib.oauth2.rfc6749 import catch_errors_and_unavailability
from oauthlib.oauth2.rfc6749.tokens import get_token_from_header

from custom_oauth2.utils import JWTUtils
from users.models import User


def custom_token_generator(request: Request, refresh_token=False) -> str:
    user: User = request.user
    iat = datetime.utcnow()
    exp = iat + timedelta(seconds=settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"])
    return JWTUtils.generate_token(user=user, exp=exp, iat=iat)


def custom_refresh_token_generator(request: Request, **kwargs) -> str:
    return str(uuid.uuid4())


class DRFOAuth2Server(Server):
    @catch_errors_and_unavailability
    def create_token_response(
        self, uri, http_method="POST", body=None, headers=None, credentials=None, grant_type_for_scope=None, claims=None
    ) -> Tuple[Dict[str, str], Dict[str, str], int]:
        headers, body, status = super().create_token_response(uri, http_method, body, headers, credentials)

        return headers, json.loads(body), status

    @catch_errors_and_unavailability
    def verify_request(self, uri, http_method="GET", body=None, headers=None, scopes=None):
        """Validate client, code etc, return body + headers"""
        request = Request(uri, http_method, body, headers)
        request.token_type = self.find_token_type(request)
        request.scopes = scopes
        access_token: str = get_token_from_header(request)
        request.access_token = access_token
        valid = JWTUtils.verify(access_token)
        return valid, request
        # token_type_handler: BearerToken = self.tokens.get(request.token_type, self.default_token_type_handler)
        # return token_type_handler.validate_request(request), request
