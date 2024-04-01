from django.db import models
from django.contrib.auth import get_user_model
from apps.provider.models import Category, TypePay
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Country(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')


class Region(models.Model):
    title = models.CharField(max_length=123)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Регион (Область)')
        verbose_name_plural = _("Регионы (Области)")


class City(models.Model):
    title = models.CharField(max_length=123)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _('Города')


class Tender(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField()
    price = models.PositiveIntegerField(blank=True, default=0)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    requirements = models.CharField(max_length=123)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField()
    place_of_sale = models.CharField(max_length=123)
    type_pay = models.ForeignKey(TypePay, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Тендер')
        verbose_name_plural = _('Тендеры')
        ordering = ['-created_at']
