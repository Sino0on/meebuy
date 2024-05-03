from django.urls import path
from apps.product.views import ProductListView, ProductUpdateView, ProductCreateView, ProductDeleteView, \
    ProductDetailView, ExcelTemplateDownloadView, ExcelUploadView
from apps.provider.views import ProviderListView, ProviderDetailView
from apps.authentication.views import LoginView
from apps.chat.views import chat_detail, chats
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


from apps.authentication.views import HomeView, RegisterView, SelectUserTypeView, ViewProfile, LogoutView, LoginView, login_redirect

from apps.authentication.views import HomeView, RegisterView, SelectUserTypeView, ViewProfile, LogoutView, LoginView
from apps.tender.views import TenderListView, TenderDetailView
from apps.user_cabinet.views import UserStatusListView, UppingListView
from apps.user_cabinet.api import BuyStatusView, BuyUppingView


urlpatterns = [
    path('provider/list/', ProviderListView.as_view()),
    path('provider/detail/<int:pk>/', ProviderDetailView.as_view()),
    path('chat/<str:pk>/', chat_detail),
    path('chat_list/', chats),
    # path('', ProviderHomeListView.as_view()),
    path('change_password/', PasswordChangeView.as_view(template_name='auth/change_password.html'), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'),
         name='password_change_done'),
    path('reset-password/', PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('select_user_type/', SelectUserTypeView.as_view(), name='select_user_type'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ViewProfile.as_view(), name='view_profile'),
    path('login_redirect/', login_redirect, name='login_redirect'),

    # products
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/download-excel/', ExcelTemplateDownloadView.as_view(), name='download_excel'),
    path('product/upload-products/', ExcelUploadView.as_view(), name='upload_products'),
    path('product/upload-excel/', ExcelUploadView.as_view(), name='upload_excel'),

    # tenders
    path('tender/list/', TenderListView.as_view(), name='tender_list'),
    path('tender/detail/<int:pk>/', TenderDetailView.as_view(), name='tender_detail'),

    path('status/list/', UserStatusListView.as_view()),
    path('upping/list/', UppingListView.as_view()),
    path('status/buy/<int:pk>', BuyStatusView.as_view()),
    path('upping/buy/<int:pk>', BuyUppingView.as_view())

]
