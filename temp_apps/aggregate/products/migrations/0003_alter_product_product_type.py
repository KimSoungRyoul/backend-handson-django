# Generated by Django 3.2.6 on 2021-08-22 10:09
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_type",
            field=models.CharField(
                choices=[("grocery", "식료품"), ("furniture", "가구"), ("books", "책"), ("food", "음식")], max_length=32
            ),
        ),
    ]
