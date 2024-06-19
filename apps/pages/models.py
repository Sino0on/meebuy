from ckeditor.fields import RichTextField

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
