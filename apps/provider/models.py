from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=123)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='categor', null=True, blank=True, verbose_name='Родительская категория')
    icon = models.FileField(upload_to='images/category/icons/')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_category_descendants(cls, category):
        """ Рекурсивно получает все подкатегории для указанной категории. """
        categories = [category]
        for child in category.categor.all():  # используем related_name
            categories.extend(cls.get_category_descendants(child))
        return categories

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Provider(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название', blank=True, null=True)
    mini_descr = models.CharField(max_length=250, verbose_name='Короткое описание', blank=True, null=True)
    type = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True, verbose_name=_('Тип'), blank=True)
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name='providers', verbose_name=_('Категории'), blank=True, null=True)
    city = models.ForeignKey('tender.City', on_delete=models.SET_NULL, blank=True, null=True)
    how_get = models.CharField(max_length=200, verbose_name=_('Как добраться'), blank=True, null=True)
    post_index = models.CharField(max_length=123, blank=True, null=True, verbose_name=_('Почтовый индекс'))
    metro = models.CharField(max_length=123, blank=True, null=True, verbose_name=_('Метро'))
    address = models.CharField(max_length=123, verbose_name=_('Адрес'), blank=True, null=True)
    work_time = models.CharField(max_length=123, verbose_name=_('Время работы'), blank=True, null=True)
    phones = ArrayField(models.CharField(max_length=123), verbose_name=_('Телефон'), blank=True, null=True)
    web_site = models.URLField(verbose_name=_('Вебсайт'), blank=True, null=True)
    fax = models.CharField(max_length=123, verbose_name=_('Факс'), blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    image = models.ImageField(blank=True, null=True, upload_to='images/providers/avatars/%Y/%m', verbose_name=_('Аватар'))
    banner = models.ImageField(blank=True, null=True, upload_to='images/providers/banners/%Y/%m', verbose_name=_('Банер'))
    requisites = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, default=True, verbose_name=_('Активность'))
    emp_quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Кол-во работников'))
    register_ur = models.DateField(verbose_name=_('Дата регистрации юр лица'), blank=True, null=True)
    conditions = models.ManyToManyField('Condition', blank=True, verbose_name=_('Условия'), null=True)
    deliveries = models.ManyToManyField('Delivery', blank=True, verbose_name=_('Доставка'), null=True)
    is_modered = models.BooleanField(default=False, blank=True, verbose_name=_('Прошла модерацию'), null=True)
    type_pay = models.ManyToManyField('TypePay', blank=True, null=True)

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
