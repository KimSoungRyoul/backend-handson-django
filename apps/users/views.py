from typing import Any

from django.conf import settings
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from config.schema import OAS3Tag
from users.models import User


class UserSchema(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSchema
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="...", tags=[OAS3Tag.PyCon2023User])
    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary="...", tags=[OAS3Tag.PyCon2023User])
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UserSchema(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(summary="(1) 카카오 SignIn 페이지로 redirect", tags=[OAS3Tag.SocialAuth])
    @action(detail=False, methods=["GET"], url_path="kakao", url_name="kakao_signin")
    def kakao_signin(self, request):
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?"
            f"client_id={settings.KAKAO_AUTH.client_id}"
            f"&redirect_uri={settings.KAKAO_AUTH.redirect_url}"
            f"&response_type=code"
        )

    @extend_schema(summary="(1) 네이버 SignIn 페이지로 redirect", tags=[OAS3Tag.SocialAuth])
    @action(detail=False, methods=["GET"], url_path="naver", url_name="naver_signin")
    def naver_signin(self, request):
        return redirect(
            f"https://nid.naver.com/oauth2.0/authorize?"
            f"client_id={settings.NAVER_AUTH.client_id}"
            f"&redirect_uri={settings.NAVER_AUTH.redirect_url}"
            f"&response_type=code"
        )
