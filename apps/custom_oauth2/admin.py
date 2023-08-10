# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model

has_email = hasattr(get_user_model(), "email")


class RegisteredApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "client_type", "authorization_grant_type")
    list_filter = ("client_type", "authorization_grant_type", "skip_authorization")
    radio_fields = {
        "client_type": admin.HORIZONTAL,
    }

    search_fields = ("name",) + (("user__email",) if has_email else ())
    raw_id_fields = ("user",)
