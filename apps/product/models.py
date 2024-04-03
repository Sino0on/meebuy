from django.db import models
from apps.provider.models import Category


class Product(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за мелкий опт')
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за крупный опт')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    phone = models.CharField(max_length=123)

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
