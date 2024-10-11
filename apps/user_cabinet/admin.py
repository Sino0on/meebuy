from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from apps.user_cabinet.models import (
    Cabinet,
    Transaction,
    ActiveUserStatus,
    PackageStatus,
    Status,
    Upping,
    ActiveUpping,
    SupportMessage,
    Contacts,
    FAQ
)


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'user_status')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(user__email__icontains=search_term)
        return queryset, use_distinct

    search_fields = ('user__email',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'total',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(user__user__email__icontains=search_term)
        return queryset, use_distinct

    search_fields = ('user__user__email',)


@admin.register(PackageStatus)
class PackageStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'price', 'months')
    list_filter = ('months',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(status__title__icontains=search_term)
        return queryset, use_distinct

    search_fields = ('status__title',)


@admin.register(ActiveUserStatus)
class ActiveUserStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'is_active', 'end_date')
    list_filter = ('is_active',)


# @admin.register(Constants)
# class ConstantsAdmin(admin.ModelAdmin):
#     list_display = ('max_cabinets', 'days_color', 'days_vip', 'is_moder')
#
#     actions = ['moderate', 'unmoderate']
#
#     @admin.action(description=_('Включить режим модерации'))
#     def moderate(self, request, queryset):
#     def moderate(self, request, queryset):
#         queryset.update(is_moder=True)
#         self.message_user(request, _(f"Режим модерации включена!"))
#
#     @admin.action(description=_('Выключить режим модерации'))
#     def unmoderate(self, request, queryset):
#         queryset.update(is_moder=False)
#         self.message_user(request, _(f"Режим модерации выключена!"))


@admin.register(Status)
class StatusAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'title', 'created_date', )
    search_fields = ('title',)
    ordering = ('order',)


@admin.register(Upping)
class UppingAdmin(admin.ModelAdmin):
    list_display = ('days', 'price')
    # search_fields = ('da', )


@admin.register(ActiveUpping)
class ActiveUppingAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'end_date')
    search_fields = ('is_active',)


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message', 'agree_to_policy', 'regret_to_register', 'created_at')


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('instagram', 'whatsapp', 'telegram', 'vk', 'phone')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question', 'answer')
