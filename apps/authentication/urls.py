from django.urls import path
from .views import HomeView, RegisterView, LoginView, SelectUserTypeView, LogoutView, ViewProfile, login_redirect

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('select_user_type/', SelectUserTypeView.as_view(), name='select_user_type'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ViewProfile.as_view(), name='view_profile'),
    path('login_redirect/', login_redirect, name='login_redirect'),
]
