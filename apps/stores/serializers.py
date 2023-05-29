from rest_framework import serializers
from stores.models import Contract, Store


class StoreSchema(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class ContractSchema(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"
