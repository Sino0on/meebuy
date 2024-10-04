from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from apps.authentication.views import my_custom_callback_view

urlpatterns = [
                  path("__debug__/", include("debug_toolbar.urls")),
                  path('admin/', admin.site.urls),
                  path('', include('apps.urls')),
                  path('accounts/google/login/callback/', my_custom_callback_view, name='google_callback'),

                  re_path(r'^accounts/login/$', RedirectView.as_view(pattern_name='login', permanent=False)),
                  path('accounts/', include('allauth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
