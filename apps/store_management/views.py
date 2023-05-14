# Create your views here.
from typing import Any, Type

from aggregate.products.models import Product
from aggregate.products.serializers import ProductCreateSchema, ProductSchema
from aggregate.stores.models import Store
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from study_example_app.serializers.store_serializers import StoreSerializer


class StoreTestSchema(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


@api_view(http_method_names=["PATCH"])
def drf_fbv(request):
    return Response()


@extend_schema_view(
    get=extend_schema(tags=["스토어 호호"], summary="Get appointment notes"),
)
class AGenericView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreTestSchema


class ProductViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    serializer_class = ProductSchema
    queryset = Product.objects.all()

    serializer_classes = {
        "retrieve": ProductSchema,
        "create": ProductCreateSchema,
    }

    # def get_serializer_class(self) -> Type[Serializer]:
    #     return self.serializer_classes.get(self.action, self.serializer_class)

    @extend_schema(summary="API 요약 서술입니다.", tags=["상품"])
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer: ProductSchema = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(summary="API 요약 서술입니다.", tags=["상품"])
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: ProductCreateSchema = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StoreViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()

    @extend_schema(summary="API 요약 서술입니다.", tags=["상점"])
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
