from __future__ import annotations

import boto3
from django.db import models
from django.db.models.query import EmptyQuerySet

from django_dynamodb.models import DynamoDBModel


class SimpleDynamoDBManager(models.Manager):
    # "202308121256_12344_qwefggwer3"
    def get(self, pk: str) -> OrderHistory:
        client = boto3.client("dynamodb")
        result = client.get_item(
            Key={"order_number_pk": {"S": pk}},
            TableName=self.model._meta.db_table,
        )
        try:
            return self.model(
                pk=result["Item"]["order_number_pk"]["S"],
                status=result["Item"]["status"]["S"],
            )
        except KeyError:
            raise self.model.DoesNotExist(
                "%s matching query does not exist." % self.__class__._meta.object_name
            )

    def filter(self, pk__in: list[str]) -> list[OrderHistory]:
        client = boto3.client("dynamodb")
        # result = client.batch_get_item(
        #     Keys=
        #     keys=[{"order_number_pk": {"S": pk}} for pk in pk__in],
        #     table_name=self.model._meta.db_table,
        # )
        # try:
        #     return [
        #         self.model(
        #         pk=item["order_number_pk"]["S"],
        #         status=item["status"]["S"],
        #     ) for item in result["Items"]
        #     ]
        # except KeyError:
        #     raise self.model.DoesNotExist(
        #         "%s matching query does not exist." % self.__class__._meta.object_name
        #     )







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

    simple_objects = SimpleDynamoDBManager()

    class Meta:
        db_table = "pycon2023_order_history_table"
