from orders.models import Order
from rest_framework import serializers


class OrderSchema(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
