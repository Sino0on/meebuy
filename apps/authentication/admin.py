from django.contrib import admin
from apps.authentication.models import User
from django.utils.translation import gettext as _
from django.utils.translation import ngettext


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'auth_provider', 'is_staff', 'is_active', 'is_confirm')
    search_fields = ('email', 'first_name', 'last_name', )
    list_filter = ('is_staff', 'is_active', 'is_confirm', )

    actions = ['ban_user', 'unban_user', 'count_user']

    @admin.action(description=_('Заблокировать учетную запись'))
    def ban_user(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _(f"Учетная запись заблокирована!"))

    @admin.action(description=_('Разблокировать учетную запись'))
    def unban_user(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _(f"Учетная разблокирована!"))

    @admin.action(description=_('Количество активных пользователей'))
    def count_user(self, request, queryset):
        active_users_count = queryset.filter(is_active=True).count()
        total_users_count = queryset.count()  # Подсчет общего количества пользователей

        message = ngettext(
            "Найдено %(active_count)d активные пользователи из %(total_count)d.",
            "Найдено %(active_count)d активных пользователей из %(total_count)d.",
            active_users_count,
        ) % {'active_count': active_users_count, 'total_count': total_users_count}
        self.message_user(request, message)
