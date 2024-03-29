from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('dev-admin8/', admin.site.urls),
    # path('social-auth/', include('social.apps.django_app.urls', namespace='social')),
    # path('auth/', include('apps.authentication.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
