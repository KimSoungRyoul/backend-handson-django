from __future__ import annotations

from datetime import date, timedelta
from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from sample_app.models.store import Store


class ContractManager(models.Manager):
    def current_valid(self, store: Store):
        today = date.today()
        return self.filter(start_date__gte=today, end_date__lt=today, store=store)

    def recently_expired(self, store: Store):
        return self.filter(store=store).order_by("-end_date")

    def tomorrow_start(self):
        today = date.today()
        return self.filter(start_date=today + timedelta(days=1))

    def tomorrow_expired(self):
        today = date.today()
        return self.filter(end_date=today + timedelta(days=1))


class Contract(models.Model):
    store = models.ForeignKey(to="Store", on_delete=models.CASCADE)
    sales_commission = models.DecimalField(decimal_places=2, max_digits=5)

    start_date = models.DateField(null=True, db_comment="store active will be True ")
    end_date = models.DateField(null=True, db_comment="store active will be False")

    objects = ContractManager()

    class Meta:
        db_table = "contract"
        db_table_comment = "Store Contract"
        ordering = ["pk"]

    @property
    def store_name(self) -> str:
        return self.store.name
