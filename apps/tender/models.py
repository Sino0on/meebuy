from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.provider.mixins import StatusMixin
from apps.provider.models import Category

User = get_user_model()


class Country(models.Model):
    title = models.CharField(max_length=123)
    code = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Страна")
        verbose_name_plural = _("Страны")


class Region(models.Model):
    title = models.CharField(max_length=123)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Регион (Область)")
        verbose_name_plural = _("Регионы (Области)")


class City(models.Model):
    title = models.CharField(max_length=123)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Город")
        verbose_name_plural = _("Города")


class Tender(StatusMixin, models.Model):
    title = models.CharField(max_length=123, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name="Цена")
    currency = models.CharField(max_length=100, verbose_name="Валюта", blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name="Количество")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Категория")
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Город")
    phone = models.CharField(max_length=123, blank=True, null=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Электронная почта")
    user = models.ForeignKey(User, related_name="tenders", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    requirements = models.CharField(max_length=123, blank=True, null=True, verbose_name="Требования")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    end_date = models.DateField(blank=True, null=True, verbose_name="Дата окончания")
    place_of_sale = models.CharField(max_length=123, blank=True, null=True, verbose_name="Место продажи")

    is_phone = models.BooleanField(default=False, blank=True, null=True, verbose_name="Наличие телефона")
    is_active = models.BooleanField(default=True, blank=True, null=True, verbose_name="Активен")
    # Payment Types
    cash = models.BooleanField(default=False, verbose_name="Наличными")
    bank_transfer = models.BooleanField(default=False, verbose_name="Безналичная оплата")
    credit_card = models.BooleanField(default=False, verbose_name="Кредитные карты")
    electronic_money = models.BooleanField(default=False, verbose_name="Электронные деньги")
    # Sales Locations
    retail_store = models.BooleanField(default=False, verbose_name=_("Розничный магазин"))
    marketplaces = models.BooleanField(default=False, verbose_name=_("Маркетплейсы"))
    online_store = models.BooleanField(default=False, verbose_name=_("Интернет-магазин"))
    social_networks = models.BooleanField(default=False, verbose_name=_("Соцсети, доски объявлений"))
    wholesale_resale = models.BooleanField(default=False, verbose_name=_("Оптовая перепродажа"))
    group_purchases = models.BooleanField(default=False, verbose_name=_("Совместные покупки"))
    for_personal_use = models.BooleanField(default=False, verbose_name=_("Для собственного потребления"))

    # Wholesale Information
    large_wholesale = models.BooleanField(default=False, verbose_name=_("Крупный опт"))
    small_wholesale = models.BooleanField(default=False, verbose_name=_("Мелкий опт"))
    retail = models.BooleanField(default=False, verbose_name=_("Поштучно"))
    official_distributor = models.BooleanField(verbose_name=_("Официальный дистрибьютор"), blank=True, null=True)

    class PurchaseFrequency(models.TextChoices):
        ONCE = 'once', _("Однократно")
        WEEKLY = 'weekly', _("Каждую неделю")
        MONTHLY = 'monthly', _("Каждый месяц")
        MULTIPLE_TIMES_YEAR = 'multiple_times_year', _("Несколько раз в год")
        TWICE_YEAR = 'twice_year', _("Пару раз в год")

    purchase_frequency = models.CharField(
        max_length=20,
        choices=PurchaseFrequency.choices,
        verbose_name=_("Как часто планируете закупать"),
        default=PurchaseFrequency.ONCE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Тендер")
        verbose_name_plural = _("Тендеры")
        ordering = ["-created_at"]


class TenderImg(models.Model):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name="tender_images", blank=True)
    image = models.ImageField(upload_to="images/tenders/")

    def __str__(self):
        return f"{self.tender}"

    class Meta:
        verbose_name = "Изображении закупки"
        verbose_name_plural = "Изображение закупки"


class SearchRequest(models.Model):
    user = models.ForeignKey(User, related_name="search_requests", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    created_at = models.DateField(auto_now=True)
    name = models.TextField(verbose_name='Запрос', null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
