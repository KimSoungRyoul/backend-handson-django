from datetime import time

from django.core import validators
from django.db import models


def set_deleted_owner():
    return -1

class Store(models.Model):
    class StoreType(models.TextChoices):
        FOOD = "food", "배달음식"
        GROCERY = "grocery", "식료품/가공식품"
        PET_FOOD = "pet_food", "반려동물음식"

    name = models.CharField(max_length=128, help_text="음식점 가게명",default="ff222f")
    name2222 = models.CharField(max_length=128, help_text="음식점 가게명", default="fff")
    owner = models.ForeignKey(
        to="ShoppingMallUser", null=False, on_delete=models.CASCADE, unique=True,
    )
    tel_num = models.CharField(max_length=16,default="070-000-0000", help_text="음식점 연락처")

    store_info = models.OneToOneField(to="StoreInfo", null=True, on_delete=models.SET(set_deleted_owner))

    class Meta:
        db_table = "store"


class StoreInfo(models.Model):

    open_time = models.TimeField(default=time(hour=0, minute=0), help_text="가게 개장시간")
    close_time = models.TimeField(default=time(hour=0, minute=0), help_text="가게 마감시간")
    is_always_open = models.BooleanField(default=False, help_text="24시간 운영여부")

    food_nutrition_facts = models.JSONField(help_text="식재료별 영양정보 ex: {'식재료이름':'영양성분'}", default={"식재료이름": "영양성분"})
    company_number = models.CharField(
        help_text="사업자 번호",
        max_length=16,
        blank=True,
        validators=[
            validators.RegexValidator(
                regex=r"^([0-9]{3})-?([0-9]{2})-?([0-9]{5})$", message="잘못된 사업자 번호 형식입니다. xxx-xx-xxxxx 형식을 지켜주세요."
            )
        ],
    )

    class Meta:
        db_table = "store_info"


