import uuid

import httpx
from django.conf import settings
from django.core.files.base import ContentFile

from django.db import transaction
from django.db.models import Q
from django.db.models.query import EmptyQuerySet
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from config.schema import OAS3Tag
from custom_oauth2.external_apis import (
    KakaoHttpx,
    NaverHttpx,
    SocialUserInfo,
)
from custom_oauth2.models import (
    JWTAccessToken,
    RedisRefreshToken,
    RegisteredApplication,
)
from custom_oauth2.serializers.token_schema import (
    EmptySerializer,
    TokenSchema,
)
from custom_oauth2.utils import JWTUtils
from users.models.users import SocialInfo, User


class SocialAuthCallBackViewSet(viewsets.GenericViewSet):
    queryset = EmptyQuerySet
    serializer_class = EmptySerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(summary="(2) 카카오 콜백 API", responses={status.HTTP_200_OK: TokenSchema}, tags=[OAS3Tag.SocialAuth])
    @action(detail=False, methods=["GET"], url_path="kakao", url_name="kakao_callback")
    @transaction.atomic
    def kakao_callback(self, request: Request):
        code = request.query_params["code"]
        kakao_response = httpx.get(
            url=f"https://kauth.kakao.com/oauth/token",
            headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
            params={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_AUTH.client_id,
                "redirect_uri": settings.KAKAO_AUTH.redirect_url,
                "code": code,
            },
        )
        token_json = kakao_response.json()
        error = token_json.get("error", None)

        if error is not None:
            return Response(
                data={"detail": "INVALID_CODE"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = token_json.get("access_token")

        kakao_uuid: int = KakaoHttpx.retrieve_uuid(access_token=access_token)

        user: User = User.objects.filter(
            socialinfo__social_uuid=kakao_uuid, socialinfo__provider=SocialInfo.AuthProvider.KAKAO
        ).first()

        if user is None:
            userinfo: SocialUserInfo = KakaoHttpx.retrieve_social_info(
                access_token=access_token,
            )
            response = httpx.get(userinfo.profile_image_url)
            user: User = User.objects.create_user(
                username=userinfo.email,
                password=access_token,
                email=userinfo.email,
                name=userinfo.nickname,
                profile_image=ContentFile(content=response.content, name=f"{userinfo.name}_profile_img.{userinfo.profile_image_url.split('.')[-1]}"),
            )
            SocialInfo.objects.create(
                user=user,
                social_uuid=userinfo.social_uuid,
                provider=SocialInfo.AuthProvider.KAKAO,
                auth_info=token_json,
            )
        else:
            user.kakao_socialinfo.auth_info = token_json
            user.kakao_socialinfo.save()
            now = timezone.now()
            User.objects.filter(id=user.id).update(date_joined=now)
            user.date_joined = now

        access_token: str = JWTUtils.generate_token(user=user)
        refresh_token = RedisRefreshToken.objects.create(
            user=user,
            access_token=JWTAccessToken.parse(access_token),
            token=str(uuid.uuid4()),
            application=RegisteredApplication.objects.get(name="pycon-auth-server"),
        )

        return Response(
            data=TokenSchema(
                {
                    "access_token": access_token,
                    "expires_in": settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"],
                    "refresh_token": refresh_token.token,
                    "token_type": "Bearer",
                    "scope": "read write",
                    #  "user": user,
                }
            ).data
        )

    @extend_schema(summary="(2) 네이버 콜백 API", tags=[OAS3Tag.SocialAuth])
    @action(detail=False, methods=["GET"], url_path="naver", url_name="naver_callback")
    @transaction.atomic
    def naver_callback(self, request: Request):

        code = request.query_params["code"]
        naver_response = httpx.get(
            url="https://nid.naver.com/oauth2.0/token",
            params={
                "grant_type": "authorization_code",
                "client_id": settings.NAVER_AUTH.client_id,
                "client_secret": settings.NAVER_AUTH.secret,
                "redirect_uri": settings.NAVER_AUTH.redirect_url,
                "code": code,
            },
        )
        token_json = naver_response.json()
        # print(f"네이버:{token_json}")
        error = token_json.get("error", None)

        if error is not None:
            return Response(
                data={"detail": "INVALID_CODE"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token: str = token_json.get("access_token")
        userinfo: SocialUserInfo = NaverHttpx.retrieve_social_info(access_token=access_token)
        naver_uuid: str = userinfo.social_uuid
        if (
            user := User.objects.filter(
                Q(socialinfo__social_uuid=naver_uuid, socialinfo__provider=SocialInfo.AuthProvider.NAVER)
                | Q(username=userinfo.email)
            ).first()
        ) is None:

            user: User = User.objects.create_user(
                username=userinfo.email,
                password=access_token,
                email=userinfo.email,
                name=userinfo.nickname,
            )
            SocialInfo.objects.create(
                user=user,
                social_uuid=userinfo.social_uuid,
                provider=SocialInfo.AuthProvider.NAVER,
                auth_info=token_json,
            )
        else:
            user.naver_socialinfo: SocialInfo = SocialInfo.objects.create(
                user=user,
                social_uuid=userinfo.social_uuid,
                provider=SocialInfo.AuthProvider.NAVER,
                auth_info=token_json,
            )

            user.naver_socialinfo.auth_info = token_json
            user.naver_socialinfo.save()
            now = timezone.now()
            User.objects.filter(id=user.id).update(date_joined=now)
            user.date_joined = now

        access_token: str = JWTUtils.generate_token(user=user)

        refresh_token = RedisRefreshToken.objects.create(
            user=user,
            access_token=JWTAccessToken.parse(token=access_token),
            token=str(uuid.uuid4()),
            application=RegisteredApplication.objects.get(name="pycon-auth-server"),
        )

        return Response(
            data=TokenSchema(
                {
                    "access_token": access_token,
                    "expires_in": settings.OAUTH2_PROVIDER["ACCESS_TOKEN_EXPIRE_SECONDS"],
                    "refresh_token": refresh_token.token,
                    "token_type": "Bearer",
                    "scope": "read write",
                    #  "user": user,
                }
            ).data
        )
