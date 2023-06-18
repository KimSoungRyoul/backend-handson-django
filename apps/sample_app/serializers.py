from rest_framework import serializers
from sample_app.models import Contract, Store


class ContractSchema(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ("store_name", "start_date", "end_date")


class ContractDetailSchema(ContractSchema):
    class Meta(ContractSchema.Meta):
        model = Contract
        fields = "__all__"
        depth = 1


class ContractCreateSchema(ContractSchema):
    def create(self, validated_data):
        return Contract.objects.create(**validated_data)

    class Meta(ContractSchema.Meta):
        model = Contract
        fields = ("sales_commission", "start_date", "end_date", "store")


class ContractUpdateSchema(ContractSchema):
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta(ContractSchema.Meta):
        model = Contract
        fields = "__all__"


class StoreSchema(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"
        depth = 1
