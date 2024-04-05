from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class Cabinet(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Пользователь'))
    balance = models.PositiveIntegerField(blank=True, default=0, verbose_name=_('Баланс'))
    is_upping = models.ForeignKey('ActiveUpping', blank=True, null=True, on_delete=models.SET_NULL)
    user_status = models.ForeignKey(
        'ActiveUserStatus',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='user_statuses',
        verbose_name=_('Статус пользователя')
    )

    def __str__(self):
        return f'{self.user.pk} - {self.user.email}'

    class Meta:
        verbose_name = _('Кабинет')
        verbose_name_plural = _('Кабинеты')


class Status(models.Model):
    title = models.CharField(max_length=123, verbose_name=_('Название'))
    price_month = models.DecimalField(verbose_name='Цена за месяц', max_digits=100, decimal_places=1)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Статус')
        verbose_name_plural = _('Статусы')


class PackageStatus(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='packagestatuses', verbose_name=_('Статус'))
    price = models.DecimalField(verbose_name=_('Цена'), max_digits=100, decimal_places=1)
    quantity_products = models.PositiveIntegerField(verbose_name=_('Количество объявлений'))
    quantity_tenders = models.PositiveIntegerField(verbose_name=_('Количество закупок'))
    is_advertise = models.BooleanField(default=False, blank=True)
    is_contact_prov = models.BooleanField(default=False, blank=True)
    dayly_message = models.PositiveIntegerField(blank=True, default=30)
    is_publish_phone = models.BooleanField(default=False, blank=True)
    months = models.PositiveIntegerField(verbose_name=_('Количество месяцев'))

    def __str__(self):
        return _(f'{self.status.title} - {self.months} месяцев')

    def get_discount(self):
        return self.status.price_month - self.get_month_price()

    def get_month_price(self):
        return self.price // self.months

    class Meta:
        verbose_name = _('Статус пользователя')
        verbose_name_plural = _('Статусы пользователей')


class ActiveUserStatus(models.Model):
    status = models.ForeignKey(PackageStatus, on_delete=models.PROTECT, related_name='active_statues', verbose_name=_('Статус'))
    end_date = models.DateField(verbose_name=_('Дата окончание'))
    is_active = models.BooleanField(default=False, blank=True, verbose_name=_('Активный'))

    def __str__(self):
        return f'{self.status.pk}'

    class Meta:
        verbose_name = _('Активный статус пользователя')
        verbose_name_plural = _('Активные статусы пользователей')


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))
    user = models.ForeignKey(
        Cabinet,
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True,
        blank=True,
        verbose_name=_('Пользователь')
    )
    total = models.IntegerField(blank=True, default=0, verbose_name=_('Итого'))
    description = models.TextField(verbose_name=_('Описание'))

    def __str__(self):
        return f'{self.pk} {self.description}'

    class Meta:
        verbose_name = _('Транзакция')
        verbose_name_plural = _('Транзакции')


class Upping(models.Model):
    days = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=1, max_digits=100)

    def __str__(self):
        return f'Поднятие в топ на - {self.days} дней'

    class Meta:
        verbose_name = 'Поднятие в топ'
        verbose_name_plural = 'Поднятии в топ'


class ActiveUpping(models.Model):
    upping = models.ForeignKey(Upping, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True, blank=True)
    end_date = models.DateField()

    def __str__(self):
        return f'Активное поднятие на  - {self.upping.days} дней'


# class SingletonModel(models.Model):
#     """
#     Модель, которая всегда имеет только один экземпляр.
#     """
#
#     class Meta:
#         abstract = True
#
#     def save(self, *args, **kwargs):
#         # Если модель уже существует, удалите ее
#         self.__class__.objects.exclude(id=self.id).delete()
#         super(SingletonModel, self).save(*args, **kwargs)
#
#     @classmethod
#     def load(cls):
#         # Если модель еще не существует, создайте ее
#         if not cls.objects.exists():
#             cls.objects.create()
#         return cls.objects.get()


# class Constants(SingletonModel):
#     max_cabinets = models.PositiveIntegerField(verbose_name=_('Максимальное количество'))
#     days_color = models.PositiveIntegerField(verbose_name=_('Выделенные цветом дни'))
#     days_vip = models.PositiveIntegerField(verbose_name=_('Вип дни'))
#     is_moder = models.BooleanField(verbose_name=_('Режим модерации'), blank=True, default=False)
#
#     class Meta:
#         verbose_name = _('Константа')
#         verbose_name_plural = _('Константы')
