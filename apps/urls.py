from django.urls import path
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from apps.provider.views import ProviderHomeListView
from apps.authentication.views import register, logout_view, home, view_profile, select_user_type, login


urlpatterns = [
    # path('', ProviderHomeListView.as_view()),
    path('', home),
    path('register/', register, name='register'),
    path('select_user_type/', select_user_type, name='select_user_type'),
    path('login/', login, name='login'),
    path('logout/', logout_view),
    path('change_password/', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('reset-password/', PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', view_profile, name='view_profile'),
]
