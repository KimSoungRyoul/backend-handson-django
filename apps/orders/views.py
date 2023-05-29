from typing import Final

from drf_spectacular.utils import extend_schema, extend_schema_view
from orders.models import Order
from orders.serializers import OrderSchema
from rest_framework import viewsets

ORDER_TAG: Final[str] = "주문"


@extend_schema_view(
    list=extend_schema(tags=[ORDER_TAG]),
    retrieve=extend_schema(tags=[ORDER_TAG]),
    create=extend_schema(tags=[ORDER_TAG]),
    update=extend_schema(tags=[ORDER_TAG]),
    destroy=extend_schema(tags=[ORDER_TAG]),
)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSchema
