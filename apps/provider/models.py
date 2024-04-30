from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=123)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='categor', null=True, blank=True, verbose_name='Родительская категория')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Provider(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название')
    mini_descr = models.CharField(max_length=250, verbose_name='Короткое описание')
    description = models.TextField()
    type = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True, verbose_name=_('Тип'))
    category = models.ManyToManyField(Category, related_name='providers', verbose_name=_('Категории'))
    post_index = models.CharField(max_length=123, blank=True, null=True, verbose_name=_('Почтовый индекс'))
    metro = models.CharField(max_length=123, blank=True, null=True, verbose_name=_('Метро'))
    image = models.ImageField(blank=True, null=True, upload_to='images/providers/avatars/%Y/%m', verbose_name=_('Аватар'))
    banner = models.ImageField(blank=True, null=True, upload_to='images/providers/banners/%Y/%m', verbose_name=_('Банер'))
    address = models.CharField(max_length=123, verbose_name=_('Адрес'))
    how_get = models.CharField(max_length=200, verbose_name=_('Как добраться'))
    work_time = models.CharField(max_length=123, verbose_name=_('Время работы'))
    phones = ArrayField(models.CharField(max_length=123), verbose_name=_('Телефон'))
    fax = models.CharField(max_length=123, verbose_name=_('Факс'))
    requisites = models.TextField()
    is_active = models.BooleanField(blank=True, default=True, verbose_name=_('Активность'))
    emp_quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Кол-во работников'))
    register_ur = models.DateField(verbose_name=_('Дата регистрации юр лица'))
    conditions = models.ManyToManyField('Condition', blank=True, verbose_name=_('Условия'))
    deliveries = models.ManyToManyField('Delivery', blank=True, verbose_name=_('Доставка'))
    is_modered = models.BooleanField(default=False, blank=True, verbose_name=_('Изменения'))
    type_pay = models.ManyToManyField('TypePay')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Поставщик')
        verbose_name_plural = _('Поставщики')


class Tag(models.Model):
    title = models.CharField(max_length=123, verbose_name='Тэг')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Тэг")
        verbose_name_plural = _("Тэги")


class Condition(models.Model):
    title = models.CharField(max_length=123, verbose_name='Состояние')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Условия")
        verbose_name_plural = _("Условии")


class Delivery(models.Model):
    title = models.CharField(max_length=123, verbose_name='Доставка')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Доставка")
        verbose_name_plural = _("Доставки")


class ProvideImg(models.Model):
    image = models.ImageField(upload_to='images/providers/%Y/%m/')
    providers = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.providers.title}'

    class Meta:
        verbose_name = _("Изображение Поставщика")
        verbose_name_plural = _("Изображения Поставщика")


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
