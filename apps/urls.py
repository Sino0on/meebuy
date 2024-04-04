from django.urls import path
from apps.product.views import ProductListView, ProductUpdateView, ProductCreateView, ProductDeleteView, \
    ProductDetailView
from apps.provider.views import ProviderListView, ProviderDetailView
from apps.authentication.views import LoginView
from apps.chat.views import chat_detail, chats
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from apps.authentication.views import HomeView, RegisterView, SelectUserTypeView, ViewProfile, LogoutView, LoginView

urlpatterns = [
    path('provider/list/', ProviderListView.as_view()),
    path('provider/detail/<int:id>', ProviderDetailView.as_view()),
    path('chat/<str:pk>/', chat_detail),
    path('chat_list/', chats),
    # path('', ProviderHomeListView.as_view()),
    path('change_password/', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),
    path('reset-password/', PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('select_user_type/', SelectUserTypeView.as_view(), name='select_user_type'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ViewProfile.as_view(), name='view_profile'),

    # products
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

]
