from django.urls import path
from apps.provider.views import ProviderHomeListView
from apps.authentication.views import LoginView


urlpatterns = [
    path('', ProviderHomeListView.as_view()),
    path('login/', LoginView.as_view(), name='login')
]
