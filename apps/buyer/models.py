from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.tender.models import City
from apps.user_cabinet.models import SingletonModel

User = get_user_model()


class Buyer(models.Model):
    title = models.CharField(max_length=123, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mini_desc = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True)
    image = models.ImageField(upload_to="images/avatars/buyer/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=123, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
        ordering = ["-created_at"]


class BuyerImg(models.Model):
    image = models.ImageField(upload_to="images/buyer/%Y/%m/")
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f"{self.buyer.title}"

    class Meta:
        verbose_name = _("Изображение Продавца")
        verbose_name_plural = _("Изображения Продавца")


class BuyerFiles(models.Model):
    image = models.ImageField(upload_to="images/providers/%Y/%m/")
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Файл Продавца")
        verbose_name_plural = _("Файлы Продавца")


class BannerSettings(SingletonModel):
    number = models.PositiveIntegerField(verbose_name="Очередность", default=3)

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = _("Очередность")


class Banner(models.Model):
    TYPE_CHOICES = (
        ("provider", _("Поставщики")),
        ("tender", _("Закупки")),
        ("buyer", _("Покупатели")),
    )

    title = models.CharField(
        verbose_name="Телефон", max_length=123, blank=True, null=True
    )
    image_desktop = models.ImageField(
        verbose_name="Картинка круп", upload_to="images/banners/desktop/%Y/%m/", blank=True, null=True
    )
    image_mobile = models.ImageField(
        verbose_name="Картинка моб", upload_to="images/banners/mobile/%Y/%m/", blank=True, null=True
    )
    image_vertical = models.FileField(
        verbose_name="Картинка верт", upload_to="images/banners/vertical/%Y/%m/", blank=True, null=True
    )
    page_for = models.CharField(
        verbose_name="Страница",
        choices=TYPE_CHOICES,
        max_length=200,
        blank=False,
        null=False,
        default="provider",
    )
    link = models.URLField(verbose_name="ссылка", max_length=200, blank=True, null=True)
    settings = models.ForeignKey(
        BannerSettings, verbose_name="Настройки", on_delete=models.CASCADE, blank=True, null=True
    )
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, blank=True, null=True
    )

    def get_image_desktop(self):
        if self.image_desktop:
            return mark_safe(
                f'<img src="{self.image_desktop.url}" width="328" height="100" />'
            )
        return ""

    def get_image_mobile(self):
        if self.image_mobile:
            return mark_safe(
                f'<img src="{self.image_mobile.url}" width="328" height="100" />'
            )
        return ""

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
        ordering = ["is_active", "-created_at"]
