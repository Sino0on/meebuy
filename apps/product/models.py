from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('ProductCategory', on_delete=models.PROTECT, related_name='children', null=True, blank=True, verbose_name='Родительская категория')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_category_descendants(cls, category):
        """ Рекурсивно получает все подкатегории для указанной категории. """
        categories = [category]
        for child in category.children.all():
            categories.extend(cls.get_category_descendants(child))
        return categories

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Product(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    mini_desc = models.TextField(blank=True, null=True, verbose_name='Короткое описание')
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name='Тип')
    manufacturer = models.CharField(max_length=100, blank=True, null=True, verbose_name='Производитель')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(max_length=100, verbose_name=_('Валюта'), blank=True, null=True)
    min_quantity = models.PositiveIntegerField(default=1, verbose_name='Минимальное количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Времея обновления')
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name='Категория', blank=True, null=True)
    image = models.ImageField(upload_to='images/products/%Y/%m/', verbose_name='Картинка')
    provider = models.ForeignKey('provider.Provider', on_delete=models.PROTECT, related_name='products')
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
