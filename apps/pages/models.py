from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class StaticPage(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    description = RichTextField(verbose_name=_("Описание"))
    slug = models.SlugField(unique=True, verbose_name=_("Слоган"), blank=True, null=True)

    class Meta:
        verbose_name = _("Статическая страница")
        verbose_name_plural = _("Статические страницы")

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TelegramBotToken(models.Model):
    bot_token = models.CharField(max_length=200, unique=True, verbose_name=_("Телеграм Бот Токен"))
    report_channels = models.TextField(max_length=200, blank=True, null=True, verbose_name=_("Айди каналов"))

    def clean(self):
        if TelegramBotToken.objects.exists() and not self.pk:
            raise ValidationError(_('Может существовать только один экземпляр модели TelegramBotToken.'))

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "Токен бота Telegram"

    class Meta:
        verbose_name = _("Токен бота Telegram")
        verbose_name_plural = _("Токены бота Telegram")


class OurPartners(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    icon = models.FileField(upload_to="partners/", verbose_name=_("Иконка"))
    link = models.URLField(verbose_name=_("Ссылка"), blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name=_("Активен"))

    class Meta:
        verbose_name = _("Партнер")
        verbose_name_plural = _("Партнеры")

    def __str__(self):
        return f"{self.title}"
