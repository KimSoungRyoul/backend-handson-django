# 2022/04/{category}/20220401_uuid_filename.mp4
import os
import uuid
from functools import cached_property

from django.contrib.auth.models import AbstractUser as DjangoAbstrctAuthUser
from django.db import models
from django_mysql import models as mysql_models

from users.models.managers.user_manager import CustomUserManager


class BaseModel(mysql_models.Model):
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


def upload_filepath(instance: models.Model, filename: str):
    # ex: filename = "./i_am_file.txt""
    file_basename: str = os.path.basename(filename)
    # ex: file_basename = "i_am_file.txt"
    return f"{instance._meta.db_table}/{instance.username}/{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=file_basename)}_{file_basename}"


class User(BaseModel, DjangoAbstrctAuthUser):
    name = models.CharField(max_length=128, default="")
    nickname = models.CharField(max_length=128, default="")
    phone = models.CharField(max_length=64, null=True)
    birthday = models.DateField(null=True)
    profile_image = models.ImageField(upload_to=upload_filepath, null=True)

    objects = CustomUserManager()

    class Meta:
        db_table = "user"
        constraints = [models.UniqueConstraint(fields=["phone"], name="unique_phone")]

    @cached_property
    def kakao_socialinfo(self):
        return self.socialinfo_set.filter(provider=SocialInfo.AuthProvider.KAKAO).first()

    @cached_property
    def naver_socialinfo(self):
        return self.socialinfo_set.filter(provider=SocialInfo.AuthProvider.NAVER).first()



class SocialInfo(BaseModel):
    class AuthProvider(models.TextChoices):
        PYCON2023APP = "pycon2023_app", "파이콘2023인증서버"
        KAKAO = "kakao", "카카오"
        NAVER = "naver", "네이버"

    provider = models.CharField(choices=AuthProvider.choices, max_length=64, default=AuthProvider.PYCON2023APP)
    social_uuid = models.CharField(null=False, max_length=128, help_text="카카오 네이버측 고유번호")
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)

    auth_info = models.JSONField(
        default=dict,
        help_text="""auth_info 포맷 예시(소셜인증으로 얻은 토큰정보)
        {
            "access_token": "jV1w97fQUeRloxy12gWjYoCmEWy9dx3c7QodIQopb7kAAAGAomXG0Q",
            "token_type": "bearer",
            "refresh_token": "z1I_MM1lwOk-uKBXbLHgH02MD0derxRPCkkfHwopb7kAAAGAomXG0A",
            "expires_in": 21599,
            "scope": "birthday account_email profile_image profile_nickname",
            "refresh_token_expires_in": 5183999
        }
        """,
    )
