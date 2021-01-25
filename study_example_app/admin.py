from django.contrib import admin
from django.contrib.auth.models import Permission
# Register your models here.


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass
