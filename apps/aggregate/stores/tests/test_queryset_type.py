from unittest import skip

from aggregate.orders.models import Order, OrderedProduct
from aggregate.products.models import Product
from aggregate.stores.models import Store
from aggregate.users.models import User
from django.db.models import Exists, Subquery
from django.test import TestCase
from django_mysql.models import QuerySet


class QuerySetTest(TestCase):
    def setUp(self) -> None:
        s1 = Store.objects.create(name="김첨지 설렁탕전문점", store_type=Store.StoreType.FOOD)
        p1 = Product.objects.create(name="설렁탕", price=10_500, product_type=Product.ProductType.FOOD, store=s1)

        o1 = Order.objects.create(total_price=21_000, store=s1)
        OrderedProduct.objects.create(order=o1, product=p1, count=2)
        o2 = Order.objects.create(total_price=31_500, store=s1)
        OrderedProduct.objects.create(order=o2, product=p1, count=3)

        Store.objects.create(name="싱싱청과물", store_type=Store.StoreType.GROCERY)
        Store.objects.create(name="혈염산하 선지해장국", store_type=Store.StoreType.FOOD)

    def test_asdf111(self):
        User.objects.create_user(
            username="asdf",
            password="1234",
            last_name="kim",
            first_name="soungryoul",
            email="soungryoul@gmail.com",
        )
        user_qs: QuerySet[User] = User.objects.filter(last_name="kim")

        user_list: Store = list(user_qs)

        store_qs = Store.objects.values()
        store_qs

        store_qs1 = Store.objects.annotate()

        User.objects.limit(1)

        store_queryset = Store.objects.filter(id__in=[1, 2, 3])
        sql_array_str: str = ",".join(map(str, [1, 2, 3]))
        store_raw_queryset = Store.objects.raw(
            raw_query="SELECT * FROM store WHERE id IN ( %(pk_list)s )", params={"pk_list": sql_array_str}
        )

        store_qs = Store.objects.current_valid()

        Subquery
        Exists

        assert user_list


# SELECT "post"."id", (
#     SELECT U0."email"
#     FROM "comment" U0
#     WHERE U0."post_id" = ("post"."id")
#     ORDER BY U0."created_at" DESC LIMIT 1
# ) AS "newest_commenter_email" FROM "post"
