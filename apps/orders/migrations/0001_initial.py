# Generated by Django 4.2.2 on 2023-06-25 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("stores", "0002_store_description_delete_storetext"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DailyReport",
            fields=[
                (
                    "day",
                    models.DateField(help_text="날짜", primary_key=True, serialize=False),
                ),
                ("total_sales", models.IntegerField(help_text="일 주문 총 매출")),
                ("total_cnt", models.IntegerField(help_text="일 주문 총 갯수")),
            ],
            options={
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DailyReportVModel",
            fields=[
                (
                    "day",
                    models.DateField(help_text="날짜", primary_key=True, serialize=False),
                ),
                ("total_sales", models.IntegerField(help_text="일 주문 총 매출")),
                ("total_cnt", models.IntegerField(help_text="일 주문 총 갯수")),
            ],
            options={
                "db_table": "daily_report_view_table",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("waiting", "주문 수락 대기중"),
                            ("accepted", "주문 접수 완료"),
                            ("rejected", "주문 거절"),
                            ("delivery complete", "배달 완료"),
                        ],
                        default="waiting",
                        help_text="주문 상태값",
                        max_length=32,
                    ),
                ),
                ("total_price", models.IntegerField(default=0)),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="주문이 생성된 시간"),
                ),
                (
                    "address",
                    models.CharField(help_text="주문 배송지", max_length=256),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderedProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "count",
                    models.IntegerField(default=1, help_text="주문한 해당 메뉴의 갯수"),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "db_table": "ordered_product",
                "db_table_comment": "주문된 상품, Order와 Product사이 매핑테이블",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="product_set",
            field=models.ManyToManyField(through="orders.OrderedProduct", to="products.product"),
        ),
        migrations.AddField(
            model_name="order",
            name="store",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="stores.store"),
        ),
    ]