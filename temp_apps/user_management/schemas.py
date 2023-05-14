from typing import Any, Dict

from aggregate.users.models import User
from rest_framework import serializers


class UserQueryParams(serializers.Serializer):
    ...


class UserSchema(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_active")


class UserDetailSchema(UserSchema):
    # full_name = serializers.SerializerMethodField(method_name="full_name_function")
    #
    # def full_name_function(self, obj:User) -> str:
    #     full_name: str = obj.last_name + obj.first_name
    #     return full_name

    class Meta(UserSchema.Meta):
        fields = ("id", "username", "email", "first_name", "last_name", "full_name", "owned_store_count")


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
