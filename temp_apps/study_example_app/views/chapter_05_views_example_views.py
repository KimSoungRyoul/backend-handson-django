from aggregate.stores.models import Store
from django.db.models import QuerySet
from rest_framework import exceptions, generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from study_example_app.serializers.store_serializers import StoreSerializer


class StoreGenericViews(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def retrieve(self, request: Request, pk, *args, **kwargs):
        store_queryset: QuerySet = self.get_queryset()
        try:
            store: Store = store_queryset.filter(id=pk)
        except Store.DoesNotExist:
            raise exceptions.NotFound(detail=f"상점 {pk}는 존재하지 않습니다.")
        serializer: StoreSerializer = self.get_serializer(instance=store)
        return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
