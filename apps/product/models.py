from django.db import models
from apps.provider.models import Category


class Product(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за мелкий опт', blank=True, null=True)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за крупный опт', blank=True, null=True)
    min_quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    phone = models.CharField(max_length=123, blank=True, null=True)
    terms_of_sale = models.CharField(max_length=200, blank=True, null=True)
    country_of_manufacture = models.CharField(max_length=100, blank=True, null=True)
    characterization = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImg(models.Model):
    image = models.ImageField(upload_to='images/products/%Y/%m/')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title}'
