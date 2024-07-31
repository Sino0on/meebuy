from django.contrib import admin

from apps.pages.models import StaticPage, TelegramBotToken


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    pass

@admin.register(TelegramBotToken)
class TelegramBotTokenAdmin(admin.ModelAdmin):
    pass
