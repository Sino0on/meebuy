from django.db import models
from apps.provider.models import Category


class Product(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name='Тип')
    manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name='Производитель')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за мелкий опт', blank=True, null=True)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за крупный опт', blank=True, null=True)
    min_quantity = models.PositiveIntegerField(default=1, verbose_name='Минимальное количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Времея обновления')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    phone = models.CharField(max_length=123, blank=True, null=True, verbose_name='Телефон')
    terms_of_sale = models.CharField(max_length=200, blank=True, null=True, verbose_name='Условия продажи')
    country_of_manufacture = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна производства')
    characterization = models.CharField(max_length=200, blank=True, null=True, verbose_name='Характеристики')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImg(models.Model):
    image = models.ImageField(upload_to='images/products/%Y/%m/', verbose_name='Картинка')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return f'{self.product.title}'
