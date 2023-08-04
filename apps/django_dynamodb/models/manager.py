from __future__ import annotations

from django.db.models.manager import BaseManager

from .queryset import DynamoDBQuerySet


class DynamoDBManager(BaseManager.from_queryset(DynamoDBQuerySet)):
    ...
    # def __init__(self):
    #     super().__init__()
    #     self._db = "dynamodb"

