# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Transaction
from apps.products.serializers import ProductSerializer
from apps.inventory.serializers import WarehouseLocationSerializer

class TransactionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    warehouse_location = WarehouseLocationSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order