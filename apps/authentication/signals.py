from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.user_cabinet.models import Cabinet


User = get_user_model()


@receiver(post_save, sender=User)
def create_user_cabinet(sender, instance, created, **kwargs):
    if created:
        Cabinet.objects.create(user=instance)
