from collections import defaultdict
from typing import Type

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from aggregate.users.models import User
from aggregate.users.serializers import UserSerializer
from user_management.schemas import UserDetailSchema
from user_management.schemas import UserRequestBody
from user_management.schemas import UserSchema
from user_management.serializers import UserQueryParamSerializer

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


from rest_framework import serializers
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(summary="회원 목록조회", tags=["회원관리"]),
    retrieve=extend_schema(summary="회원 상세조회", tags=["회원관리"]),
    create=extend_schema(summary="회원 가입", tags=["회원관리"]),
    partial_update=extend_schema(summary="회원 수정", tags=["회원관리"]),
)
class UserViewSet(viewsets.ModelViewSet):
    """
        ModelViewSet을 활용한
    """

    queryset = User.objects.all()
    serializer_class = UserSchema
    serializer_classes = {
        "list": UserSchema,
        "retrieve": UserDetailSchema,
        "create": UserRequestBody,
        "update": UserRequestBody,
        "partial_update": UserRequestBody,
    }

    def get_serializer_class(self) -> Type[Serializer]:
        return self.serializer_classes.get(self.action, self.serializer_class)
