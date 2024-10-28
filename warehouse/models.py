from django.db import models

# Create your models here.


#Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


#Material Model
class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ProductMaterial (Intermediary Table) Model
class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material=models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of  {self.material.name} for  {self.product.name}"


#Warehouse model

class Warehouse(models.Model):
    material=models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder=models.DecimalField(max_digits=10, decimal_places=2)
    price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.material} of {self.remainder} at {self.price}"

