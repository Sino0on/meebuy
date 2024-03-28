from django.db import models
from django.contrib.auth import get_user_model
from api.user_cabinet.utils import generate_payment_link
from api.user_cabinet.utils import generate_promocode
from django.utils.translation import gettext as _

User = get_user_model()


class Cabinet(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Пользователь'))
    balance = models.PositiveIntegerField(blank=True, default=0, verbose_name=_('Баланс'))
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
    quantity_announce = models.PositiveIntegerField(verbose_name=_('Количество объявлений'))
    discount = models.PositiveIntegerField(blank=True, default=0, verbose_name=_('Скидка'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Статус')
        verbose_name_plural = _('Статусы')


class UserStatus(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='userstatuses', verbose_name=_('Статус'))
    price = models.PositiveIntegerField(verbose_name=_('Цена'))
    days = models.PositiveIntegerField(verbose_name=_('Количество дней'))

    def __str__(self):
        return _(f'{self.status.title} - {self.days} дней')

    class Meta:
        verbose_name = _('Статус пользователя')
        verbose_name_plural = _('Статусы пользователей')


class ActiveUserStatus(models.Model):
    status = models.ForeignKey(UserStatus, on_delete=models.PROTECT, related_name='active_statues', verbose_name=_('Статус'))
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


class Payment(models.Model):
    cost = models.DecimalField(max_digits=100, decimal_places=2, verbose_name=_('Цена'))
    description = models.TextField(verbose_name=_('Описание'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))
    cabinet = models.ForeignKey(Cabinet, related_name='payments', on_delete=models.SET_NULL, null=True, verbose_name=_('Кабинет'))
    is_paid = models.BooleanField(blank=True, default=False, verbose_name=_('Оплачен'))
    payment_url = models.TextField(blank=True, null=True, verbose_name=_('Ссылка на оплату'))

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()

        self.payment_url = generate_payment_link(self.cost, self.pk, self.description)
        return super().save()

    def __str__(self):
        return _(f'Счет оплаты - {self.pk}')

    class Meta:
        verbose_name = _('Оплата')
        verbose_name_plural = _('Оплаты')


class Promocode(models.Model):
    code = models.CharField(max_length=16, blank=True, unique=True, verbose_name=_('Код'))
    money = models.PositiveIntegerField(blank=True, default=0, verbose_name=_('Деньги'))
    user_status = models.ForeignKey(UserStatus, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Статус пользователя'))
    is_active = models.BooleanField(blank=True, default=True, verbose_name=_('Активный'))

    # def save(
    #     self, force_insert=False, force_update=False, using=None, update_fields=None
    # ):
    #     self.code = generate_promocode()
    #     return super().save()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_promocode(length=16)
        super(Promocode, self).save(*args, **kwargs)


    class Meta:
        verbose_name = _('Промокод')
        verbose_name_plural = _('Промокоды')


class VipStatus(models.Model):
    end_date = models.DateTimeField(verbose_name=_('Дата окончание'))
    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Активный'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))

    class Meta:
        verbose_name = _('Вип статус')
        verbose_name_plural = _('Вип статусы')


class IsColored(models.Model):
    end_date = models.DateTimeField(verbose_name=_('Дата окончание'))
    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Активный'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создание'))

    class Meta:
        verbose_name = _('Цветное объявление')
        verbose_name_plural = _('Цветные объявления')


class SingletonModel(models.Model):
    """
    Модель, которая всегда имеет только один экземпляр.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Если модель уже существует, удалите ее
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Если модель еще не существует, создайте ее
        if not cls.objects.exists():
            cls.objects.create()
        return cls.objects.get()


class Constants(SingletonModel):
    max_cabinets = models.PositiveIntegerField(verbose_name=_('Максимальное количество'))
    days_color = models.PositiveIntegerField(verbose_name=_('Выделенные цветом дни'))
    days_vip = models.PositiveIntegerField(verbose_name=_('Вип дни'))
    is_moder = models.BooleanField(verbose_name=_('Режим модерации'), blank=True, default=False)

    class Meta:
        verbose_name = _('Константа')
        verbose_name_plural = _('Константы')


class Ban(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    ipaddress = models.CharField(max_length=123, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _(f'бан на пользователя {self.user} - {self.ipaddress}')

    class Meta:
        verbose_name = _('Заблокированый IP')
        verbose_name_plural = _('Заблокированные IP')
