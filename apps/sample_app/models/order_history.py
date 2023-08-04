from __future__ import annotations

from django.db import models

from django_dynamodb.models import DynamoDBModel


class OrderHistory(DynamoDBModel):
    class Status(models.TextChoices):
        WAIT_FOR_ACCEPT = "WAIT_FOR_ACCEPT", "주문수락대기중"
        CANCEL = "CANCEL"
        COOKING = "COOKING", "조리중"
        WAIT_FOR_DELIVERY = "WAIT_FOR_DELIVERY", "조리완료(배달대기중)"
        DELIVERY = "delivery", "배달중"

    order_number_pk = models.CharField(primary_key=True, max_length=512, help_text="파티션 키")
    status = models.CharField(max_length=32, help_text="주문이력 기록당시 주문상태값", default=Status.WAIT_FOR_ACCEPT)
    address = models.CharField(max_length=512,help_text="")
    total_price = models.IntegerField(default=0)

    class Meta:
        db_table = "pycon2023_order_history_table"
