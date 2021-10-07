from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager
from django.db import models
from django_extensions.db.models import TimeStampedModel

from study_example_app.models import fields as custom_fields
from study_example_app.models.fields import encrypt_max_length
# Create your models here.


class UserManager(_UserManager):
    def inactive(self):
        return self.filter(is_active=False)

    def active(self):
        return self.filter(is_active=False)


class User(AbstractUser):


    objects = UserManager()


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
    registration_number = custom_fields.EncryptedField(
        max_length=encrypt_max_length(16), help_text="주민등록번호", blank=True,
    )


    class Meta:
        db_table = "user"

User.objects.filter(is_active=False)

User.objects.inactive()


class HModel(models.Model):
    aa = models.CharField(max_length=64, default="qqqqq", help_text="help_text")

    class Meta:
        db_table = "h_model"
