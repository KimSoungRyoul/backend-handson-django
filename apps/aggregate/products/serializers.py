from typing import Any

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from aggregate.orders.models import Order, OrderedProduct
from aggregate.products.models import Product
from aggregate.stores.models import Store
from django.db import transaction
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    # product_type = serializers.ChoiceField(
    #     source="get_product_type_display", choices=Product.ProductType.choices,
    # )

    class Meta:
        model = Product
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"
@extend_schema_field(OpenApiTypes.STR)

class OrderedProductSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    id = serializers.IntegerField(source="product.id")
    name = serializers.CharField(source="product.name", max_length=128)
    price = serializers.IntegerField(source="product.price")
    product_type = serializers.ChoiceField(source="product.product_type", choices=Product.ProductType.choices)
    created_at = serializers.DateTimeField(source="product.created_at")
    #store = StoreSerializer(source="product.store", read_only=True)

    class Meta:
        model = OrderedProduct
        fields = ("id", "count", "name", "price", "created_at", "product_type", )


class OrderSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # status = serializers.ChoiceField(Order.Status.choices)
    total_price = serializers.IntegerField(read_only=True, help_text="주문 총액은 외부에서 수정할 수 없도록 read_only옵션을 부여합니다.")
    # address = serializers.CharField(max_length=256)
    product_set = OrderedProductSerializer(many=True, source="orderedproduct_set")

    @transaction.atomic(using="default")
    def create(self, validated_data: dict[str, Any]) -> Order:
        # print(validated_data)
        orderedproduct_data: dict[str, Any] = validated_data.pop("orderedproduct_set")

        instance: Order = Order.objects.create(**validated_data)
        orderedproduct_set: list[OrderedProduct] = [
            OrderedProduct(
                order_id=instance.id, product_id=orderedproduct["product"]["id"], count=orderedproduct["count"]
            )
            for orderedproduct in orderedproduct_data
        ]
        instance.orderedproduct_set.add(*orderedproduct_set, bulk=False)

        return instance

    class Meta:
        model = Order
        # depth = 1
        fields = ("id", "status", "total_price", "address", "product_set", "store")


def dsf():
    o = Order.objects.get(id=1)
