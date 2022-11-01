from aggregate.stores.models import Store
from aggregate.users.models import User
from rest_framework import serializers


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "groups", "user_permissions")


class StoreSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()

    class Meta:
        model = Store
        depth = 1
        fields = ("id", "name", "owner", "tel_num", "store_type", "created_at", "product_set")
