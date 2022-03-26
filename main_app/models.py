from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    brand = models.CharField(max_length=150)
    product_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    website_link = models.CharField(max_length=150)
    tags = models.CharField(max_length=150)
    image_link = models.CharField(max_length=1000)
    product_description = models.CharField(max_length=4000)
    product_type = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'product'

    def __str__(self):
        return f'{self.product_name} by {self.brand}'

class ProductFavorite(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_id} favorited by {self.user_id}'

class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    hex_value = models.CharField(max_length=7, blank=True, null=True)
    colour_name = models.CharField(max_length=150, blank=True, null=True)
    color_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'color'

    def __str__(self):
        return f'{self.hex_value} {self.colour_name}'

class Look(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name