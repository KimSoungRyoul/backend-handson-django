from __future__ import annotations

from datetime import date
from datetime import timedelta
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from aggregate.stores.models.store import Store


class ContractQuerySet(models.QuerySet):
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

    objects = ContractQuerySet.as_manager()
