from __future__ import annotations

from datetime import date
from datetime import timedelta

from django.db import models


# Create your models here.
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

    class Meta:
        db_table = "store"


class ContractManager(models.Manager):
    def current_valid(self, store: Store):
        """
            현재 유효한 계약
        """
        today = date.today()
        return self.filter(start_date__gte=today, end_date__lt=today, store=store)

    def recently_expired(self, store: Store):
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


class Contract(models.Model):
    """
        상점 계약
    """

    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)
    sales_commission = models.DecimalField(decimal_places=2, max_digits=5, help_text="판매 수수료(%)")

    start_date = models.DateField(null=True, help_text="계약 시작날짜")
    end_date = models.DateField(null=True, help_text="계약 종료날짜")

    objects = ContractManager()
