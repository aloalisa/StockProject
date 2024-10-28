from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductSerializer, MaterialSerializer, ProductMaterialSerializer, WarehouseSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ProductMaterialViewSet(viewsets.ModelViewSet):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer


@action(detail=True, methods=['get'])


def required_quantity(self, request, pk=None):
    product_material = self.get_object()
    required = product_material.quantity
    return Response({'required_quantity': required})



class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    @action(detail=True, methods=['GET'])
    def check_availability(self, request, pk=None):
        warehouse = self.get_object()
        if warehouse.remainder>0:
            return Response({'status':'In stock', 'quantity':warehouse.remainder})
        return Response({'status':'Out of Stock'}, status=status.HTTP_400_BAD_REQUEST)



