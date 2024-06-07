from django.db import models


class StatusMixin(models.Model):
    is_new = models.BooleanField(verbose_name="Новинка", default=False)
    is_recommended = models.BooleanField(verbose_name="Рекомендуемое", default=False)

    class Meta:
        abstract = True
