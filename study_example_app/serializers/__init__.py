from django.contrib.auth.models import User
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from shopping_mall.models import ShoppingMallUser
from study_example_app.models import DjangoModel


@extend_schema_serializer(
    exclude_fields=("password",),  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Valid example 1",
            summary="short summary",
            description="longer description",
            value={
                "is_superuser": True,
                "username": "string",
                "first_name": "string",
                "last_name": "string",
                "email": "user@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": "2021-04-18 04:14:30",
                "user_type": "customer",
            },
            request_only=True,  # signal that example only applies to requests
            response_only=False,  # signal that example only applies to responses
        ),
    ],
)
class UserReadOnlySerializer(ModelSerializer):
    d = serializers.SerializerMethodField(method_name="get_field_custom")
    class Meta:
        model = User
        depth = 1
        fields = "__all__"


class DjangoModelSerializer(ModelSerializer):
    class Meta:
        model = DjangoModel
        fields = "__all__"


class Django2ModelSerializer(DjangoModelSerializer):
    a_field = serializers.CharField(help_text="sdfsdf")

    class Meta:
        model = DjangoModel
        fields = "__all__"


class Django3ModelSerializer(DjangoModelSerializer):
    b_field = serializers.CharField(help_text="sdfsdf22222")

    class Meta:
        model = DjangoModel
        fields = "__all__"

