from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from apps.chat.models import Chat, Message
from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.user_cabinet.models import Contacts

User = get_user_model()

@login_required(login_url='login')
def chats(request):
    chat_rooms = Chat.objects.filter(models.Q(user_first=request.user) | models.Q(user_second=request.user))
    chat_details = []

    for chat in chat_rooms:
        messages = Message.objects.filter(chat=chat).order_by('-created_at')
        unread_count = messages.filter(is_read=False).exclude(sender=request.user).count()
        chat_details.append({
            'chat': chat,
            'last_message': messages.first(),
            'unread_count': unread_count
        })
    contacts = Contacts.load()

    return render(request, 'chat_list.html', {
        'chat_details': chat_details,
        'contacts': contacts
    })


@login_required(login_url='/login/')
def chat_detail(request, pk):
    chat = get_object_or_404(Chat, id=pk)
    messages = Message.objects.filter(chat=chat).order_by('created_at')
    unread_messages = messages.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)
    return render(request, 'chat.html', {'chat': chat, 'messages': messages})


def create_chat(request, pk):
    user = get_object_or_404(User, id=pk)

    # Проверяем, существует ли уже чат между этими двумя пользователями
    existing_chat = Chat.objects.filter(
        (Q(user_first=request.user) & Q(user_second=user)) |
        (Q(user_first=user) & Q(user_second=request.user))
    ).first()

    if existing_chat:
        # Если чат существует, редиректим к нему
        return redirect(f'/chat/{existing_chat.id}')

    # Если чата нет, создаем новый
    chat = Chat.objects.create(user_first=request.user, user_second=user)
    return redirect(f'/chat/{chat.id}')
