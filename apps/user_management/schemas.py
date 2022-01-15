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

        # 지금은 단순히 User생성만
        instance: User = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            name_kor=validated_data["name_kor"],
            user_type=User.UserType.CUSTOMER,
            is_staff=False,
            is_active=True,
        )

        instance.user_permissions.add

        return instance

    def update(self, validated_data: Dict[str, Any], instance: User) -> User:

        return instance

    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_active", "phone", "name_kor", "registration_number")
        extra_kwargs = {
            "is_staff": {"read_only": True},
            "is_active": {"read_only": True},
        }
