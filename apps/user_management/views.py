from typing import Any, List, Type

from aggregate.products.models import Customer2, PurchaseDescriptions
from aggregate.stores.models import Store
from aggregate.users.models import Staff, User
from aggregate.users.serializers import UserSerializer
from django.db import models
from django.db.models import Prefetch, QuerySet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from study_example_app.schemas import USER_CREATE_QUERY_PARAM_EXAMPLES
from user_management.schemas import UserDetailSchema, UserRequestBody, UserSchema
from user_management.serializers import (
    StaffDetailSchema,
    StaffSchema,
    UserQueryParamSerializer,
)

# Create your views here.


class _UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    학습용 UserViewSet
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.http_request_packet)
        return Response(serializer.http_request_packet, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request: Request, *args, **kwargs):
        qp_serializer = UserQueryParamSerializer(data=request.query_params)
        qp_serializer.is_valid(raise_exception=True)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.http_request_packet)


from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    extend_schema_serializer,
    extend_schema_view,
)
from rest_framework import serializers, viewsets
from rest_framework.viewsets import GenericViewSet

# from rest_framework.generics import get_object_or_404


@extend_schema_serializer(
    # many=True # 주석을 풀면 API 문서상 array 형태로 명시됩니다.
    # exclude_fields = ["int_data"] # 주석을 풀면 int_data가 API 문서상에서 제외됩니다.
    examples=[
        OpenApiExample(
            "CustomSchemaEx1",
            summary="CustomSchema예제1",
            description="예제에 대한 설명",
            value={"int_data": 1234, "str_data": "커스텀스키마 str data 예시입니다.", "date_data": "1997-12-19"},
            request_only=True,  # request 예제로만 사용 가능합니다.
            response_only=False,  # response 예시로 사용못하게 막습니다.
        ),
        OpenApiExample(
            "CustomSchemaEx2",
            summary="CustomSchema예제2",
            description="예제에 대한 설명2",
            value={"int_data": 4321, "str_data": "커스텀스키마 str data 예시입니다222.", "date_data": "2022-11-19"},
            request_only=True,  # request 예제로만 사용 가능합니다.
            response_only=False,  # response 예시로 사용못하게 막습니다.
        ),
    ]
)
class CustomSchema(serializers.Serializer):
    int_data = serializers.IntegerField(help_text="숫자 데이터")
    str_data = serializers.IntegerField(help_text="문자열 데이터")
    date_data = serializers.DateField(help_text="날짜 데이터")


class CustomResponse(serializers.Serializer):
    detail = serializers.CharField(help_text="요청 결과에 대한 메시지")


class CustomErrorResponse(serializers.Serializer):
    message = serializers.CharField(help_text="400에러가 발생한 이유에 대해 서술합니다.")


