from django.db import transaction
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from aggregate.products.models import Product
from aggregate.stores.models import Store
# Create your views here.


class StoreViewSet(viewsets.ModelViewSet):

    def create(self, request: Request, *args, **kwargs) -> Response:

        with transaction.atomic():
            s1 = Store.objects.create(name="김첨지 설렁탕전문점", store_type=Store.StoreType.FOOD)

            raise ValueError("일부로 발생시키는 에러")

            p1 = Product.objects.create(name="설렁탕", price=10_500, product_type=Product.ProductType.FOOD, store=s1)

        return Response(data={"detail": "생성완료"})
