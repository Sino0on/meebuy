from django.urls import path

from apps.chat.consumers import ChatConsumers

websocket_urlpatterns = [
    path('ws/socket-server/chat/<str:pk>', ChatConsumers.as_asgi()),
]
