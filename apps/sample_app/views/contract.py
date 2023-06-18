from typing import Any, Final

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from sample_app.models import Contract, Store
from sample_app.serializers import (
    ContractCreateSchema,
    ContractDetailSchema,
    ContractSchema,
    ContractUpdateSchema,
)

CONTRACT_TAG: Final[str] = "SampleApp"


class ContractViewSet(viewsets.GenericViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSchema
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class_list = {
        "list": ContractSchema,
        "retrieve": ContractDetailSchema,
        "create": ContractCreateSchema,
        "update": ContractUpdateSchema,
    }

    def get_serializer_class(self):
        return self.serializer_class_list[self.action]

    @extend_schema(tags=[CONTRACT_TAG], summary="Show Contract List")
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        paging_queryset = self.paginate_queryset(queryset)
        serializer: ContractSchema = self.get_serializer(paging_queryset, many=True)
        return Response(serializer.data)

    @extend_schema(tags=[CONTRACT_TAG])
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance: Contract = self.get_object()
        serializer: ContractDetailSchema = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(tags=[CONTRACT_TAG])
    def create(self, request: Request, store_pk: str, *args: Any, **kwargs: Any) -> Response:
        serializer: ContractCreateSchema = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=[CONTRACT_TAG])
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance: Contract = self.get_object()
        serializer: ContractUpdateSchema = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
