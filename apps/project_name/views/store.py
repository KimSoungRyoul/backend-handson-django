from typing import Any, Final

from drf_spectacular.utils import extend_schema, extend_schema_view
from project_name.models import Contract, Store
from project_name.serializers import (
    ContractCreateSchema,
    ContractDetailSchema,
    ContractSchema,
    ContractUpdateSchema,
    StoreSchema,
)
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

STORE_TAG: Final[str] = "SampleApp"


@extend_schema_view(
    list=extend_schema(tags=[STORE_TAG], summary="Show Store List"),
    retrieve=extend_schema(tags=[STORE_TAG]),
    create=extend_schema(tags=[STORE_TAG]),
    destroy=extend_schema(tags=[STORE_TAG]),
)
class StoreViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Store.objects.all()
    serializer_class = StoreSchema
    permission_classes = [
        permissions.IsAuthenticated,
    ]
