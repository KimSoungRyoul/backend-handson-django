from typing import Any, Dict, Optional

from aggregate.users.models import DomainException, User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from drf_example_app.models import University
from drf_example_app.schemas import UNIVERSITY_SCHEMA_PARAMETERS
from drf_example_app.serializers import UniversitySchema

# Create your views here.
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySchema
    pagination_class = PageNumberPagination

    @extend_schema(
        tags=["대학교"],
        summary="리스트 조회 요약 description....",
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    @extend_schema(tags=["대학교"], summary="생성 요약 description....")
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(tags=["대학교"], summary="수정 요약 description ....")
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# exception_handler


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "따로 에러 메시지를 상세서술하지 않으면 사용될 안내문구 작성"


@extend_schema(summary="임시 API", request=None, tags=["example"])
@api_view(["GET"])
def example_api(request: Request, *args, **kwargs):
    raise CustomException({"message": "에러문구 직접작성"})


# def something_check_about_welcome_coupon(phone_number: str, username: str):
#     if User.objects.filter(phone=phone_number).exists():
#         return Response(
#             status=status.HTTP_400_BAD_REQUEST,
#             data={"message": "이미 해당 전화번호로 발급받은 아이디로 쿠폰이 발급되어있습니다."}
#         )
#
#     if user := User.objects.filter(username=username).first():
#         if user.has_welcome_coupon():
#             return Response(
#                 status=status.HTTP_400_BAD_REQUEST,
#                 data={"message": "이미 해당 계정은 쿠폰을 가지고 있습니다."}
#             )
#         if user.check_already_use_welcome_coupon():
#             return Response(
#                 status=status.HTTP_400_BAD_REQUEST,
#                 data={"message": "이미 쿠폰을 사용했습니다."}
#             )
#     return Response(
#         status=status.HTTP_200_OK,
#         data={"message": "별다른 문제가 없습니다."}
#     )


#
# @extend_schema(summary="임시 API2", request=None, tags=["example"])
# @api_view(["GET"])
# def signup_api(request: Request, *args, **kwargs):
#     phone_number = request.data["phone_number"]
#     username = request.data["username"]
#
#     something_check_about_welcome_coupon(phone_number, username)
#
#     return Response(
#         status=status.HTTP_200_OK,
#         data={"message": "별다른 문제가 없습니다."}
#     )
#


@extend_schema(summary="세션 기반 로그인 API", request=None)
@api_view(["POST"])
# @permission_classes(permission_classes=[ISAuthenticated])
def login_example_api(request: Request, *args, **kwargs):
    login_dto: Dict[str, str] = request.data

    if not login_dto.get("username"):
        # raise ValidationError()
        # raise APIException(code=)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "회원 계정을 입력해주세요."})
    if not login_dto.get("password"):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"message": "비밀번호를 입력해주세요."},
        )

    login_user: Optional[User] = authenticate(
        request=request,
        username=login_dto["username"],
        password=login_dto["password"],
    )
    if login_user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    login(request=request, user=login_user)

    return Response(
        status=status.HTTP_200_OK,
        data={"message": "로그인 되었습니다."},
    )
