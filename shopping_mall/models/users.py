from django.contrib.auth.models import AbstractUser
from django.db import models


class ShoppingMallUser(AbstractUser):
    class UserType(models.TextChoices):
        CUSTOMER = "customer", "고객"
        OWNER = "store_owner", "사장님"

    """
    AbstractUser를 상속받았기때문에 ShoppingMallUser에는 아래 7개 Field들이 이미 선언되어있다.

    username = models.CharField(max_length=150, unique=True,)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    date_joined = models.DateTimeField(default=timezone.now)
    """
    user_type = models.CharField(help_text="회원 유형", default=UserType.CUSTOMER, max_length=16, choices=UserType.choices)

    class Meta:
        db_table = "shopping_mall_user"
