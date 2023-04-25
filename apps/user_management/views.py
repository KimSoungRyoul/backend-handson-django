from typing import Any, List, Type

from aggregate.products.models import Customer2, PurchaseDescriptions
from aggregate.stores.models import Store
from aggregate.users.models import Staff, User
from aggregate.users.serializers import UserSerializer
from django.db import models
from django.db.models import Prefetch, QuerySet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
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


from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets


# @extend_schema_view(
#     list=extend_schema(summary="회원 목록조회", tags=["회원관리"]),
#     retrieve=extend_schema(summary="회원 상세조회", tags=["회원관리"]),
#     create=extend_schema(summary="회원 가입", tags=["회원관리"]),
#     update=extend_schema(summary="회원 일괄 수정", tags=["회원관리"]),
#     partial_update=extend_schema(summary="회원 수정", tags=["회원관리"]),
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

    @extend_schema(
        summary="회원 상세조회",
        tags=["회원관리"],
        responses={
            status.HTTP_200_OK: UserDetailSchema,
        },
    )
    def retrieve(
        self,
        request: Request,
        pk: str,
    ) -> Response:
        instance: User = User.objects.get(pk=pk)
        serializer = UserDetailSchema(instance)
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
