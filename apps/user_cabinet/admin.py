from django.contrib import admin, messages
from apps.user_cabinet.models import Cabinet, Transaction, ActiveUserStatus, UserStatus, Status
from django.db.models.functions import TruncWeek, TruncMonth, TruncYear
from django.db.models import Count, Sum
from django.utils.translation import gettext as _


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'user_status')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(user__email__icontains=search_term)
        return queryset, use_distinct

    search_fields = ('user__email', )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(user__user__email__icontains=search_term)
        return queryset, use_distinct

    search_fields = ('user__user__email', )


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'price', 'days')
    list_filter = ('days', )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(status__title__icontains=search_term)
        return queryset, use_distinct

    search_fields = ('status__title', )


@admin.register(ActiveUserStatus)
class ActiveUserStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'is_active', 'end_date')
    list_filter = ('is_active', )


# @admin.register(Constants)
# class ConstantsAdmin(admin.ModelAdmin):
#     list_display = ('max_cabinets', 'days_color', 'days_vip', 'is_moder')
#
#     actions = ['moderate', 'unmoderate']
#
#     @admin.action(description=_('Включить режим модерации'))
#     def moderate(self, request, queryset):
#         queryset.update(is_moder=True)
#         self.message_user(request, _(f"Режим модерации включена!"))
#
#     @admin.action(description=_('Выключить режим модерации'))
#     def unmoderate(self, request, queryset):
#         queryset.update(is_moder=False)
#         self.message_user(request, _(f"Режим модерации выключена!"))


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'quantity_announce', 'discount', 'created_date')
    search_fields = ('title', )
