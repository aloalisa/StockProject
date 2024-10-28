from rest_framework import serializers
from .models import Product, Material, ProductMaterial, Warehouse

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'material', 'remainder', 'price']

    def validate_remainder(self, value):
        if value < 1:
            raise serializers.ValidationError('Remainder must be greater than 0.')
        return value

    def validate_price(self, value):
        if value <=0:
            raise serializers.ValidationError('Price must be greater than 0.')
        return value



