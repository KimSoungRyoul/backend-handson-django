# Generated by Django 4.0.4 on 2022-06-02 17:34

from django.conf import settings
from django.db import migrations

from custom_oauth2.models import RegisteredApplication


def forwards(apps, schema_editor):
    RegisteredApplication.objects.create(
        name="pycon-auth-server",
        client_type="public",
        client_id=settings.PYCON2023APP_AUTH.client_id,
        client_secret=settings.PYCON2023APP_AUTH.secret,
        authorization_grant_type="password,refresh_token,authorization-code",
    )


def backwards(apps, schema_editor):
    RegisteredApplication.objects.filter(name="pycon-auth-server").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("custom_oauth2", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=forwards,
            reverse_code=backwards,
        )
    ]
