from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.db.models import Count
from datetime import datetime, timedelta

from apps.product.models import Product
from apps.provider.models import Provider
from apps.tender.models import Tender


User = get_user_model()


class Cabinet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Пользователь'))
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
    favorite_products = models.ManyToManyField(Product, related_name='user_cabinet', verbose_name=_('Избранные продукты'), blank=True)
    favorite_tenders = models.ManyToManyField(Tender, related_name='user_cabinet', verbose_name=_('Избранные закупки'), blank=True)
    favorite_providers = models.ManyToManyField(Provider, related_name='user_cabinet', verbose_name=_('Избранные оптовики'), blank=True)


    def __str__(self):
        return f'{self.user.pk} - {self.user.email}'

    class Meta:
        verbose_name = _('Кабинет')
        verbose_name_plural = _('Кабинеты')


class Status(models.Model):
    title = models.CharField(max_length=123, verbose_name=_('Название'))
    price_month = models.DecimalField(verbose_name='Цена за месяц', max_digits=100, decimal_places=1,)
    is_recomended = models.BooleanField(blank=True, default=False, verbose_name='РЕКОМЕНДУЕМ')
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
    image = models.FileField(upload_to='images/packages/', blank=True, default='1', verbose_name='Изображение')
    is_advertise = models.BooleanField(default=False, blank=True, verbose_name='Просмотр сайта без рекламы')
    is_contact_prov = models.BooleanField(default=False, blank=True, verbose_name='Просмотр контактов поставщиков')
    is_email = models.BooleanField(default=False, blank=True, verbose_name='Показ Вашего E-mail и ссылки на ваш сайт / соцсети')
    dayly_message = models.PositiveIntegerField(blank=True, default=30, verbose_name='Исходящих сообщений в день')
    is_publish_phone = models.BooleanField(default=False, blank=True, verbose_name='Показ Вашего телефона незарегистрированным посетителям')
    months = models.PositiveIntegerField(verbose_name=_('Количество месяцев'))
    priorety = models.PositiveIntegerField(max_length=1, blank=True, default=1)

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
    pg_payment_id = models.CharField(max_length=255, unique=True, verbose_name=_('ID платежа'), blank=True, null=True)
    status = models.CharField(max_length=50, default='pending', verbose_name=_('Статус'))

    def __str__(self):
        return f'{self.pk} {self.description}'

    class Meta:
        verbose_name = _('Транзакция')
        verbose_name_plural = _('Транзакции')
        ordering = ['-created_at']


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


class Contacts(SingletonModel):
    instagram = models.URLField(verbose_name=_('Instagram'), null=True, blank=True)
    whatsapp = models.URLField(verbose_name=_('WhatsApp'), null=True, blank=True)
    telegram = models.URLField(verbose_name=_('Telegram'), null=True, blank=True)
    vk = models.URLField(verbose_name=_('VK'), null=True, blank=True)
    phone = models.CharField(max_length=100, verbose_name=_('Phone'), null=True, blank=True)

    def __str__(self):
        return 'Контактная информация'

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


# class Constants(SingletonModel):
#     max_cabinets = models.PositiveIntegerField(verbose_name=_('Максимальное количество'))
#     days_color = models.PositiveIntegerField(verbose_name=_('Выделенные цветом дни'))
#     days_vip = models.PositiveIntegerField(verbose_name=_('Вип дни'))
#     is_moder = models.BooleanField(verbose_name=_('Режим модерации'), blank=True, default=False)
#
#     class Meta:
#         verbose_name = _('Константа')
#         verbose_name_plural = _('Константы')


class ViewsCountProfile(models.Model):
    user = models.ForeignKey(Cabinet, on_delete=models.CASCADE, related_name='views_count')
    quest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    @staticmethod
    def get_count_for_today(user):
        today = datetime.now().date()
        return ViewsCountProfile.objects.filter(user=user, created_at=today).count()

    @staticmethod
    def get_count_for_yesterday(user):
        yesterday = datetime.now().date() - timedelta(days=1)
        return ViewsCountProfile.objects.filter(user=user, created_at=yesterday).count()

    @staticmethod
    def get_count_for_month(user):
        today = datetime.now()
        return ViewsCountProfile.objects.filter(
            user=user,
            created_at__year=today.year,
            created_at__month=today.month
        ).count()

    @staticmethod
    def get_count_for_year(user):
        today = datetime.now()
        return ViewsCountProfile.objects.filter(
            user=user,
            created_at__year=today.year
        ).count()


class OpenNumberCount(models.Model):
    user = models.ForeignKey(Cabinet, on_delete=models.CASCADE, related_name='numbers_count')
    quest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    @staticmethod
    def get_count_for_today(user):
        today = datetime.now().date()
        return OpenNumberCount.objects.filter(user=user, created_at=today).count()

    @staticmethod
    def get_count_for_yesterday(user):
        yesterday = datetime.now().date() - timedelta(days=1)
        return OpenNumberCount.objects.filter(user=user, created_at=yesterday).count()

    @staticmethod
    def get_count_for_month(user):
        today = datetime.now()
        return OpenNumberCount.objects.filter(
            user=user,
            created_at__year=today.year,
            created_at__month=today.month
        ).count()

    @staticmethod
    def get_count_for_year(user):
        today = datetime.now()
        return OpenNumberCount.objects.filter(
            user=user,
            created_at__year=today.year
        ).count()


class SiteOpenCount(models.Model):
    user = models.ForeignKey(Cabinet, on_delete=models.CASCADE, related_name='sites_count')
    quest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    @staticmethod
    def get_count_for_today(user):
        today = datetime.now().date()
        return SiteOpenCount.objects.filter(user=user, created_at=today).count()

    @staticmethod
    def get_count_for_yesterday(user):
        yesterday = datetime.now().date() - timedelta(days=1)
        return SiteOpenCount.objects.filter(user=user, created_at=yesterday).count()

    @staticmethod
    def get_count_for_month(user):
        today = datetime.now()
        return SiteOpenCount.objects.filter(
            user=user,
            created_at__year=today.year,
            created_at__month=today.month
        ).count()

    @staticmethod
    def get_count_for_year(user):
        today = datetime.now()
        return SiteOpenCount.objects.filter(
            user=user,
            created_at__year=today.year
        ).count()


class SupportMessage(models.Model):
    CHOICES = (
        ('Компания или ИП', 'Компания или ИП'),
        ('Частное лицо', 'Частное лицо')
    )
    name = models.CharField(max_length=100, verbose_name=_('Ваше ФИО'))
    phone = models.CharField(max_length=20, verbose_name=_('Ваш номер телефона'))
    email = models.EmailField(verbose_name=_('Ваш e-mail'))
    message = models.TextField(verbose_name=_('Ваше сообщение'))
    regret_to_register = models.CharField(verbose_name=_('Оснавная цель для регистрации'), max_length=100, choices=CHOICES, default='Компания или ИП')
    agree_to_policy = models.BooleanField(default=False, verbose_name=_('Я ознакомился и согласен с условиями'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        return f'Message from {self.name} at {self.created_at}'

    class Meta:
        verbose_name = _('Сообщение поддержки')
        verbose_name_plural = _('Сообщения поддержки')


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name=_('Вопрос'))
    answer = models.TextField(verbose_name=_('Ответ'))

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _('Часто задаваемый вопрос')
        verbose_name_plural = _('Часто задаваемые вопросы')
