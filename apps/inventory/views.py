
from rest_framework import viewsets
from .models import Supplier, WarehouseLocation, Inventory
from utils.pagination import CustomPagination
from .serializers import SupplierSerializer, WarehouseLocationSerializer, InventorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = CustomPagination

class WarehouseLocationViewSet(viewsets.ModelViewSet):
    queryset = WarehouseLocation.objects.all()
    serializer_class = WarehouseLocationSerializer
    pagination_class = CustomPagination

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    pagination_class = CustomPagination