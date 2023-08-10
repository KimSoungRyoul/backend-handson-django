from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from users.models import User


class EmptySerializer(serializers.Serializer):
    ...


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="로그인 포맷 예시",
            value={
                "username": "root",
                "password": "1234",
                "grant_type": "password",
                "client_id": "NIm1VMoRRnLODCmAgDmlAaeFjYnxk2qyiDo62ojZ",
            },
            request_only=True,  # signal that example only applies to requests
            response_only=False,  # signal that example only applies to responses
        ),
        OpenApiExample(
            name="refresh_token으로 access_token 갱신 예시",
            value={
                "refresh_token": "bd61c69c-1d62-41e2-9f77-698aaf82199f",
                "grant_type": "refresh_token",
                "client_id": "NIm1VMoRRnLODCmAgDmlAaeFjYnxk2qyiDo62ojZ",
            },
            request_only=True,  # signal that example only applies to requests
            response_only=False,  # signal that example only applies to responses
        ),
    ]
)
class TokenRequestBody(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)
    grant_type = serializers.CharField(max_length=32)
    client_id = serializers.CharField(max_length=256)


class UserDetailSchema(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="응답 포맷 예시",
            value={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJkYXdubGlrZW4iLCJleHAiOjE2NTQyNzY1MzMsIm5hbWUiOiJcdWFlNDBcdWMxMzFcdWI4MmMiLCJqdGkiOjEsInVzZXJuYW1lIjoicm9vdCIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdfQ.7o995eSwdKIKwwf5d-oU_JmTZKEu8kJl-Zn90NFADc0",
                "expires_in": 36000,
                "token_type": "Bearer",
                "scope": "read write admin",
                "refresh_token": "db2638e8-214a-4c67-b930-c2bcbbc16ab6",
            },
        )
    ]
)
class TokenSchema(serializers.Serializer):
    access_token = serializers.CharField(max_length=512)
    expires_in = serializers.IntegerField(help_text="토큰 만료시간(sec)")
    token_type = serializers.CharField(max_length=32)
    scope = serializers.CharField(max_length=128)
    refresh_token = serializers.CharField(max_length=512)
    # user = UserDetailSchema(help_text="인증 회원 정보")


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="응답 포맷 예시",
            value={
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJkYXdubGlrZW4iLCJleHAiOjE2NTQyNzY1MzMsIm5hbWUiOiJcdWFlNDBcdWMxMzFcdWI4MmMiLCJqdGkiOjEsInVzZXJuYW1lIjoicm9vdCIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdfQ.7o995eSwdKIKwwf5d-oU_JmTZKEu8kJl-Zn90NFADc0",
                "expires_in": 36000,
                "token_type": "Bearer",
                "scope": "read write admin",
                "refresh_token": "db2638e8-214a-4c67-b930-c2bcbbc16ab6",
            },
        )
    ]
)
class IntrospectionSchema(serializers.Serializer):
    active = serializers.BooleanField()
    username = serializers.CharField(max_length=128)
    token_type = serializers.CharField(max_length=128)
    client_id = serializers.CharField(max_length=256)
