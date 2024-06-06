from django.db import models
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    user_first = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='chats')
    user_second = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='second_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False, blank=True)  # Добавлено для избранных сообщений
    is_deleted = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.user_first} {self.user_second}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-created_at']


class Message(models.Model):
    content = models.CharField(max_length=250)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    is_read = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content[:10]} - {self.sender}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщении'
        ordering = ['-created_at']

    @staticmethod
    def get_count_for_today(sender):
        today = datetime.now().date()
        return Message.objects.filter(sender=sender, created_at__date=today).count()

    @staticmethod
    def get_count_for_yesterday(sender):
        yesterday = datetime.now().date() - timedelta(days=1)
        return Message.objects.filter(sender=sender, created_at__date=yesterday).count()

    @staticmethod
    def get_count_for_month(sender):
        today = datetime.now()
        return Message.objects.filter(
            sender=sender,
            created_at__year=today.year,
            created_at__month=today.month
        ).count()

    @staticmethod
    def get_count_for_year(sender):
        today = datetime.now()
        return Message.objects.filter(
            sender=sender,
            created_at__year=today.year
        ).count()

    @staticmethod
    def get_count_for_today_recipient(recipient):
        today = datetime.now().date()
        return Message.objects.filter(
            created_at__date=today
        ).exclude(
            sender=recipient
        ).filter(
            Q(chat__user_first=recipient) | Q(chat__user_second=recipient)
        ).count()

    @staticmethod
    def get_count_for_yesterday_recipient(recipient):
        yesterday = datetime.now().date() - timedelta(days=1)
        return Message.objects.filter(
            created_at__date=yesterday
        ).exclude(
            sender=recipient
        ).filter(
            Q(chat__user_first=recipient) | Q(chat__user_second=recipient)
        ).count()

    @staticmethod
    def get_count_for_month_recipient(recipient):
        today = datetime.now()
        return Message.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month
        ).exclude(
            sender=recipient
        ).filter(
            Q(chat__user_first=recipient) | Q(chat__user_second=recipient)
        ).count()

    @staticmethod
    def get_count_for_year_recipient(recipient):
        today = datetime.now()
        return Message.objects.filter(
            created_at__year=today.year
        ).exclude(
            sender=recipient
        ).filter(
            Q(chat__user_first=recipient) | Q(chat__user_second=recipient)
        ).count()
