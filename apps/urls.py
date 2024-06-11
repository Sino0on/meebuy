from django.urls import path
from apps.product.views import ProductListView, ProductUpdateView, ProductCreateView, ProductDeleteView, \
    ProductDetailView, ExcelTemplateDownloadView, ExcelUploadView, ProductCategoryCreateView, ProductCategoryUpdateView, \
    ProductCategoryDeleteView, PriceColumnCreateView, PriceColumnUpdateView, PriceColumnDeleteView
from apps.provider.views import ProviderListView, ProviderDetailView, CategoryListView, upload_file
from apps.user_cabinet.views import *

from apps.pages.views import privacy_policy_view, rules_view

from apps.authentication.views import LoginView, SelectAuthUserTypeView, cabinet_create, activate

from apps.chat.views import chat_detail, chats, create_chat, add_to_favorites, delete_chat, remove_from_favorites, remove_from_deleted

from apps.authentication.views import (HomeView, SelectUserTypeView, ViewProfile, LogoutView, LoginView, login_redirect,
                                       )


from apps.authentication.views import HomeView, SelectUserTypeView, LogoutView, LoginView
from apps.tender.views import TenderListView, TenderDetailView, delete_tender, TenderCreateView, TenderUpdateView
from apps.user_cabinet.views import UserStatusListView, UppingListView
from apps.buyer.views import BuyerListView, BuyerDetailView
from apps.user_cabinet.api import BuyStatusView, BuyUppingView


urlpatterns = [
    path('provider/list/', ProviderListView.as_view(), name='provider_list'),
    path('provider/detail/<int:pk>/', ProviderDetailView.as_view(), name='provider_detail'),
    path('upload/', upload_file, name='upload_file'),
    path('chat/<str:pk>/', chat_detail, name='chat_detail'),
    path('chat/create/<str:pk>/', create_chat, name='chat_create'),
    path('chat_list/', chats, name='chat_list'),
    path('add_to_favorites/<int:chat_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:chat_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('delete_chat/<int:chat_id>/', delete_chat, name='delete_chat'),
    path('undelete_chat/<int:chat_id>/', remove_from_deleted, name='undelete_chat'),

    # path('', ProviderHomeListView.as_view()),
    path('', HomeView.as_view(), name='home'),


    path('login/', LoginView.as_view(), name='login'),
    path('choice/', SelectUserTypeView.as_view(), name='choice'),
    path('select_user_type/', SelectUserTypeView.as_view(), name='select_user_type'),
    path('select_auth_user_type/', SelectAuthUserTypeView.as_view(), name='select_auth_user_type'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserDetailView.as_view(), name='view_profile'),
    path('profile/settings/', UserSettingsView.as_view(), name='settings'),
    path('profile/anketa/', UserAnketaView.as_view(), name='anketa'),
    path('profile/anketa/buyer/', UserAnketaBuyerView.as_view(), name='anketa_buyer'),

    path('profile/balance/', BalanceView.as_view(), name='balance'),
    path('profile/tender/list/', TenderListCabinetView.as_view(), name='user_tenders'),
    path('profile/product/list/', ProductListCabinetView.as_view(), name='user_products'),
    path('profile/product/create/', ProductCreateView.as_view(), name='product_create'),

    path('profile/create/tender/', CreateTenderView.as_view(), name='create_tender'),
    path('profile/create/cabinet/', cabinet_create),
    path('profile/favorites/', FavoritesCabinetView.as_view(), name='favorites'),
    path('profile/analytic/', AnalyticCabinetView.as_view(), name='analytic'),
    path('profile/tariffs/', TariffsCabinetView.as_view(), name='tariffs'),
    path('login_redirect/', login_redirect, name='login_redirect'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),

    path('change-avatar/', change_avatar),
    path('change-image/', change_image),
    path('change-password/', change_password, name='change_password'),
    path('reset_password/', reset_password, name='reset_password'),
    path('check_email/', check_email, name='check_email'),
    path('reset/<str:uidb64>/<str:token>/', reset_password_confirm, name='password_reset_confirm'),
    path('password-change-success/', password_change_success, name='password_change_success'),
    path('send-message/', send_message, name='send_message'),
    path('send-message-logout/', send_message_logout, name='send_message_logout'),


    path('buyer/list/', BuyerListView.as_view(), name='buyer_list'),
    path('buyer/detail/<int:pk>/', BuyerDetailView.as_view(), name='buyer_detail'),

    # products
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/download-excel/', ExcelTemplateDownloadView.as_view(), name='download_excel'),
    path('product/upload-products/', ExcelUploadView.as_view(), name='upload_products'),
    path('product/upload-excel/', ExcelUploadView.as_view(), name='upload_excel'),

    # tenders
    path('tender/list/', TenderListView.as_view(), name='tender_list'),
    path('tender/detail/<int:pk>/', TenderDetailView.as_view(), name='tender_detail'),
    path('tender/create/', TenderCreateView.as_view(), name='tender_create'),
    path('tender/update/<int:pk>', TenderUpdateView.as_view(), name='tender_update'),
    path('tender/delete/<int:pk>/', delete_tender, name='delete_tender'),

    path('status/list/', StatusListView.as_view()),
    path('upping/list/', UppingListView.as_view()),
    path('status/buy/<int:pk>', BuyStatusView.as_view()),
    path('upping/buy/<int:pk>', BuyUppingView.as_view()),


    path('fav/provider/<int:pk>/', add_provider_fav_api),
    path('fav/product/<int:pk>/', add_product_fav_api),
    path('fav/tender/<int:pk>/', add_tender_fav_api),
    path('fav/buyer/<int:pk>/', add_buyer_fav_api),

    path('delete/fav/provider/<int:pk>/', delete_provider_fav),
    path('add_provider_favorite/<int:pk>/', add_provider_fav),

    # user
    path('user/', UserDetailView.as_view()),
    path('redirect_to_site/<int:pk>/', redirect_to_site),

    # apis
    path('category/list/<int:pk>', CategoryListView.as_view()),

  
    path('create-category/', ProductCategoryCreateView.as_view(), name='create_category'),
    path('edit-category/<int:pk>/', ProductCategoryUpdateView.as_view(), name='edit_category'),
    path('delete-category/<int:pk>/', ProductCategoryDeleteView.as_view(), name='delete_category'),

    path('price-columns/create/', PriceColumnCreateView.as_view(), name='price_column_create'),
    path('price-columns/edit/<int:pk>/', PriceColumnUpdateView.as_view(), name='price_column_edit'),
    path('price-columns/delete/<int:pk>/', PriceColumnDeleteView.as_view(), name='price_column_delete'),

    path('connect_tariff', tariff_buy),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy'),
    path('rules/', rules_view, name='rules'),

    path('init_payment/', init_payment, name='init_payment'),
    path('check_payment/', check_payment_status, name='init_payment'),
    path('freedompay/success/', freedompay_success, name='freedompay_success')
]
