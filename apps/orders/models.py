from django.db import models
from apps.products.models import Product
from apps.inventory.models import WarehouseLocation
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    """
    Modelo para registrar las transacciones de productos.
    Puede ser de tipo 'Ingreso' o 'Salida'.
    """
    TRANSACTION_TYPES = (
        ('IN', 'Ingreso'),
        ('OUT', 'Salida'),
    )

    product = models.ForeignKey(
        Product,
        related_name='transactions',
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    transaction_type = models.CharField(
        max_length=3,
        choices=TRANSACTION_TYPES,
        verbose_name="Tipo de Transacción"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    warehouse_location = models.ForeignKey(
        WarehouseLocation,
        related_name='transactions',
        on_delete=models.CASCADE,
        verbose_name="Ubicación en Almacén"
    )
    user = models.ForeignKey(
        User,
        related_name='transactions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario Responsable"
    )
    remarks = models.TextField(
        null=True,
        blank=True,
        verbose_name="Comentarios"
    )

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type} - {self.quantity}"


class Order(models.Model):
    """
    Modelo para gestionar pedidos realizados por los usuarios.
    """
    STATUS_TYPES = (
        ('Pending', 'Pendiente'),
        ('Completed', 'Completado'),
        ('Cancelled', 'Cancelado'),
    )

    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE,
        verbose_name="Usuario"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado En")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado En")
    status = models.CharField(
        max_length=20,
        choices=STATUS_TYPES,
        default='Pending',
        verbose_name="Estado del Pedido"
    )
    remarks = models.TextField(
        null=True,
        blank=True,
        verbose_name="Comentarios"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.first_name} - {self.status}"


class OrderItem(models.Model):
    """
    Modelo para gestionar los ítems de un pedido.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name="Pedido"
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio Unitario"
    )

    class Meta:
        verbose_name = "Ítem de Pedido"
        verbose_name_plural = "Ítems de Pedido"

    def __str__(self):
        return f"{self.order.user.first_name} - {self.product.name} - {self.quantity}"