from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.provider.mixins import StatusMixin


class ProductCategory(MPTTModel):  # Использование MPTTModel
    name = models.CharField(max_length=255)
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        verbose_name="Родительская категория"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.FileField(upload_to="images/categories/", verbose_name="Иконка", blank=True, null=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    # provider = models.ForeignKey(
    #     "provider.Provider", on_delete=models.PROTECT, related_name="product_categories"
    # )

    @classmethod
    def get_category_descendants(cls, category):
        categories = [category]
        for child in category.children.all():
            categories.extend(cls.get_category_descendants(child))
        return categories

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name = _("Категория продуктов")
        verbose_name_plural = _("Категории продуктов")
class AddNewCategoryRequest(models.Model):
    parent = models.ForeignKey("ProductCategory", verbose_name="Родительская категория", on_delete=models.CASCADE,
                               null=True, blank=True)
    new_category_name = models.CharField(max_length=255, verbose_name="Новая категория")

    class Meta:
        verbose_name = _("Запрос на добавление новой категории")
        verbose_name_plural = _("Запросы на добавление новых категорий")


class Product(StatusMixin, models.Model):
    title = models.CharField(max_length=123, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    mini_desc = models.TextField(
        blank=True, null=True, verbose_name="Короткое описание"
    )
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Тип")
    manufacturer = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Производитель"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    currency = models.CharField(
        max_length=100, verbose_name=_("Валюта"), blank=True, null=True
    )
    min_quantity = models.PositiveIntegerField(
        default=1, verbose_name="Минимальное количество"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Времея обновления")
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        verbose_name="Категория",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="images/products/%Y/%m/",
        verbose_name="Картинка",
        blank=True,
        null=True,
    )
    provider = models.ForeignKey(
        "provider.Provider", on_delete=models.PROTECT, related_name="products"
    )
    phone = models.CharField(
        max_length=123, blank=True, null=True, verbose_name="Телефон"
    )
    terms_of_sale = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Условия продажи"
    )
    country_of_manufacture = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Страна производства"
    )
    characterization = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Характеристики"
    )
    product_link = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Ссылка на товар"
    )
    is_active = models.BooleanField(default=False, verbose_name="Активный товар")
    small_wholesale = models.IntegerField(verbose_name="Малая партия", blank=True, null=True)
    medium_wholesale = models.IntegerField(verbose_name="Средняя партия", blank=True, null=True)
    large_wholesale = models.IntegerField(verbose_name="Большая партия", blank=True, null=True)
    small_wholesale_price = models.IntegerField(verbose_name="Цена за малую партию", blank=True, null=True)
    medium_wholesale_price = models.IntegerField(verbose_name="Цена за среднюю партию", blank=True, null=True)
    large_wholesale_price = models.IntegerField(verbose_name="Цена за большую партию", blank=True, null=True)


    @staticmethod
    def get_count_for_today(sender):
        return Product.objects.filter(user_first=sender, is_active=True).count()


    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImg(models.Model):
    image = models.ImageField(
        upload_to="images/products/%Y/%m/", verbose_name="Картинка"
    )
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE, verbose_name="Продукт"
    )

    def __str__(self):
        return f"{self.product.title}"


class PriceColumn(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название колонки")
    formula = models.CharField(max_length=255, verbose_name="Формула расчета")
    min_order_amount = models.PositiveIntegerField(verbose_name="Сумма от", default=0)
    provider = models.ForeignKey(
        "provider.Provider", on_delete=models.PROTECT, related_name="prices"
    )

    def apply_formula(self, base_price):
        try:
            # Преобразуем base_price в Decimal, если это возможно
            price = Decimal(base_price)
            formulas = self.formula.split(";")

            for formula_part in formulas:
                print(formula_part)
                if not formula_part:  # Пропускаем пустые элементы
                    continue

                operator = formula_part[0]
                value = formula_part[1:]

                if value.endswith("%"):
                    percentage = Decimal(value[:-1]) / 100
                    if operator == "+":
                        price += price * percentage
                    elif operator == "-":
                        price -= price * percentage
                elif value.endswith("$"):
                    amount = Decimal(value[:-1])
                    if operator == "+":
                        price += amount
                    elif operator == "-":
                        price -= amount
                else:
                    amount = Decimal(value)
                    if operator == "+":
                        price += amount
                    elif operator == "-":
                        price -= amount

            return price
        except (InvalidOperation, IndexError, ValueError) as e:
            # Возвращаем исходную цену в случае ошибки
            return Decimal(base_price)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Колонка цены"
        verbose_name_plural = "Колонки цен"


class Currency(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название валюты")
    code = models.CharField(max_length=255, verbose_name="Код валюты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class ProductBanner(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    wide_banner = models.FileField(upload_to="images/banners/", verbose_name="Верхний баннер", blank=True,)
    wide_banner_mobile = models.FileField(upload_to="images/banners/", verbose_name="Верхний баннер моб", blank=True,)
    wide_banner_link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка')
    left_banner = models.FileField(upload_to="images/banners/", verbose_name="Левый баннер", blank=True,)
    left_banner_link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка')
    right_banner = models.FileField(upload_to="images/banners/", verbose_name="Правый баннер", blank=True, )
    right_banner_link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка')
    bottom_banner = models.FileField(upload_to="images/banners/", verbose_name="Нижний баннер", blank=True, )
    bottom_banner_mobile = models.FileField(upload_to="images/banners/", verbose_name="Нижний баннер моб", blank=True,)
    bottom_banner_link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
