from django.db import models
from apps.provider.models import Category


class Product(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title}'
