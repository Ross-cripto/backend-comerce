# inventory/serializers.py
from rest_framework import serializers
from .models import Supplier, WarehouseLocation, Inventory
from apps.products.serializers import ProductSerializer

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class WarehouseLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseLocation
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    warehouse_location = WarehouseLocationSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'