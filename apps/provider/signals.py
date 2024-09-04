from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Provider

@receiver(pre_save, sender=Provider)
def capture_previous_state(sender, instance, **kwargs):
    # Проверяем, существует ли уже запись в базе данных
    if instance.pk:
        # Загружаем предыдущее состояние из базы данных
        previous = sender.objects.get(pk=instance.pk)
        instance._previous_moderation_state = previous.is_modered
    else:
        instance._previous_moderation_state = None


@receiver(post_save, sender=Provider)
def provider_moderation_signal(sender, instance, created, **kwargs):
    # Проверяем, что запись не новая и что состояние изменилось с False на True
    if not created and getattr(instance, '_previous_moderation_state', None) == False and instance.is_modered:
        user_email = instance.user.email
        instance.comment = 'Вы успешно прошли модерацию, ваш аккаунт полностью активен.'
        subject = 'Поставщик прошел модерацию'
        message = render_to_string('providers/provider_moderation_email.html', {'provider': instance})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])