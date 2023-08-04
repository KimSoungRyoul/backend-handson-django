from __future__ import annotations

from django.db import models
from django.db.models import Manager

from .manager import DynamoDBManager


class DynamoDBModel(models.Model):
    class Meta:
        abstract = True
        base_manager_name = "objects"

    objects: Manager[DynamoDBModel] = DynamoDBManager()
