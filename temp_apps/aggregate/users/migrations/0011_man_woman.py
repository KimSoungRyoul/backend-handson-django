# Generated by Django 4.2 on 2023-05-13 03:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_department_staff_alter_user_user_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Man",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=32)),
                ("age", models.IntegerField()),
            ],
            options={
                "db_table": "man",
            },
        ),
        migrations.CreateModel(
            name="Woman",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=32)),
                ("age", models.IntegerField()),
            ],
            options={
                "db_table": "woman",
            },
        ),
    ]
