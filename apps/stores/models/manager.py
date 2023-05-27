from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Exists

if TYPE_CHECKING:
    from stores.models.store import Store, StoreActiveSwitch, StoreText


class StoreManager(models.Manager[Store]):
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
