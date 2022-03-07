from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from aggregate.stores.models import Store
from rest_framework import serializers
from rest_framework import mixins


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
