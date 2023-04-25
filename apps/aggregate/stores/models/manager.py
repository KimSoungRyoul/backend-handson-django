from __future__ import annotations

from datetime import date, timedelta
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Exists

if TYPE_CHECKING:
    from aggregate.stores.models.store import StoreActiveSwitch, StoreText


class BaseRepository(models.QuerySet):
    @classmethod
    def as_repository(cls, model) -> BaseRepository:
        from django.db.models.manager import Manager

        manager = Manager.from_queryset(cls)()
        manager._built_with_as_manager = True
        manager.model = model
        return manager


class _StoreRepository(BaseRepository):
    def create(self, name, store_owner, address, **extra_fields):
        from aggregate.stores.models.store import StoreActiveSwitch, StoreText

        instance = self.model(name=name, address=address, **extra_fields)
        instance.save(using=self._db)

        instance.storeactiveswitch_set.bulk_create(
            objs=[
                StoreActiveSwitch(store=instance, switch_type=switch_type, is_active=False)
                for switch_type in StoreActiveSwitch.SwitchType.values
            ],
        )
        instance.storetext_set.bulk_create(
            objs=[
                StoreText(store=instance, text_type=text_type, contents="") for text_type in StoreText.TextType.values
            ],
        )
        return instance

    def only_food_store(self):
        return self.filter(store_type="food")

    def active(self) -> _StoreRepository:
        """
        현재 운영중인 상점들
        """
        from aggregate.stores.models import Contract

        today = date.today()
        return self.filter(Exists(Contract.objects.filter(start_date__gte=today, end_date__lt=today)))

    def switch_on(self, instance, switch_type: StoreActiveSwitch.SwitchType) -> int:
        cnt = instance.storeactiveswitch_set.filter(switch_type=switch_type).update(is_active=True)
        instance._prefetched_objects_cache.pop("storeactiveswitch_set", None)
        return cnt

    def switch_off(self, instance, switch_type: StoreActiveSwitch.SwitchType) -> int:
        cnt = instance.storeactiveswitch_set.filter(switch_type=switch_type).update(is_active=False)
        instance._prefetched_objects_cache.pop("storeactiveswitch_set", None)
        return cnt

    def update_text(self, instance, text_type: StoreText.TextType, contents) -> int:
        cnt = instance.storetext_set.filter(text_type=text_type).update(contents=contents)
        instance._prefetched_objects_cache.pop("storetext_set", None)
        return cnt


class StoreQuerySet(models.QuerySet["Store"]):
    def create_vendor(self, name, store_owner, *args, **kwargs):
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
