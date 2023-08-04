from __future__ import annotations

import uuid
from datetime import datetime, timezone
from functools import cached_property

from django.db import models
from pynamodb.indexes import AllProjection
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, JSONAttribute, ListAttribute, UTCDateTimeAttribute, \
    MapAttribute

from sample_app.models import Order


class OrderHistoryManager(models.Manager):

    def append_snapshot(self, order: Order, comment: str) -> OrderHistory:
        order_history = OrderHistory.get(order.order_number)
        order_history.snapshots.append(OrderSnapshot(
            history_id=f"{order.order_number}={uuid.uuid4()}",
            order_number=order.order_number,
            store_id=order.store_id,
            status=order.status,
            address=order.address,
            total_price=order.total_price,
            comment=comment,
        ))

    def current_histories(self, order: Order):
        # OrderHistory.batch_get)
        # order.order_number
        ...


class Status(models.TextChoices):
    WAIT_FOR_ACCEPT = "WAIT_FOR_ACCEPT", "주문수락대기중"
    CANCEL = "CANCEL"
    COOKING = "COOKING", "조리중"
    WAIT_FOR_DELIVERY = "WAIT_FOR_DELIVERY", "조리완료(배달대기중)"
    DELIVERY = "DELIVERY", "배달중"
    COMPLETE = "COMPLETE", "완료"


def get_datetime_now():
    return datetime.now(timezone.utc)


class OrderSnapshot(MapAttribute):
    history_id = UnicodeAttribute()
    order_number = UnicodeAttribute()
    store_id = NumberAttribute()
    created_at = UTCDateTimeAttribute(default_for_new=get_datetime_now)
    status = UnicodeAttribute(default=Status.WAIT_FOR_ACCEPT.value)
    address = JSONAttribute()
    total_price = NumberAttribute(default=0)
    comment = UnicodeAttribute()


class OrderHistory(Model):
    order_number = UnicodeAttribute(hash_key=True)
    store_id = NumberAttribute()
    current_status = UnicodeAttribute(default=Status.WAIT_FOR_ACCEPT.value)
    snapshots = ListAttribute(of=OrderSnapshot)

    objects = OrderHistoryManager()

    class Meta:
        table_name = "pycon2023_order_history"
        region = "ap-northeast-2"

    @cached_property
    def order(self) -> Order:
        return Order.objects.get(order_number=self.order_number)
