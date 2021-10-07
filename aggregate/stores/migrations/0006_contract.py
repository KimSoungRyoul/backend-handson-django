# Generated by Django 3.2.6 on 2021-09-28 17:28
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_alter_store_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_commission', models.DecimalField(decimal_places=2, help_text='판매 수수료(%)', max_digits=5)),
                ('start_date', models.DateField(help_text='계약 시작날짜', null=True)),
                ('end_date', models.DateField(help_text='계약 종료날짜', null=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store')),
            ],
        ),
    ]
