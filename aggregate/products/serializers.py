from rest_framework import serializers

from aggregate.orders.models import OrderedProduct
from aggregate.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderedProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderedProduct
        fields = ("product", "count")
