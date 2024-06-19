from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.translation import gettext as _, ngettext

from apps.authentication.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
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
        self.message_user(request, _(f"Учетная запись разблокирована!"))

    @admin.action(description=_('Количество активных пользователей'))
    def count_user(self, request, queryset):
        active_users_count = queryset.filter(is_active=True).count()
        total_users_count = queryset.count()  # Подсчет общего количества пользователей

        message = ngettext(
            "Найден %(active_count)d активный пользователь из %(total_count)d.",
            "Найдено %(active_count)d активных пользователей из %(total_count)d.",
            active_users_count,
        ) % {'active_count': active_users_count, 'total_count': total_users_count}
        self.message_user(request, message)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ]
        return custom_urls + urls

    def user_change_password(self, request, id, form_url=''):
        user = self.get_object(request, id)
        if request.method == 'POST':
            form = AdminPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin:apps_authentication_user_changelist')
        else:
            form = AdminPasswordChangeForm(user)

        context = {
            'form': form,
            'title': _('Change password: {}'.format(user.username)),
        }

        return render(request, 'admin/auth/user/change_password.html', context)
