# Generated by Django 4.2 on 2023-04-23 07:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stores", "0010_store_store_name_display_only"),
    ]

    operations = [
        migrations.AlterModelTableComment(
            name="store",
            table_comment="상점",
        ),
    ]
