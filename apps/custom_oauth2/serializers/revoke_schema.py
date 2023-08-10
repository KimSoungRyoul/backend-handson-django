from django.db.models import TextChoices
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers


class TokenTypeHint(TextChoices):
    REFRESH_TOKEN = "refresh_token", "redis에 저장된 리프레시토큰"
    ACCESS_TOKEN = "access_token", "OAUTH2스펙상 존재하지만 JWT라 폐기 불가능합니다."


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="토큰 폐기 포맷 예시",
            value={
                "token_type_hint": "refresh_token",
                "token": "784c2da2-0f74-4a07-8075-9f0fa29cddda",
                "client_id": "NIm1VMoRRnLODCmAgDmlAaeFjYnxk2qyiDo62ojZ",
            },
            request_only=True,
        ),
    ]
)
class RevokeRequestBody(serializers.Serializer):
    token_type_hint = serializers.ChoiceField(choices=TokenTypeHint.choices)
    token = serializers.CharField(max_length=512)
    client_id = serializers.CharField(max_length=128)
