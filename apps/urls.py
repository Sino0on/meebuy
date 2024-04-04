from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from apps.authentication.views import HomeView, RegisterView, SelectUserTypeView, ViewProfile, LogoutView, LoginView, login_redirect
from apps.provider.views import ProviderHomeListView


urlpatterns = [
    # path('', ProviderHomeListView.as_view()),
    path('change_password/', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('reset-password/', PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('select_user_type/', SelectUserTypeView.as_view(), name='select_user_type'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ViewProfile.as_view(), name='view_profile'),
    path('login_redirect/', login_redirect, name='login_redirect'),
]
