# Generated by Django 3.2.6 on 2021-08-08 11:56
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("stores", "0001_initial"),
        ("orders", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="store",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="stores.store"),
        ),
    ]
