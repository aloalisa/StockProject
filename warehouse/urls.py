from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, MaterialViewSet, ProductMaterialViewSet, WarehouseViewSet


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('materials', MaterialViewSet)
router.register(r'product-materials', ProductMaterialViewSet)
router.register('warehouses', WarehouseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

