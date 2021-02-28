from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.

from study_example_app.models import ExampleUser


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(ExampleUser)
class ExampleUserAdmin(admin.ModelAdmin):
    date_hierarchy = "date_joined"
    fields = ( "username", "first_name", "last_name", "email",  ("is_active", "is_staff"),)
    enable_nav_sidebar = True