# Create your views here.
from aggregate.products.models import Product
from aggregate.products.serializers import ProductSerializer
from aggregate.stores.models import Store
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, mixins, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
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


class ProductViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @extend_schema(summary="API 요약 서술입니다.", tags=["상품"])
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class StoreViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()

    @extend_schema(summary="API 요약 서술입니다.", tags=["상점"])
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
