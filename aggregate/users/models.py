from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class UserStatus(models.TextChoices):
        ACTIVE = "active", "활성화"
        DORMANT = "dormant", "휴면"
        SUSPENSION = "suspension", "정지"

    class UserType(models.TextChoices):
        CUSTOMER = "customer", "고객"
        OWNER = "store_owner", "사장님"

    """
    AbstractUser를 상속받았기때문에 User에는 아래 7개 Field들이 이미 선언되어있다.

    username = models.CharField(max_length=150, unique=True,)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    date_joined = models.DateTimeField(default=timezone.now)
    """

    user_type = models.CharField(help_text="고객 유형", default=UserType.CUSTOMER, max_length=16, choices=UserType.choices)
    phone = models.CharField(max_length=64, blank=True, help_text="전화번호")
    name_kor = models.CharField(max_length=64, help_text="회원 성함(한국어)")

    class Meta:
        db_table = "user"


class HModel(models.Model):
    aa = models.CharField(max_length=64, default="qqqqq", help_text="help_text")

    class Meta:
        db_table = "h_model"