# @extend_schema_view(
#     list=extend_schema(summary="회원 목록조회", tags=["회원관리"]),
#     retrieve=extend_schema(summary="회원 상세조회", tags=["회원관리"]),
#     create=extend_schema(summary="회원 가입", tags=["회원관리"]),
#     update=extend_schema(summary="회원 수정", tags=["회원관리"]),
#     partial_update=extend_schema(summary="회원 부분 수정", tags=["회원관리"]),
#     asdf=extend_schema(summary="asdf", tags=["회원관리"]),
# )
class UserViewSet(viewsets.GenericViewSet):
    """
    ModelViewSet을 활용한
    """

    queryset = User.objects.all()
    serializer_class = UserSchema
    # serializer_classes = {
    #     "list": UserSchema,
    #     "retrieve": UserDetailSchema,
    #     "create": UserRequestBody,
    #     "update": UserRequestBody,
    #     "partial_update": UserRequestBody,
    # }

    @extend_schema(summary="회원 목록조회", tags=["회원관리"])
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(summary="회원 상세조회", tags=["회원관리"])
    def retrieve(
        self,
        request: Request,
        pk: str,
    ) -> Response:
        instance: User = get_object_or_404(queryset=User.objects.filter(id=pk))
        serializer = UserDetailSchema(instance)
        return Response(serializer.data)

    from drf_spectacular.types import OpenApiTypes
    from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

    @extend_schema(
        operation_id="signup-api",  #
        parameters=[
            OpenApiParameter(
                name="date_param",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="Filter by release date",
                examples=[
                    OpenApiExample(
                        "이것은 Query Parameter Example입니다.",
                        summary="날짜예제1",
                        description="longer description",
                        value="1993-08-23",
                    ),
                    OpenApiExample(
                        "이것은 Query Parameter Example2입니다.",
                        summary="날짜예제2",
                        description="longer description",
                        value="2020-11-23",
                    ),
                    OpenApiExample(
                        "이것은 Query Parameter Example3입니다.",
                        summary="날짜예제3",
                        description="longer description",
                        value="2002-02-02",
                    ),
                ],
            ),
        ],
        summary="회원 가입",
        tags=["회원관리"],
    )
    def create(self, request, *args, **kwargs):
        serializer = UserRequestBody(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary="회원 수정",
        tags=["회원관리"],
    )
    def update(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        instance: User = get_object_or_404(queryset=User.objects.filter(id=pk))
        serializer = UserRequestBody(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="회원 부분 수정", tags=["회원관리"])
    def partial_update(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        instance: User = get_object_or_404(queryset=User.objects.filter(id=pk))
        serializer = UserRequestBody(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="커스텀 API",
        tags=["회원관리"],
        request=CustomSchema,
        responses={
            status.HTTP_200_OK: CustomResponse,
            status.HTTP_400_BAD_REQUEST: CustomErrorResponse,
        },
    )
    @action(detail=False, methods=["POST"], url_path="custom-api", url_name="custom-api")
    def custom_action_api(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        instance: User = get_object_or_404(queryset=User.objects.filter(id=pk))
        serializer = UserRequestBody(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # def get_serializer_class(self) -> Type[Serializer]:
    #     return self.serializer_classes.get(self.action, self.serializer_class)
    #
    # @action(detail=False, url_path="asdf/(?P<first>\w+)", url_name="asdf", methods=["GET"])
    # def asdf(self, request: Request, first, *args, **kwargs):
    #     return Response(data={"slud": first})


@extend_schema_view(
    list=extend_schema(summary="직원 목록조회", tags=["직원관리"]),
    retrieve=extend_schema(summary="직원 상세조회", tags=["직원관리"]),
    create=extend_schema(summary="직원 가입", tags=["직원관리"]),
    update=extend_schema(summary="직원 일괄 수정", tags=["직원관리"]),
    partial_update=extend_schema(summary="직원 수정", tags=["직원관리"]),
)
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSchema
    serializer_classes = {
        "list": StaffSchema,
        "retrieve": StaffDetailSchema,
        "create": StaffDetailSchema,
        "update": StaffDetailSchema,
        "partial_update": StaffDetailSchema,
    }


#
# from django.contrib.auth.hashers import PBKDF2PasswordHasher
# from django.contrib.auth.models import User
#
# user = User.objects.get(id=1)
# # 비밀변호 변경 로직
# hasher = PBKDF2PasswordHasher()
# salt = hasher.salt()
# encoded_password = PBKDF2PasswordHasher.encode(password="1234", salt=salt)
# user.password = encoded_password
# user.save()
#
#
# class User(models.Model):
#     ...
#
#     def set_password(self, raw_password):
#         hasher = PBKDF2PasswordHasher()
#         salt = hasher.salt()
#         encoded_password = PBKDF2PasswordHasher.encode(password="1234", salt=salt)
#         user.password = encoded_password
#
#
# user = User.objects.get(id=1)
# # 비밀변호 변경 로직
# user.set_password(raw_password="1234")
# user.save()


#
#
# class User(models.Model):
#     objects = UserManager()
#     ...
#
#     class Config:
#         db_table = "user"


# user_queryset: QuerySet[User] = User.objects.filter(username="abc1234")  # (1번)
#
# if user_queryset.exists():  # (2번)
#     user_queryset: QuerySet[User] = user_queryset.filter(first_name="김예제")  # (3번)
#     user_list: List[User] = list(user_queryset)  # (4번)
#     user1: User = user_queryset[0]  # (5번)


# User.objects.filter(id=1)


# settings.py


# INSTALL_APPS 위에 있음
