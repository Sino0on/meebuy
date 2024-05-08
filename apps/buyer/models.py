from django.db import models
from django.contrib.auth import get_user_model
from apps.tender.models import City, Category

User = get_user_model()


class Buyer(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='images/avatars/buyer/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    phone = models.CharField(max_length=123)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['-created_at']

