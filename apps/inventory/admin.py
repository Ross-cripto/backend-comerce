from django.contrib import admin
from .models import Supplier, WarehouseLocation, Inventory
# Register your models here.
admin.site.register(Supplier)
admin.site.register(WarehouseLocation)
admin.site.register(Inventory)