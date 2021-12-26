from rest_framework import serializers

from aggregate.stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("id", "name", "owner", "tel_num", "store_type", "created_at")
