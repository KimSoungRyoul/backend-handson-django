from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=128, db_comment="상점 이름")

    class Meta:
        db_table = "store"
