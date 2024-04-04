from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    user_first = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='chats')
    user_second = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='second_chats')
    created_at = models.DateTimeField(auto_now_add=True)

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
