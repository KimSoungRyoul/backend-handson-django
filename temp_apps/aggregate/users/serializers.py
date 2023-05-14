from typing import Any, Dict

from aggregate.orders.models import Order
from aggregate.products.models import Customer2, Product, PurchaseDescriptions
from aggregate.users.models import User
from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


@transaction.atomic
def modify_order_product_set(pk: int, product_list: list[Product]):
    order = Order.objects.get(id=pk)
    order.product_set.set(objs=product_list, clear=True)
    return order
