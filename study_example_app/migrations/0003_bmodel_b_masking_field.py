# Generated by Django 3.1.4 on 2021-01-26 10:35

from django.db import migrations
import study_example_app.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('study_example_app', '0002_owner_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='bmodel',
            name='b_masking_field',
            field=study_example_app.models.fields.MaskingField(default='bb', max_length=32),
            preserve_default=False,
        ),
    ]
