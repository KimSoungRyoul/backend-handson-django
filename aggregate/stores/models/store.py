from __future__ import annotations

from django.db import models

from aggregate.stores.models.repository import _StoreRepository
from aggregate.stores.models.repository import StoreQuerySet


class Store(models.Model):
    class StoreType(models.TextChoices):
        FOOD = "food", "배달음식"
        GROCERY = "grocery", "식료품/가공식품"
        PET_FOOD = "pet_food", "반려동물음식"

    name = models.CharField(max_length=128, help_text="음식점 가게명")
    owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, null=True)
    tel_num = models.CharField(max_length=16, help_text="음식점 연락처")
    created_at = models.DateTimeField(auto_now_add=True)
    store_type = models.CharField(choices=StoreType.choices, help_text="상점 유형", max_length=32)

    address = models.OneToOneField("StoreAddress", on_delete=models.CASCADE)

    objects = StoreQuerySet.as_manager()

    class Meta:
        db_table = "store"

    @property
    def is_open(self):
        return next(
            store_switch.is_active
            for store_switch in self.storeactiveswitch_set.all()
            if store_switch.switch_type == StoreActiveSwitch.SwitchType.OPEN
        )

    def text(self, text_type: StoreText.TextType):
        return next(store_text for store_text in self.storetext_set.all() if store_text.text_type == text_type)


class StoreAddress(models.Model):
    si = models.CharField(max_length=128, help_text="시")
    gu = models.CharField(max_length=128, help_text="구")
    gun = models.CharField(max_length=128, help_text="군")
    dongmyun = models.CharField(max_length=128, help_text="동,면,읍")

    lat = models.FloatField(help_text="위도")
    lng = models.FloatField(help_text="경도")

    detail = models.CharField(max_length=128, help_text="상세 주소")


class StoreActiveSwitch(models.Model):
    class SwitchType(models.TextChoices):
        OPEN = "is_open", "현재 영업 여부"
        AD = "has_ad_mark", "현재 광고상품 사용여부"

    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)
    switch_type = models.CharField(choices=SwitchType.choices, max_length=32)
    is_active = models.BooleanField(default=False)


class StoreText(models.Model):
    class TextType(models.TextChoices):
        LEGAL = "legal_notice", "법적 고시"
        ORIGIN = "origin", "원산지 정보"

    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)
    text_type = models.CharField(choices=TextType.choices, max_length=32)
    contents = models.TextField(help_text="대용량 텍스트")


StoreRepository = _StoreRepository.as_repository(Store)
