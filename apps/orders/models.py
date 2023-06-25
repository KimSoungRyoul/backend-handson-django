from __future__ import annotations

from typing import List

from django.db import models


class OrderedProduct(models.Model):
    order = models.ForeignKey(to="orders.Order", on_delete=models.CASCADE)
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    count = models.IntegerField(help_text="주문한 해당 메뉴의 갯수", default=1)

    class Meta:
        db_table = "ordered_product"
        db_table_comment = "주문된 상품, Order와 Product사이 매핑테이블"


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "주문 수락 대기중"
        ACCEPTED = "accepted", "주문 접수 완료"
        REJECTED = "rejected", "주문 거절"
        DELIVERY_COMPLETE = "delivery complete", "배달 완료"

    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        help_text="주문 상태값",
        default=Status.WAITING,
    )
    total_price = models.IntegerField(default=0)
    store = models.ForeignKey(to="stores.Store", on_delete=models.CASCADE)

    product_set = models.ManyToManyField(
        to="products.Product",
        through="OrderedProduct",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="주문이 생성된 시간")

    address = models.CharField(max_length=256, help_text="주문 배송지")


class DailyReportManager(models.Manager):
    """
    통계쿼리 Manager :  django Manager에 대한 내용은 3장을 참고하라
    """

    def get_list_by_created_at(self, created_at__gte, created_at__lt) -> List[DailyReport]:
        return list(
            self.raw(
                raw_query="""
        SELECT DATE_TRUNC('day', O.created_at) AS day,
            COUNT(*) AS total_cnt,
            SUM(O.total_price) as total_sales
        FROM orders_order O
        WHERE O.created_at >= %s AND O.created_at < %s
        group by DATE_TRUNC('day', O.created_at);
        """,
                params=[created_at__gte, created_at__lt],
            ),
        )


class DailyReport(models.Model):
    """
    일별 통계
    """

    day = models.DateField(help_text="날짜", primary_key=True)
    total_cnt = models.IntegerField(help_text="일 주문 총 갯수")
    total_sales = models.IntegerField(help_text="일 주문 총 매출")
    total_cnt = models.IntegerField(help_text="일 주문 총 갯수")

    objects = DailyReportManager()

    class Meta:
        managed = False

    def __repr__(self) -> str:
        return (
            f" {self.day.strftime('%Y-%m-%d')}:DailyReport(total_cnt:{self.total_cnt} total_sales: {self.total_sales})"
        )


class DailyReportVModel(models.Model):
    """
    일별 통계
    """

    day = models.DateField(help_text="날짜", primary_key=True)
    total_cnt = models.IntegerField(help_text="일 주문 총 갯수")
    total_sales = models.IntegerField(help_text="일 주문 총 매출")
    total_cnt = models.IntegerField(help_text="일 주문 총 갯수")

    class Meta:
        db_table = "daily_report_view_table"
