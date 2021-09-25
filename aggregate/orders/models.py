# Create your models here.
from django.db import models


class OrderedProduct(models.Model):
    order = models.ForeignKey(to="orders.Order", on_delete=models.CASCADE)
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    count = models.IntegerField(help_text="주문한 해당 메뉴의 갯수", default=1)

    class Meta:
        db_table = "ordered_product"


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "주문 수락 대기중"
        ACCEPTED = "accepted", "주문 접수 완료"
        REJECTED = "rejected", "주문 거절"
        DELIVERY_COMPLETE = "delivery complete", "배달 완료"

    status = models.CharField(max_length=32, choices=Status.choices, help_text="주문 상태값", default=Status.WAITING)
    total_price = models.IntegerField(default=0)
    store = models.ForeignKey(to="stores.Store", on_delete=models.CASCADE)
    product_set = models.ManyToManyField(to="products.Product", through="OrderedProduct")

    address = models.CharField(max_length=256, help_text="주문 배송지")
