from typing import Final

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from stores.models import Contract, Store
from stores.serializers import ContractSchema, StoreSchema

STORE_TAG: Final[str] = "상점"


@extend_schema_view(
    list=extend_schema(tags=[STORE_TAG], summary="상점 목록 조회"),
    retrieve=extend_schema(tags=[STORE_TAG]),
    create=extend_schema(tags=[STORE_TAG]),
    update=extend_schema(tags=[STORE_TAG]),
    destroy=extend_schema(tags=[STORE_TAG]),
)
class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSchema


CONTRACT_TAG: Final[str] = "상점 계약"


@extend_schema_view(
    list=extend_schema(tags=[CONTRACT_TAG], summary="계약 목록 조회"),
    retrieve=extend_schema(tags=[CONTRACT_TAG]),
    create=extend_schema(tags=[CONTRACT_TAG]),
    update=extend_schema(tags=[CONTRACT_TAG]),
    destroy=extend_schema(tags=[CONTRACT_TAG]),
)
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSchema
