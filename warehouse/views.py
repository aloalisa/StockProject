from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductSerializer, MaterialSerializer, ProductMaterialSerializer, WarehouseSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

@api_view(['POST'])
def check_materials(request):
    product_code = request.data.get("product_code")
    quantity = request.data.get("quantity")

    try:
        product = Product.objects.get(code=product_code)
    except Product.DoesNotExist:
        raise NotFound(detail="Product with the specified code does not exist.")

    result = {
        "product_name": product.name,
        "product_qty": quantity,
        "product_materials": []
    }


    for product_material in ProductMaterial.objects.filter(product=product):
        material = product_material.material
        required_qty = quantity * product_material.quantity


        warehouses = Warehouse.objects.filter(material=material).order_by('price')
        remaining_qty = required_qty


        for warehouse in warehouses:
            if remaining_qty <= 0:
                break

            allocated_qty = min(remaining_qty, warehouse.remainder)
            result["product_materials"].append({
                "warehouse_id": warehouse.id,
                "material_name": material.name,
                "qty": allocated_qty,
                "price": warehouse.price
            })
            remaining_qty -= allocated_qty


        if remaining_qty > 0:
            result["product_materials"].append({
                "warehouse_id": None,
                "material_name": material.name,
                "qty": remaining_qty,
                "price": None
            })

    return Response({"result": [result]})




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



