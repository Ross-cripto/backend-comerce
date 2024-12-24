from django.db import models
from apps.products.models import Product

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class WarehouseLocation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    inventory_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        editable=False,  # Evita que se pueda editar manualmente
    )
    product = models.ForeignKey(Product, related_name='inventories', on_delete=models.CASCADE)
    warehouse_location = models.ForeignKey(WarehouseLocation, related_name='inventories_warehouse', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generar un identificador único si no existe
        if not self.inventory_id:
            from uuid import uuid4
            self.inventory_id = uuid4().hex[:20]  # Generar un ID único de hasta 20 caracteres
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventory_id} - {self.product.name} ({self.warehouse_location.name})"
