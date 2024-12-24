import random
from django.core.management.base import BaseCommand
from apps.products.models import Category, Product
from apps.inventory.models import Supplier, WarehouseLocation, Inventory
from apps.orders.models import Order, OrderItem, Transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Populate database with sample data"

    def handle(self, *args, **kwargs):
        # Limpiar datos existentes
        Product.objects.all().delete()
        Category.objects.all().delete()
        Supplier.objects.all().delete()
        WarehouseLocation.objects.all().delete()
        Inventory.objects.all().delete()
        Transaction.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()

        # Agregar Categorías (5 categorías)
        categories = [
            {"name": "Electronics", "description": "Devices and gadgets."},
            {"name": "Books", "description": "Books across all genres."},
            {"name": "Clothing", "description": "Apparel for men, women, and children."},
            {"name": "Furniture", "description": "Home and office furniture."},
            {"name": "Toys", "description": "Toys and games for children."},
        ]

        category_objects = []
        for category_data in categories:
            category, created = Category.objects.get_or_create(**category_data)
            category_objects.append(category)

        # Crear Productos (5 productos por categoría)
        products = []
        for category in category_objects:
            for i in range(5):
                product = {
                    "name": f"{category.name} Product {i+1}",
                    "category": category,
                    "stock": random.randint(50, 200),
                    "price": round(random.uniform(10, 500), 2),
                    "sku": f"{category.name[:3].upper()}_{random.randint(1000, 9999)}",
                    "description": f"Description for {category.name} product {i+1}."
                }
                products.append(product)

        product_objects = []
        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            product_objects.append(product)

        # Crear Proveedores (5 proveedores)
        suppliers = [
            {"name": "TechSupplies", "contact_person": "John Doe", "email": "john@techsupplies.com", "phone": "123456789", "address": "123 Tech Street"},
            {"name": "BookDistributors", "contact_person": "Jane Doe", "email": "jane@bookdistributors.com", "phone": "987654321", "address": "456 Book Ave"},
            {"name": "FashionMart", "contact_person": "Emily Smith", "email": "emily@fashionmart.com", "phone": "555555555", "address": "789 Fashion Rd"},
            {"name": "FurniturePro", "contact_person": "Michael Johnson", "email": "michael@furniturepro.com", "phone": "444444444", "address": "101 Furniture Blvd"},
            {"name": "ToyWorld", "contact_person": "Sarah Lee", "email": "sarah@toyworld.com", "phone": "666666666", "address": "202 Toy St"},
        ]

        supplier_objects = []
        for supplier_data in suppliers:
            supplier, created = Supplier.objects.get_or_create(**supplier_data)
            supplier_objects.append(supplier)

        # Crear Ubicaciones de Almacén (5 ubicaciones)
        warehouse_locations = [
            {"name": "Main Warehouse", "address": "123 Warehouse Rd."},
            {"name": "Secondary Warehouse", "address": "456 Storage Blvd."},
            {"name": "North Warehouse", "address": "789 North St."},
            {"name": "South Warehouse", "address": "101 South Ave."},
            {"name": "East Warehouse", "address": "202 East Ln."},
        ]

        warehouse_location_objects = []
        for location_data in warehouse_locations:
            warehouse_location, created = WarehouseLocation.objects.get_or_create(**location_data)
            warehouse_location_objects.append(warehouse_location)

        # Crear Inventarios (5 inventarios)
        inventory_data = []
        for product in product_objects:
            location = random.choice(warehouse_location_objects)
            quantity = random.randint(50, 200)
            inventory_data.append({"product": product, "warehouse_location": location, "quantity": quantity})

        for inventory in inventory_data:
            Inventory.objects.get_or_create(**inventory)

        # Crear Transacciones (5 transacciones)
        transaction_data = []
        for product in product_objects:
            supplier = random.choice(supplier_objects)
            transaction_type = random.choice(["purchase", "sale"])
            quantity = random.randint(1, 10)
            transaction_data.append({"product": product, "quantity": quantity, "transaction_type": transaction_type, "supplier": supplier})

        for transaction in transaction_data:
            Transaction.objects.get_or_create(**transaction)

        # Crear Órdenes (5 órdenes)
        user = User.objects.first() or User.objects.create_user(username="customer", password="password123")  # Asegurarse que hay un usuario
        orders = [
            {"order_number": f"ORD{str(i).zfill(3)}", "customer": user}
            for i in range(1, 6)
        ]

        order_objects = []
        for order_data in orders:
            order, created = Order.objects.get_or_create(**order_data)
            order_objects.append(order)

        # Crear Detalles de Órdenes (5 detalles)
        order_items = []
        for order in order_objects:
            for product in product_objects:
                order_items.append({"order": order, "product": product, "quantity": random.randint(1, 3), "price": product.price})

        for order_item_data in order_items:
            OrderItem.objects.get_or_create(**order_item_data)

        self.stdout.write(self.style.SUCCESS("Database populated successfully"))
