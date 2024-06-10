from django.contrib import admin

from apps.pages.models import StaticPage


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    pass
