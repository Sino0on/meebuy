from django.contrib import admin
from apps.product.models import Product, ProductImg


admin.site.register(Product)
admin.site.register(ProductImg)

