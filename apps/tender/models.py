from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model
from apps.provider.models import Category
from django.utils.translation import gettext_lazy as _
from apps.provider.mixins import StatusMixin


User = get_user_model()


class Country(models.Model):
    title = models.CharField(max_length=123)

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
    title = models.CharField(max_length=123)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, default=0, null=True)
    currency = models.CharField(
        max_length=100, verbose_name=_("Валюта"), blank=True, null=True
    )
    quantity = models.PositiveIntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, null=True
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True)
    phone = models.CharField(max_length=123, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    user = models.ForeignKey(
        User, related_name="tenders", on_delete=models.SET_NULL, null=True, blank=True
    )
    requirements = models.CharField(max_length=123, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField(blank=True, null=True)
    place_of_sale = models.CharField(max_length=123, blank=True, null=True)

    is_phone = models.BooleanField(default=False, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    # Payment Types
    cash = models.BooleanField(default=False, verbose_name=_("Наличными"))
    bank_transfer = models.BooleanField(
        default=False, verbose_name=_("Безналичная оплата")
    )
    credit_card = models.BooleanField(default=False, verbose_name=_("Кредитные карты"))
    electronic_money = models.BooleanField(
        default=False, verbose_name=_("Электронные деньги")
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Тендер")
        verbose_name_plural = _("Тендеры")
        ordering = ["-created_at"]


class TenderImg(models.Model):
    tender = models.ForeignKey(
        Tender, on_delete=models.CASCADE, related_name="tender_images", blank=True
    )
    image = models.ImageField(upload_to="images/tenders/")

    def __str__(self):
        return f"{self.tender}"

    class Meta:
        verbose_name = "Изображении закупки"
        verbose_name_plural = "Изображение закупки"
