from typing import Any
from typing import Dict

from rest_framework import serializers

from aggregate.users.models import User


class UserQueryParams(serializers.Serializer):
    ...


class UserSchema(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_active")


class UserDetailSchema(UserSchema):
    class Meta(UserSchema.Meta):
        excludes = ("password",)


class UserRequestBody(serializers.ModelSerializer):
    def create(self, validated_data: Dict[str, Any]) -> User:
        # .. 생성로직 구현
        return instance

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "is_staff": {"read_only": True},
            "is_active": {"read_only": True},
        }


class UserUpdateRequestBody(serializers.ModelSerializer):
    def update(self, validated_data: Dict[str, Any], instance: User) -> User:
        # .. 수정 로직 구현
        return instance

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
            "is_active",
            "phone",
            "name_kor",
            "registration_number",
        )
        extra_kwargs = {
            "is_staff": {"read_only": True},
            "is_active": {"read_only": True},
        }
