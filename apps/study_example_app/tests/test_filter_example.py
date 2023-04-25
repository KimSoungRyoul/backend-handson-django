from aggregate.orders.models import Order, OrderedProduct
from aggregate.products.models import Product
from aggregate.stores.models import Store
from django.db.models import Q
from django.test import TestCase


class QuerySetFilterTest(TestCase):
    def setUp(self) -> None:
        s1 = Store.objects.create(name="김첨지 설렁탕전문점", store_type=Store.StoreType.FOOD)
        p1 = Product.objects.create(name="설렁탕", price=10_500, product_type=Product.ProductType.FOOD, store=s1)

        o1 = Order.objects.create(total_price=21_000, store=s1)
        OrderedProduct.objects.create(order=o1, product=p1, count=2)
        o2 = Order.objects.create(total_price=31_500, store=s1)
        OrderedProduct.objects.create(order=o2, product=p1, count=3)

        Store.objects.create(name="싱싱청과물", store_type=Store.StoreType.GROCERY)
        Store.objects.create(name="혈염산하 선지해장국", store_type=Store.StoreType.FOOD)

    def test_filter_normal(self):
        store_queryset = Store.objects.filter(name="김첨지 설렁탕전문점")
        print(store_queryset.query)
        # SELECT "store"."id", "store"."name",... FROM "store" WHERE "store"."name" = 김첨지 설렁탕전문점

        store_queryset = Store.objects.filter(name__contains="설렁탕")
        print(store_queryset.query)
        # SELECT "store"."id", "store"."name", ... FROM "store" WHERE "store"."name"::text LIKE %설렁탕%

        store_queryset = Store.objects.filter(name__startswith="김첨지")
        print(store_queryset.query)
        # SELECT "store"."id", "store"."name", ... FROM "store" WHERE "store"."name"::text LIKE 김첨지%

        store_queryset = Store.objects.filter(name__endswith="전문점")
        print(store_queryset.query)
        # SELECT "store"."id", "store"."name", ... FROM "store" WHERE "store"."name"::text LIKE %전문점

        store_queryset = Store.objects.filter(owner__isnull=True)
        print(store_queryset.query)
        # SELECT "store"."id", "store"."name", ... FROM "store" WHERE "store"."owner_id" IS NULL

        product_queryset = Product.objects.filter(product_type__in=["food", "grocery"])
        print(product_queryset.query)
        # SELECT "product"."id", "product"."name", "... FROM "product" WHERE "product"."product_type" IN (food, grocery) ORDER BY "product"."created_at" DESC

        order_queryset = Order.objects.filter(total_price__gt=20_000)
        print(order_queryset.query)
        # SELECT "orders_order"."id", "orders_order"."status", ... FROM "orders_order" WHERE "orders_order"."total_price" > 20000

        order_queryset = Order.objects.filter(total_price__lte=30_000)
        print(order_queryset.query)
        # SELECT "orders_order"."id", "orders_order"."status", ...FROM "orders_order" WHERE "orders_order"."total_price" <= 30000

        order_queryset = Order.objects.filter(total_price__range=(20_000, 30_000))
        print(order_queryset.query)
        # SELECT "orders_order"."id", "orders_order"."status", ... FROM "orders_order" WHERE "orders_order"."total_price" BETWEEN 20000 AND 30000

    def test_filter_foreignkey(self):
        order_queryset = Order.objects.filter(orderedproduct__count=2, orderedproduct__product__name="설렁탕")
        print(order_queryset.query)
        # SELECT "orders_order"."id", "orders_order"."status", ... FROM "orders_order"
        #       INNER JOIN "ordered_product" ON ("orders_order"."id" = "ordered_product"."order_id")
        #       INNER JOIN "product" ON ("ordered_product"."product_id" = "product"."id")
        # WHERE ("ordered_product"."count" = 2 AND "product"."name" = 설렁탕)
        product_queryset = Product.objects.filter(store__name__contains="설렁탕")
        print(product_queryset.query)
        # SELECT "product"."id", "product"."name", "... FROM "product"
        #       INNER JOIN "store" ON ("product"."store_id" = "store"."id")
        # WHERE "store"."name"::text LIKE %설렁탕%

        product_queryset = Product.objects.filter(Q(store__name="김첨지 설렁탕전문점") | Q(store__name="싱싱청과물"))
        print(product_queryset.query)
        # SELECT "product"."id", "product"."name", ... FROM "product"
        #       INNER JOIN "store" ON ("product"."store_id" = "store"."id")
        # WHERE ("store"."name" = 김첨지 설렁탕전문점 OR "store"."name" = 싱싱청과물)

        product_queryset = Product.objects.exclude(store__name="김첨지 설렁탕전문점")
        product_queryset = Product.objects.filter(~Q(store__name="김첨지 설렁탕전문점"))
        print(product_queryset.query)
        # SELECT "product"."id", "product"."name",... FROM "product"
        #       INNER JOIN "store" ON ("product"."store_id" = "store"."id")
        # WHERE NOT ("store"."name" = 김첨지 설렁탕전문점)
