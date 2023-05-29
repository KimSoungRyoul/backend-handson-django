from __future__ import annotations

from datetime import date, timedelta

from django.db import models


class StoreManager(models.Manager["Store"]):
    def create_store(self, name, store_owner, *args, **kwargs):
        instance = super().create(name, store_owner, *args, **kwargs)

        # ... 애그리거트 객체들 추가 선언

        return instance

    def only_food_store(self):
        return self.filter(store_type="food")

    def current_valid(self, store=None):
        """
        현재 유효한 계약
        """
        today = date.today()
        return self.filter(start_date__gte=today, end_date__lt=today, store=store)

    def recently_expired(self, store):
        """
        가장 최근에 만료된 계약 순서대로
        """
        return self.filter(store=store).order_by("-end_date")

    def tomorrow_start(self):
        """
        내일부터 시작되는 계약
        """
        today = date.today()
        return self.filter(start_date=today + timedelta(days=1))

    def tomorrow_expired(self):
        """
        내일이 계약 만료일이 도래하는
        """
        today = date.today()
        return self.filter(end_date=today + timedelta(days=1))


class Store(models.Model):
    class StoreType(models.TextChoices):
        FOOD = "food", "배달음식"
        GROCERY = "grocery", "식료품/가공식품"
        PET_FOOD = "pet_food", "반려동물음식"

    name = models.CharField(max_length=128, db_comment="음식점 가게명")
    owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, null=True)
    tel_num = models.CharField(max_length=16, db_comment="음식점 연락처")
    created_at = models.DateTimeField(auto_now_add=True)
    store_type = models.CharField(choices=StoreType.choices, db_comment="상점 유형", max_length=32)

    address = models.OneToOneField("StoreAddress", on_delete=models.CASCADE, null=True)
    store_name_display_only = models.CharField(max_length=128, db_comment="직원이 해당 상점을 한눈에 볼수있게 관리하는 필드입니다.")
    description = models.TextField(db_comment="상점 소개 문구")

    objects = StoreManager()

    class Meta:
        db_table = "store"
        db_table_comment = "상점"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

    @property
    def is_open(self):
        return next(
            store_switch.is_active
            for store_switch in self.storeactiveswitch_set.all()
            if store_switch.switch_type == StoreActiveSwitch.SwitchType.OPEN
        )


class StoreAddress(models.Model):
    si = models.CharField(max_length=128, db_comment="시")
    gu = models.CharField(max_length=128, db_comment="구")
    gun = models.CharField(max_length=128, db_comment="군")
    dongmyun = models.CharField(max_length=128, db_comment="동,면,읍")

    lat = models.FloatField(db_comment="위도")
    lng = models.FloatField(db_comment="경도")

    detail = models.CharField(max_length=128, db_comment="상세 주소")


class StoreActiveSwitch(models.Model):
    class SwitchType(models.TextChoices):
        OPEN = "is_open", "현재 영업 여부"
        AD = "has_ad_mark", "현재 광고상품 사용여부"

    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)
    switch_type = models.CharField(choices=SwitchType.choices, max_length=32)
    is_active = models.BooleanField(default=False)
