from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from apps.pages.models import StaticPage, TelegramBotToken, FooterLink, FooterColumn, ProfileHelpText


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    pass

@admin.register(TelegramBotToken)
class TelegramBotTokenAdmin(admin.ModelAdmin):
    pass

@admin.register(FooterColumn)
class FooterColumnAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
@admin.register(FooterLink)
class FooterLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    fields = ['title', 'column', 'link', 'order']
    list_filter = ['column']


@admin.register(ProfileHelpText)
class ProfileHelpTextAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass