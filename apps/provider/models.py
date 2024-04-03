from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=123)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='categor', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Provider(models.Model):
    title = models.CharField(max_length=123)
    mini_descr = models.CharField(max_length=250)
    description = models.TextField()
    type = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)
    category = models.ManyToManyField(Category, related_name='providers')
    post_index = models.CharField(max_length=123, blank=True, null=True)
    metro = models.CharField(max_length=123, blank=True, null=True)
    banner = models.ImageField(blank=True, null=True, upload_to='images/providers/banners/%Y/%m')
    address = models.CharField(max_length=123)
    how_get = models.CharField(max_length=123)
    work_time = models.CharField(max_length=123)
    phones = ArrayField(models.CharField(max_length=123))
    fax = models.CharField(max_length=123)
    requisites = models.TextField()
    emp_quantity = models.PositiveIntegerField(blank=True, null=True)
    register_ur = models.DateField(verbose_name=_('Дата регистрации юр лица'))
    conditions = models.ManyToManyField('Condition', null=True, blank=True)
    deliveries = models.ManyToManyField('Delivery', null=True, blank=True)
    is_modered = models.BooleanField(default=False, blank=True)
    type_pay = models.ManyToManyField('TypePay')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Поставщик')
        verbose_name_plural = _('Поставщики')


class Tag(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Тэг")
        verbose_name_plural = _("Тэги")


class Condition(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Условия")
        verbose_name_plural = _("Условии")


class Delivery(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Доставка")
        verbose_name_plural = _("Доставки")


class ProvideImg(models.Model):
    image = models.ImageField(upload_to='images/providers/%Y/%m/')
    providers = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Изображения Поставщика")
        verbose_name_plural = _("Изображении Поставщика")


class ProvideFiles(models.Model):
    image = models.ImageField(upload_to='images/providers/%Y/%m/')
    providers = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Файл Поставщика")
        verbose_name_plural = _("Файлы Поставщика")


class TypePay(models.Model):
    title = models.CharField(max_length=123)
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Вариант оплаты')
        verbose_name_plural = _('Варианты оплаты')
