# Generated by Django 3.2.6 on 2021-09-26 09:05
import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('study_example_app', '0002_auto_20210922_1107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('company_number', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='부서명', max_length=32)),
                ('description', models.CharField(help_text='해당 부서가 하는 역할', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('age', models.IntegerField()),
                ('is_deleted', models.BooleanField()),
                ('birth_date', models.DateField(null=True)),
                ('employment_period', models.FloatField(help_text='재직 기간 ex: 3.75년')),
                ('programming_language_skill', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), size=5)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_example_app.company')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_example_app.department')),
            ],
        ),
    ]