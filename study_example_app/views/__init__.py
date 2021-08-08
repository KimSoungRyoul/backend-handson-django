import dataclasses
from datetime import datetime
from time import sleep

from django.contrib.auth.models import User
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from study_example_app.models import DjangoModel
from study_example_app.serializers import DjangoModelSerializer
from study_example_app.serializers import UserSerializer

#
# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     @extend_schema(
#         summary="asdfsadff",
#         examples=[
#             OpenApiExample(
#                 request_only=True,
#                 name="success_example",
#                 value={
#                     "username": "root",
#                     "password": "django_1234",
#                     "last_login": "2021-01-02T14:24:44.160Z",
#                     "is_superuser": True,
#                     "first_name": "성렬",
#                     "last_name": "김",
#                     "email": "users@example.com",
#                     "is_staff": True,
#                     "is_active": True,
#                     "date_joined": "2021-01-02T14:24:44.160Z",
#                     "groups": [0],
#                     "user_permissions": [0],
#                 },
#             ),
#         ],
#     )
#     def create(self, request: Request, *args, **kwargs) -> Response:
#         response: HttpResponse = super().create(request, *args, **kwargs)
#
#         return response


class DjangoModelViewSet(ModelViewSet):
    queryset = DjangoModel.objects.all()
    serializer_class = DjangoModelSerializer

    @extend_schema(summary='자동으로 만들어지는 API 문서 (이 API사용시에 주의해야할점 블라블라....)')
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request:Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #
    # @transaction.atomic
    # def create(self, request, *args, **kwargs):
    #     r1 = Restaurant2.objects.create(name="고급 레스토랑 In Back 스테이크 하우스", tel_num="070-1111-2222")
    #     Menu.objects.create(name="토마토 치오피노 파스타", price=20500, restaurant=r1)
    #     Menu.objects.create(name="투움바 스테이크 파스타", price=28900, restaurant=r1)
    #     Menu.objects.create(name="베이비 백 립", price=37900, restaurant=r1)
    #     Menu.objects.create(name="슈림프 감바스 셀러드", price=19900, restaurant=r1)
    #     Menu.objects.create(name="카프레제", price=19900, restaurant=r1)
    #
    #     menu_queryset = Menu.objects.all()
    #
    #     # 이 반복문 속에서 발생하는 SQL의 갯수는 몇개일까?
    #     for menu in menu_queryset:
    #         print("\n-----------------------")
    #         print(f"메뉴 이름: {menu.name}")
    #         print(f"메뉴 가격: {menu.price}")
    #         print(f"메뉴를 판매하는 음식점 이름: {menu.restaurant.name}")
    #         print("-----------------------\n")
    #
    #
    #     return Response(data={"sdf":"sdf"})

#
# @dataclasses.dataclass
# class Pet:
#     int_field: int = dataclasses.field(default=1)
#     str_field:str = dataclasses.field(default="기본값")
#     created_at: datetime = dataclasses.field(default_factory=datetime.now)
#
# print(dataclasses.asdict(Pet()))
#
#
# print(Pet())
