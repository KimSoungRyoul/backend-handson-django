from django.contrib import admin
from django.contrib.auth.models import Permission

from study_example_app.models import DjangoModel


# Register your models here.


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(DjangoModel)
class ExampleUserAdmin(admin.ModelAdmin):
    date_hierarchy = "datetime_field"
    list_display = ("str_field", "int_field", "float_field", "date_field")

    enable_nav_sidebar = True
