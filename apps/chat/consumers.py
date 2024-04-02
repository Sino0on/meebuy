import datetime
import json
from pprint import pprint
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from apps.chat.models import Message, Chat
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()

class ChatConsumers(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["pk"]
        print(self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user"]
        user = get_object_or_404(User, id=user_id)
        chat = get_object_or_404(Chat, id=int(self.room_group_name))
        # print(self.__dict__)
        Message(sender=user, chat=chat, content=message).save()
        text_data_json['user'] = get_object_or_404(User, id=int(text_data_json['user'])).email
        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'text': text_data_json
                })

    def chat_message(self, event):
        pprint(self.scope['user'].id)
        messages = Message.objects.filter(chat__id=self.room_group_name).order_by('created_at')
        unread_messages = messages.filter(is_read=False).exclude(sender=self.scope['user'])
        unread_messages.update(is_read=True)
        self.send(text_data=json.dumps(
            {
                'type': 'chat',
                'message': event['text']
            }
        ))