from django.contrib import admin
from .models import Product, Color, Look, ProductFavorite
# Register your models here.
admin.site.register(Product)

admin.site.register(Color)

admin.site.register(Look)

admin.site.register(ProductFavorite)