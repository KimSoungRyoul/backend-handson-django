from aggregate.orders.models import Order
from django.contrib.auth.models import User
from django.http import HttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from study_example_app.models import DjangoModel
from study_example_app.schemas import (
    USER_CREATE_EXAMPLES,
    USER_CREATE_QUERY_PARAM_EXAMPLES,
)
from study_example_app.serializers import DjangoModelSerializer
from study_example_app.serializers.order_serializers import OrderSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(help_text="회원의 유형값을 받습니다.", default="customer")

    class Meta:
        model = User
        fields = "__all__"


@extend_schema_view(
    list=extend_schema(summary="이런식으로 class레벨 데코레이터로 문서 커스터마이징 가능하다.", tags=["사용자"]),
    i_am_custom_api=extend_schema(
        summary="@action API도 마찬가지로 class 데코레이터로 문서 커스터마이징 가능하다.",
        tags=["사용자"],
        request=CustomUserSerializer,
        responses={status.HTTP_200_OK: CustomUserSerializer},
    ),
)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        tags=["사용자"],
        summary="method레벨 데코레이터도 가능",
        parameters=[
            OpenApiParameter(name="a_param", description="QueryParam1 입니다.", required=False, type=str),
            OpenApiParameter(
                name="date_param",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="Filter by release date",
                examples=USER_CREATE_QUERY_PARAM_EXAMPLES,
            ),
        ],
        examples=USER_CREATE_EXAMPLES,
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        response: HttpResponse = super().create(request, *args, **kwargs)

        return response

    @action(
        detail=False,
        url_path="custom-action-api",
    )
    def i_am_custom_api(self, request: Request, *args, **kwargs):
        return Response(data={"hi": "i am custom api"})


class DjangoModelViewSet(ModelViewSet):
    queryset = DjangoModel.objects.all()
    queryset = DjangoModelSerializer

    @extend_schema(
        tags=["사용자"],
        summary="23232323",
        request=DjangoModelSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super(DjangoModelViewSet, self).create(request, *args, **kwargs)
