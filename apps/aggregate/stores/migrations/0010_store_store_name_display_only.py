# Generated by Django 3.2.9 on 2021-12-26 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stores", "0009_alter_store_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="store",
            name="store_name_display_only",
            field=models.CharField(default="", help_text="직원이 해당 상점을 한눈에 볼수있게 관리하는 필드입니다.", max_length=128),
            preserve_default=False,
        ),
    ]
