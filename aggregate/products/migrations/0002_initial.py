# Generated by Django 3.2.6 on 2021-08-08 11:56
import django.contrib.postgres.indexes
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("stores", "0001_initial"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="store",
            field=models.ForeignKey(
                help_text="이 상품을 판매하는 가게", on_delete=django.db.models.deletion.CASCADE, to="stores.store",
            ),
        ),
        migrations.CreateModel(
            name="BooksProduct",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": []},
            bases=("products.product",),
        ),
        migrations.CreateModel(
            name="FurnitureProduct",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": []},
            bases=("products.product",),
        ),
        migrations.CreateModel(
            name="GroceryProduct",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": []},
            bases=("products.product",),
        ),
        migrations.AddIndex(model_name="product", index=models.Index(fields=["created_at"], name="created_at_index")),
        migrations.AddIndex(
            model_name="product", index=models.Index(fields=["name", "product_type"], name="name_pt_composite_index"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=django.contrib.postgres.indexes.HashIndex(fields=["name"], name="name_hash_index"),
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.CheckConstraint(
                check=models.Q(("price__lte", 100000000)), name="check_unreasonalbe_price",
            ),
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.UniqueConstraint(fields=("store", "name", "product_type"), name="unique_in_store"),
        ),
    ]