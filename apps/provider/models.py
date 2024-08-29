from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.provider.mixins import StatusMixin

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=123)
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="categor",
        null=True,
        blank=True,
        verbose_name="Родительская категория",
    )
    icon = models.FileField(upload_to="images/category/icons/", null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_main_category = models.BooleanField(default=False, verbose_name="Главная категория")

    @classmethod
    def get_category_descendants(cls, category):
        """Рекурсивно получает все подкатегории для указанной категории."""
        categories = [category]
        for child in category.categor.all():
            categories.extend(cls.get_category_descendants(child))
        return categories

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Provider(StatusMixin, models.Model):
    class BusinessType(models.TextChoices):
        WHOLESALE = "wholesale", _("Оптовая продажа товаров (вы поставщик)")
        MANUFACTURING = "manufacturing", _("Производство товаров (вы производитель)")
        SERVICES = "services", _(
            "Оказание услуг логистики / поиска товаров / таможенного оформления"
        )

    is_modered = models.BooleanField(default=False, verbose_name=_("Прошла модерацию"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активность"))
    title = models.CharField(max_length=123, verbose_name="Название", blank=True, null=True)
    mini_descr = models.CharField(max_length=250, verbose_name="Короткое описание", blank=True, null=True)
    type = models.CharField(max_length=20, choices=BusinessType.choices,
                            verbose_name=_("Основная деятельность вашей компании"), default=BusinessType.WHOLESALE,
                            blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="providers", verbose_name=_("Категории"), blank=True)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Минимальный заказ"),
                                        blank=True, null=True, )
    keywords = models.TextField(blank=True, null=True, verbose_name=_("Ключевые слова"))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Дата создания")
    email = models.EmailField(blank=True, null=True, verbose_name="Электронная почта")
    is_provider = models.BooleanField(default=False, verbose_name="Поставщик")
    comment = models.TextField(blank=True,
                               default="Анкета компании заполнена некорректно! Корректно заполните название компании, описание, контактные данные. Затем подайте на перепроверку.",
                               verbose_name="Комментарий", )
    decimal_places = models.PositiveSmallIntegerField(default=0, verbose_name="Десятичные разряды")

    # Wholesale Information
    large_wholesale = models.BooleanField(default=False, verbose_name=_("Крупный опт"))
    small_wholesale = models.BooleanField(default=False, verbose_name=_("Мелкий опт"))
    retail = models.BooleanField(default=False, verbose_name=_("Поштучно"))
    official_distributor = models.BooleanField(verbose_name=_("Официальный дистрибьютор"), blank=True, null=True)

    # City Information
    city = models.ForeignKey("tender.City", on_delete=models.SET_NULL, blank=True, null=True)
    how_get = models.CharField(max_length=200, verbose_name=_("Как добраться"), blank=True, null=True)
    post_index = models.CharField(max_length=123, blank=True, null=True, verbose_name=_("Почтовый индекс"))
    metro = models.CharField(max_length=123, blank=True, null=True, verbose_name=_("Метро"))
    address = models.CharField(max_length=123, verbose_name=_("Адрес"), blank=True, null=True)
    work_time = models.CharField(max_length=123, verbose_name=_("Время работы"), blank=True, null=True)
    phones = models.CharField(max_length=123, verbose_name=_("Телефон"), blank=True, null=True)
    web_site = models.URLField(verbose_name=_("Вебсайт"), blank=True, null=True)
    youtube_video = models.URLField(verbose_name=_("Видео с Ютуба"), blank=True, null=True)
    fax = models.CharField(max_length=123, verbose_name=_("Факс"), blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    image = models.ImageField(blank=True, null=True, upload_to="images/providers/avatars/%Y/%m",
                              verbose_name=_("Аватар"), )
    banner = models.ImageField(blank=True, null=True, upload_to="images/providers/banners/%Y/%m",
                               verbose_name=_("Банер"), )
    requisites = models.TextField(blank=True, null=True, verbose_name="Реквизиты")
    emp_quantity = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Кол-во работников"))
    register_ur = models.DateField(blank=True, null=True, verbose_name=_("Дата регистрации юр лица"))

    # Conditions
    installment = models.BooleanField(default=False, verbose_name=_("Возможна рассрочка"), blank=True)
    credit = models.BooleanField(default=False, verbose_name=_("Возможен кредит"))
    deposit = models.BooleanField(default=False, verbose_name=_("Возможен депозит"))
    consignment = models.BooleanField(default=False, verbose_name=_("Возможна передача под реализацию"))
    dropshipping = models.BooleanField(default=False, verbose_name=_("Возможен дропшиппинг"))
    showroom = models.BooleanField(default=False, verbose_name=_("Есть шоурум"))
    marketplace_sale = models.BooleanField(default=False, verbose_name=_("Разрешена продажа на маркетплейсах"))

    # Deliveries
    pickup = models.BooleanField(default=False, verbose_name=_("Самовывоз"))
    transport_company = models.BooleanField(default=False, verbose_name=_("Транспортной компанией"))
    by_car = models.BooleanField(default=False, verbose_name=_("Автомобилем"))
    air_transport = models.BooleanField(default=False, verbose_name=_("Авиатранспортом"))
    rail_transport = models.BooleanField(default=False, verbose_name=_("Железной дорогой"))
    courier = models.BooleanField(default=False, verbose_name=_("Курьером"))

    # Payment Types
    cash = models.BooleanField(default=False, verbose_name=_("Наличными"))
    bank_transfer = models.BooleanField(default=False, verbose_name=_("Безналичная оплата"))
    credit_card = models.BooleanField(default=False, verbose_name=_("Кредитные карты"))
    electronic_money = models.BooleanField(default=False, verbose_name=_("Электронные деньги"))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Поставщик")
        verbose_name_plural = _("Поставщики")


class ProvideImg(models.Model):
    image = models.ImageField(upload_to="images/providers/%Y/%m/", verbose_name="Изображение Поставщика")
    providers = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self):
        return f"{self.providers.title}"

    class Meta:
        verbose_name = _("Изображение Поставщика")
        verbose_name_plural = _("Изображения Поставщика")


class ProvideFiles(models.Model):
    image = models.FileField(upload_to="images/providers/%Y/%m/", verbose_name="Файл Поставщика")
    providers = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="files"
    )

    def __str__(self):
        return f"{self.image.url}"

    class Meta:
        verbose_name = _("Файл Поставщика")
        verbose_name_plural = _("Файлы Поставщика")


class PriceFiles(models.Model):
    file = models.FileField(upload_to="files/price/%Y/%m/", verbose_name="Файл цены")
    providers = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="files_price"
    )

    def __str__(self):
        return f"{self.file}"

    class Meta:
        verbose_name = _("Файл цены")
        verbose_name_plural = _("Файлы цен")


class VerificationDocuments(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="documents")
    document = models.FileField(upload_to='provider_documents/%Y/%m/', verbose_name="Документ")
    verified = models.BooleanField(default=False, verbose_name='Подтверждено')

    def __str__(self):
        return f"{self.document.name}"

    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Документы")


class ProviderLink(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="links")
    name = models.CharField(max_length=255, verbose_name="Название")
    link = models.URLField(verbose_name="Ссылка")
    verified = models.BooleanField(default=False, verbose_name='Подтверждено')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Ссылка")
        verbose_name_plural = _("Ссылки")
