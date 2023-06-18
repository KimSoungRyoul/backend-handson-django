from __future__ import annotations

from django.db import models
from django.db.models import QuerySet
from django.db.models.functions import Lower


class StoreManager(models.Manager["Store"]):
    def create_store(self, name, owner, store_type, tel_num="", description=""):
        instance: Store = super().create(
            name=name,
            owner=owner,
            tel_num=tel_num,
            store_type=store_type,
            description=description,
            active=False,
        )

        return instance

    def only_food_store(self) -> QuerySet["Store"]:
        return self.filter(store_type="food")


class Store(models.Model):
    class StoreType(models.TextChoices):
        FOOD = "food", "FoodDelivery"
        GROCERY = "grocery", "MorningGroceryDelivery"
        PET_EQUIPMENT = "pet_equipment", "PetEquipmentDelivery"

    active = models.BooleanField(
        default=False,
        db_comment="this field should be controlled by changes in the Contract start_date and end_date",
    )

    name = models.CharField(max_length=128)
    owner = models.ForeignKey(to="auth.User", on_delete=models.CASCADE, null=True)
    tel_num = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    store_type = models.CharField(choices=StoreType.choices, max_length=32)
    description = models.TextField(blank=True, default="")

    objects = StoreManager()

    class Meta:
        db_table = "store"
        ordering = ("pk",)
        indexes = [
            models.Index(fields=("name",), name="store_name_idx"),
            models.Index(fields=("created_at", "store_type"), name="cr_at_type_composite_idx"),
        ]
