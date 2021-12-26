# Generated by Django 3.2.9 on 2021-11-07 07:58
from django.db import migrations

import aggregate


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', aggregate.users.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='StoreOwner',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', aggregate.users.models.UserManager()),
            ],
        ),
    ]