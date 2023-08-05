from django.contrib import admin

from sample_app.models import Order, Product, Store

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Store)
