from aggregate.orders.models import Order, OrderedProduct
from aggregate.products.models import Product
from aggregate.stores.models import Store
from django.db.models import Count, F, QuerySet, Sum, Value
from django.db.models.functions import Concat
from django.test import TestCase


class QueryExpressionTest(TestCase):
    def setUp(self) -> None:
        s1 = Store.objects.create(name="김첨지 설렁탕전문점", store_type=Store.StoreType.FOOD)
        p1 = Product.objects.create(name="설렁탕", price=10_500, product_type=Product.ProductType.FOOD, store=s1)

        o1 = Order.objects.create(total_price=21_000, store=s1)
        OrderedProduct.objects.create(order=o1, product=p1, count=2)
        o2 = Order.objects.create(total_price=31_500, store=s1)
        OrderedProduct.objects.create(order=o2, product=p1, count=3)

        Store.objects.create(name="싱싱청과물", store_type=Store.StoreType.GROCERY)
        Store.objects.create(name="혈염산하 선지해장국", store_type=Store.StoreType.FOOD)

    def test_annotate(self):
        store_queryset: QuerySet = Store.objects.annotate(
            total_order_cnt=Count("order"),
            total_revenue=Sum("order__total_price"),
            store_slug=Concat(F("name"), Value(": 상점유형 ("), F("store_type"), Value(")")),
        )
        # SELECT "store"."id", "store"."name", "store"."owner_id", "store"."tel_num", "store"."created_at", "store"."store_type",
        #        COUNT("orders_order"."id") AS "total_order_cnt",
        #        SUM("orders_order"."total_price") AS "total_revenue",
        #        CONCAT("store"."name", CONCAT(: 상점유형 (, CONCAT("store"."store_type", )))) AS "store_slug"
        # FROM "store"
        # LEFT OUTER JOIN "orders_order" ON ("store"."id" = "orders_order"."store_id")
        # GROUP BY "store"."id", CONCAT("store"."name", CONCAT(: 상점유형 (, CONCAT("store"."store_type", ))))

        for store in store_queryset:
            print("\n-----------------------")
            print(f"상점 이름: {store.name}")
            print(f"Slug: {store.store_slug}")
            print(f"상점 총 주문량: {store.total_order_cnt}")
            print(f"상점 총 매출: {store.total_revenue}")

    def test_aggregate(self):
        with self.assertRaises(TypeError, msg="store_slug is not an aggregate expression"):
            Store.objects.aggregate(
                total_order_cnt=Count("order"),
                total_revenue=Sum("order__total_price"),
                store_slug=Concat(F("name"), Value(": 상점유형 ("), F("store_type"), Value(")")),  # 이름은 통계값이 아님
            )

        # print(store_aggregate)
        # {'total_order_cnt': 2, 'total_revenue': 52500}
