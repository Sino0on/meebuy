from django.urls import path

from apps.product.views import ProductListView, ProductUpdateView, ProductCreateView, ProductDeleteView, \
    ProductDetailView
from apps.provider.views import ProviderListView, ProviderDetailView
from apps.authentication.views import LoginView
from apps.chat.views import chat_detail, chats


urlpatterns = [
    path('provider/list/', ProviderListView.as_view()),
    path('provider/detail/<int:id>', ProviderDetailView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('chat/<str:pk>/', chat_detail),
    path('chat_list/', chats),

    # products
    path('products', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
