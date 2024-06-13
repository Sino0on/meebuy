from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Provider


@receiver(post_save, sender=Provider)
def provider_moderation_signal(sender, instance, created, **kwargs):
    if not created and instance.is_modered:
        user_email = instance.user.email
        instance.comment = 'Вы успешно прошли модерацию, ваш аккаунт полностью активен.'
        subject = 'Поставщик прошел модерацию'
        message = render_to_string('providers/provider_moderation_email.html', {'provider': instance})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
