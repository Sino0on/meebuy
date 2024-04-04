from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('dev-admin8/', admin.site.urls),
    path('', include('apps.urls')),
    path('accounts/', include('allauth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
