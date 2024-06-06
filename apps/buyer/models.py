from django.db import models
from django.contrib.auth import get_user_model
from apps.tender.models import City, Category
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Buyer(models.Model):
    title = models.CharField(max_length=123, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mini_desc = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True)
    image = models.ImageField(upload_to='images/avatars/buyer/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=123, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['-created_at']


class BuyerImg(models.Model):
    image = models.ImageField(upload_to='images/buyer/%Y/%m/')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.buyer.title}'

    class Meta:
        verbose_name = _("Изображение Продавца")
        verbose_name_plural = _("Изображения Продавца")


class BuyerFiles(models.Model):
    image = models.ImageField(upload_to='images/providers/%Y/%m/')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _("Файл Продавца")
        verbose_name_plural = _("Файлы Продавца")
