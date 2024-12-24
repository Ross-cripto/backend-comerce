# products/serializers.py
from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.price = validated_data.get('price', instance.price)
        instance.sku = validated_data.get('sku', instance.sku)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance