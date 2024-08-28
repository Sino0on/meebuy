from django.urls import path

# Authentication views
from apps.authentication.views import (
    HomeView,
    SelectUserTypeView,
    LogoutView,
    LoginView,
    SelectAuthUserTypeView,
    cabinet_create,
    activate,
    login_redirect, RegistrationView, AuthenticationView, register_v2
)
# Buyer views
from apps.buyer.views import (
    BuyerListView,
    BuyerDetailView,
    BuyerCategoryListView,
    BuyersStepView, TenderStepView
)
# Chat views
from apps.chat.views import (
    chat_detail,
    chats,
    create_chat,
    add_to_favorites,
    delete_chat,
    remove_from_favorites,
    remove_from_deleted
)
# Pages views
from apps.pages.views import (
    privacy_policy_view,
    rules_view,
    banner_view
)
# Product views
from apps.product.views import (
    ProductListView,
    ProductUpdateView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ExcelTemplateDownloadView,
    ExcelUploadView,
    AddNewCategoryRequestView,
    ProductCategoryUpdateView,
    ProductCategoryDeleteView,
    PriceColumnCreateView,
    PriceColumnUpdateView,
    PriceColumnDeleteView,
    DownloadPriceFileView,
    DeleteFileView
)
# Provider views
from apps.provider.views import (
    ProviderListView,
    ProviderDetailView,
    CategoryListView,
    ProviderCategoryListView,
    upload_file
)
# Tender views
from apps.tender.views import (
    TenderListView,
    TenderDetailView,
    delete_tender,
    TenderCreateView,
    TenderUpdateView,
    SearchRequestCreateView,
    SearchDetailView,
    SearchDeleteView
)
# User cabinet views
from apps.user_cabinet.api import (
    BuyStatusView,
    BuyUppingView
)
from apps.user_cabinet.views import (
    UserDetailView,
    UserSettingsView,
    UserAnketaView,
    UserAnketaBuyerView,
    BalanceView,
    TenderListCabinetView,
    ProductListCabinetView,
    CreateTenderView,
    FavoritesCabinetView,
    AnalyticCabinetView,
    TariffsCabinetView,
    change_avatar,
    change_image,
    change_password,
    reset_password,
    check_email,
    reset_password_confirm,
    password_change_success,
    send_message,
    send_message_logout,
    StatusListView,
    add_provider_fav_api,
    add_product_fav_api,
    add_tender_fav_api,
    add_buyer_fav_api,
    delete_provider_fav,
    delete_product_fav,
    delete_tender_fav,
    delete_buyer_fav,
    add_provider_fav,
    redirect_to_site,
    tariff_buy,
    delete_transaction,
    init_payment,
    freedompay_success,
    UppingListView
)

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('authentication/', AuthenticationView.as_view(), name='authentication'),
    path('register_v2/', register_v2, name='register_v2'),

    path('choice/', SelectUserTypeView.as_view(), name='choice'),
    path('select_user_type/', SelectUserTypeView.as_view(), name='select_user_type'),
    path('select_auth_user_type/', SelectAuthUserTypeView.as_view(), name='select_auth_user_type'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('login_redirect/', login_redirect, name='login_redirect'),
    path('buyer/step/', BuyersStepView.as_view(), name='buyer_step'),
    path('tender/step/', TenderStepView.as_view(), name='tender_step'),

    # Buyer
    path('buyer/list/', BuyerListView.as_view(), name='buyer_list'),
    path('buyer/list/<int:pk>/', BuyerCategoryListView.as_view(), name='buyer_category_list'),

    path('buyer/detail/<int:pk>/', BuyerDetailView.as_view(), name='buyer_detail'),

    # Chat
    path('chat/<str:pk>/', chat_detail, name='chat_detail'),
    path('chat/create/<str:pk>/', create_chat, name='chat_create'),
    path('chat_list/', chats, name='chat_list'),
    path('add_to_favorites/<int:chat_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:chat_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('delete_chat/<int:chat_id>/', delete_chat, name='delete_chat'),
    path('undelete_chat/<int:chat_id>/', remove_from_deleted, name='undelete_chat'),

    # Pages
    path('', HomeView.as_view(), name='home'),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy'),
    path('rules/', rules_view, name='rules'),
    path('bunner/', banner_view, name='bunner'),

    # Product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/download-excel/', ExcelTemplateDownloadView.as_view(), name='download_excel'),
    path('product/upload-products/', ExcelUploadView.as_view(), name='upload_products'),
    path('product/upload-excel/', ExcelUploadView.as_view(), name='upload_excel'),

    # Provider
    path('provider/list/', ProviderListView.as_view(), name='provider_list'),
    path('provider/detail/<int:pk>/', ProviderDetailView.as_view(), name='provider_detail'),
    path('provider/list/<int:pk>/', ProviderCategoryListView.as_view(), name='provider_category_list'),
    path('upload/', upload_file, name='upload_file'),
    path('download/', DownloadPriceFileView.as_view(), name='download_price_file'),
    path('delete_file/', DeleteFileView.as_view(), name='delete_file'),

    # Tender
    path('tender/list/', TenderListView.as_view(), name='tender_list'),
    path('tender/detail/<int:pk>/', TenderDetailView.as_view(), name='tender_detail'),
    path('tender/create/', TenderCreateView.as_view(), name='tender_create'),
    path('tender/update/<int:pk>/', TenderUpdateView.as_view(), name='tender_update'),
    path('tender/delete/<int:pk>/', delete_tender, name='delete_tender'),
    path('tender/create/search/request/', SearchRequestCreateView.as_view(), name='search_request_create'),
    path('search/detail/<int:pk>/', SearchDetailView.as_view(), name='search_detail'),
    path('search/delete/<int:pk>/', SearchDeleteView.as_view(), name='search_delete'),

    # User cabinet
    path('profile/create/cabinet/', cabinet_create),
    path('profile/', UserDetailView.as_view(), name='view_profile'),
    path('profile/settings/', UserSettingsView.as_view(), name='settings'),
    path('profile/anketa/', UserAnketaView.as_view(), name='anketa'),
    path('profile/anketa/buyer/', UserAnketaBuyerView.as_view(), name='anketa_buyer'),
    path('profile/balance/', BalanceView.as_view(), name='balance'),
    path('profile/tender/list/', TenderListCabinetView.as_view(), name='user_tenders'),
    path('profile/product/list/', ProductListCabinetView.as_view(), name='user_products'),
    path('profile/product/create/', ProductCreateView.as_view(), name='product_create'),
    path('profile/create/tender/', CreateTenderView.as_view(), name='create_tender'),
    path('profile/favorites/', FavoritesCabinetView.as_view(), name='favorites'),
    path('profile/analytic/', AnalyticCabinetView.as_view(), name='analytic'),
    path('profile/tariffs/', TariffsCabinetView.as_view(), name='tariffs'),
    path('change-avatar/', change_avatar, name='change_avatar'),
    path('change-image/', change_image, name='change_image'),
    path('change-password/', change_password, name='change_password'),
    path('reset_password/', reset_password, name='reset_password'),
    path('check_email/', check_email, name='check_email'),
    path('reset/<str:uidb64>/<str:token>/', reset_password_confirm, name='password_reset_confirm'),
    path('password-change-success/', password_change_success, name='password_change_success'),
    path('send-message/', send_message, name='send_message'),
    path('send-message-logout/', send_message_logout, name='send_message_logout'),

    # Favorites and API
    path('fav/provider/<int:pk>/', add_provider_fav_api, name='add_provider_fav_api'),
    path('fav/product/<int:pk>/', add_product_fav_api, name='add_product_fav_api'),
    path('fav/tender/<int:pk>/', add_tender_fav_api, name='add_tender_fav_api'),
    path('fav/buyer/<int:pk>/', add_buyer_fav_api, name='add_buyer_fav_api'),
    path('delete/fav/provider/<int:pk>/', delete_provider_fav, name='delete_provider_fav'),
    path('delete/fav/product/<int:pk>/', delete_product_fav, name='delete_product_fav'),
    path('delete/fav/tender/<int:pk>/', delete_tender_fav, name='delete_tender_fav'),
    path('delete/fav/buyer/<int:pk>/', delete_buyer_fav, name='delete_buyer_fav'),
    path('add_provider_favorite/<int:pk>/', add_provider_fav, name='add_provider_fav'),

    # Others
    path('status/list/', StatusListView.as_view(), name='status_list'),
    path('upping/list/', UppingListView.as_view(), name='upping_list'),
    path('status/buy/<int:pk>/', BuyStatusView.as_view(), name='buy_status'),
    path('upping/buy/<int:pk>/', BuyUppingView.as_view(), name='buy_upping'),
    path('redirect_to_site/<int:pk>/', redirect_to_site, name='redirect_to_site'),
    path('category/list/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('create-category/', AddNewCategoryRequestView.as_view(), name='create_category'),
    path('edit-category/<int:pk>/', ProductCategoryUpdateView.as_view(), name='edit_category'),
    path('delete-category/<int:pk>/', ProductCategoryDeleteView.as_view(), name='delete_category'),
    path('price-columns/create/', PriceColumnCreateView.as_view(), name='price_column_create'),
    path('price-columns/edit/<int:pk>/', PriceColumnUpdateView.as_view(), name='price_column_edit'),
    path('price-columns/delete/<int:pk>/', PriceColumnDeleteView.as_view(), name='price_column_delete'),

    # Payment and transactions
    path('connect_tariff/', tariff_buy, name='connect_tariff'),
    path('delete-transaction/<int:transaction_id>/', delete_transaction, name='delete_transaction'),
    path('init_payment/', init_payment, name='init_payment'),
    path('freedompay/success/', freedompay_success, name='freedompay_success'),
]
