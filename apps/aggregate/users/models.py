from __future__ import annotations

from functools import cached_property

from authentication.encryption import encryption_fields as custom_fields
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Model, QuerySet
from rest_framework import status
from rest_framework.exceptions import APIException


class DomainException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"message": "도메인 로직상 문제 발생..."}
    default_code = "invalid"


def something_check_about_welcome_coupon(phone_number: str, username: str):
    if User.objects.filter(phone=phone_number).exists():
        raise DomainException({"message": "이미 해당 전화번호로 발급받은 아이디로 쿠폰이 발급되어있습니다."})

    if user := User.objects.filter(username=username).first():
        user.has_welcome_coupon()
        user.check_already_use_welcome_coupon()


class User(AbstractUser):
    #    objects = UserManager()

    class UserStatus(models.TextChoices):
        ACTIVE = "active", "활성화"
        DORMANT = "dormant", "휴면"
        SUSPENSION = "suspension", "정지"

    class UserType(models.TextChoices):
        CUSTOMER = "customer", "고객"
        OWNER = "store_owner", "사장님"
        STAFF = "staff", "직원"

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

    user_type = models.CharField(
        help_text="고객 유형",
        default=UserType.CUSTOMER,
        max_length=16,
        choices=UserType.choices,
    )
    phone = models.CharField(max_length=64, blank=True, help_text="전화번호")
    name_kor = models.CharField(max_length=64, help_text="회원 성함(한국어)")
    registration_number = custom_fields.EncryptedField(
        max_length=custom_fields.encrypt_max_length(16),
        help_text="주민등록번호",
        blank=True,
    )
    department = models.ForeignKey(
        to="Department",
        db_comment="소속부서",
        null=True,
        on_delete=models.CASCADE,
    )

    @property
    def full_name(self) -> str:
        return self.last_name + self.first_name

    @cached_property
    def owned_store_count(self) -> int:
        return self.store_set.count()

    # def has_welcome_coupon(self) -> None:
    #     if not # (실제 쿠폰을 가지고있는지 확인하는 로직) :
    #         raise DomainExcpetion({"message": "이미 해당 계정은 쿠폰을 가지고 있습니다."})
    #
    # def check_already_use_welcome_coupon(self)-> bool:
    #     if not  # (이미 쿠폰을 사용했는지 확인하는 로직) :
    #         raise DomainExcpetion({"message": "이미 쿠폰을 사용했습니다."})

    class Meta:
        db_table = "user"


class StoreOwner(User):
    @property
    def has_multi_store(self) -> bool:
        """
        상점 여러개 소유한 사장님인가?
        """

        return True

    class Meta:
        proxy = True


class Customer(User):
    @property
    def is_init_user(self) -> bool:
        """
        아직 첫 주문을 완료하지 않은 고객인가?
        """
        return False

    class Meta:
        proxy = True


class HModel(models.Model):
    aa = models.CharField(max_length=64, default="qqqqq", help_text="help_text")

    class Meta:
        db_table = "h_model"


class Organization(models.Model):
    name = models.CharField(max_length=32, db_column="org_name")


class StaffManager(UserManager):
    def get_queryset(self) -> QuerySet[Staff]:
        return super().get_queryset().filter(user_type=User.UserType.STAFF.value)


class Staff(User):
    objects = StaffManager()

    class Meta:
        proxy = True


class Department(models.Model):
    parent1_name = models.CharField(max_length=32, db_comment="최상위 소속 부서명")
    parent2_name = models.CharField(max_length=32, db_comment="중간 소속 부서명")
    parent3_name = models.CharField(max_length=32, db_comment="상세 소속 부서명")

    def __str__(self):
        return f"{self.parent1_name}>{self.parent2_name}>{self.parent3_name}"

    class Meta:
        db_table = "department"


#
# class AModel(models.Model):
#     b_model = models.ForeignKey(to="BModel")
#
#
# class BModel(models.Model):
#     ...

# {
#     # 직원생성,수정시 이러한 포맷의 문자열을 넣으면 해당 부서가 존재하면 직원을 부서에 할당,
#     # 부서가 없으면 400 에러
#     # 조회할때도 이런 문자열 포맷 유지
#     "department": "BIZ>상점관리실>사장님관리팀",
#     ...
# }
#
# {
#     # 이런 식을 비워서 요청하면 부서를 제거
#     "department": ""
#     ...
# }


class Human(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    class Meta:
        abstract = True
        # abstract=True 인 경우 db_table을 지정할 수 없습니다.


class Man(Human):
    class Meta:
        db_table = "man"


class Woman(Human):
    class Meta:
        db_table = "woman"
