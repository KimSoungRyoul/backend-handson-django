from ninja import Schema
from pydantic import Field
from pydantic import validator
from rest_framework import serializers
from rest_framework.schemas import AutoSchema


class LoginSchema(Schema):
    username: str = Field(max_length=128, description="로그인시 사용하는 아이디")
    password: str = Field(
        min_length=8,
        max_length=16,
        description="비밀번호",
    )

    @validator("username")
    def check_username(cls, value: str):
        """
        메서드명을 자유롭게 작명 가능
        """
        # 원하는 validation 로직 작성
        return value


class LoginSchema(serializers.Serializer):
    username = serializers.CharField(max_length=128, help_text="로그인시 사용하는 아이디")
    password = serializers.CharField(min_length=8, max_length=16, help_text="비밀번호")

    def validate_username(self, attr: str):
        """
        메서드명에 "validated_" 라는 prefix가 필요하다.
        """
        # 원하는 validation 로직 작성
        return attr
