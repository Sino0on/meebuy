from django.urls import path
from apps.provider.views import ProviderListView, ProviderDetailView
from apps.authentication.views import LoginView
from apps.chat.views import chat_detail, chats
from apps.user_cabinet.views import UserStatusListView
from apps.user_cabinet.api import BuyStatusView


urlpatterns = [
    path('provider/list/', ProviderListView.as_view()),
    path('provider/detail/<int:id>', ProviderDetailView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('chat/<str:pk>/', chat_detail),
    path('chat_list/', chats),
    path('status/list/', UserStatusListView.as_view()),
    path('status/buy/<int:pk>', BuyStatusView.as_view())
]
