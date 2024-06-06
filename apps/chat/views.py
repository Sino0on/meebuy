from apps.chat.models import Chat, Message
from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from apps.user_cabinet.models import Contacts

User = get_user_model()

@login_required(login_url='login')
def chats(request):
    chat_rooms = Chat.objects.filter(
        models.Q(user_first=request.user) | models.Q(user_second=request.user)
    )
    favorite_chats = chat_rooms.filter(is_favorite=True)
    deleted_chats = chat_rooms.filter(is_deleted=True)
    chat_details = []
    chat_deleted = []
    chat_favorite = []

    for chat in chat_rooms:
        messages = Message.objects.filter(chat=chat).order_by('-created_at')
        unread_count = messages.filter(is_read=False).exclude(sender=request.user).count()
        if not chat.is_deleted:
            chat_details.append({
                'chat': chat,
                'last_message': messages.first(),
                'unread_count': unread_count
            })
    for chat in deleted_chats:
        messages = Message.objects.filter(chat=chat).order_by('-created_at')
        unread_count = messages.filter(is_read=False).exclude(sender=request.user).count()
        chat_deleted.append({
            'chat': chat,
            'last_message': messages.first(),
            'unread_count': unread_count
        })
    for chat in favorite_chats:
        messages = Message.objects.filter(chat=chat).order_by('-created_at')
        unread_count = messages.filter(is_read=False).exclude(sender=request.user).count()
        if not chat.is_deleted:
            chat_favorite.append({
                'chat': chat,
                'last_message': messages.first(),
                'unread_count': unread_count
            })
    contacts = Contacts.load()

    return render(request, 'chat_list.html', {
        'chat_details': chat_details,
        'contacts': contacts,
        'favorite_chats': chat_favorite,
        'deleted_chats': chat_deleted
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


def add_to_favorites(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    # Здесь вы можете изменить атрибут модели для добавления в избранное
    chat.is_favorite = True
    chat.save()
    return redirect('chat_list')

def remove_from_favorites(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    # Здесь вы можете изменить атрибут модели для добавления в избранное
    chat.is_favorite = False
    chat.save()
    return redirect('chat_list')


def delete_chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    # Здесь вы можете изменить атрибут модели для удаления сообщения
    chat.is_deleted = True
    chat.save()
    return redirect('chat_list')


def remove_from_deleted(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    # Здесь вы можете изменить атрибут модели для удаления сообщения
    chat.is_deleted = False
    chat.save()
    print('asdasdad')
    return redirect('chat_list')
