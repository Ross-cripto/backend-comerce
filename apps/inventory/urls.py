# inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, WarehouseLocationViewSet, InventoryViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'warehouse-locations', WarehouseLocationViewSet)
router.register(r'inventories', InventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]