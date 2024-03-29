# Generated by Django 3.2.6 on 2021-08-08 11:56
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Store",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="음식점 가게명", max_length=128)),
                ("tel_num", models.CharField(help_text="음식점 연락처", max_length=16)),
                ("created_at", models.DateTimeField()),
            ],
            options={
                "db_table": "store",
            },
        ),
    ]
