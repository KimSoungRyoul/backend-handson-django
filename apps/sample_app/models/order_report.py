from __future__ import annotations

from django.db import models


class DailyReportManager(models.Manager):
    """
    통계쿼리 Manager
    """

    def get_list_by_created_at(self, created_at__gte, created_at__lt) -> list[DailyReport]:
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
