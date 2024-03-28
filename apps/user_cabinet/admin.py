from django.contrib import admin, messages
from apps.user_cabinet.models import Cabinet, Transaction, ActiveUserStatus, UserStatus, Promocode, Constants, Status, \
    Payment, VipStatus, IsColored, Ban
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


@admin.register(Ban)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ipaddress', )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(user__user__email__icontains=search_term)
        return queryset, use_distinct

    search_fields = ('user__user__email', 'ipaddress')


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


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'money', 'user_status', 'is_active')
    search_fields = ('code', )
    list_filter = ('is_active', )


@admin.register(Constants)
class ConstantsAdmin(admin.ModelAdmin):
    list_display = ('max_cabinets', 'days_color', 'days_vip', 'is_moder')

    actions = ['moderate', 'unmoderate']

    @admin.action(description=_('Включить режим модерации'))
    def moderate(self, request, queryset):
        queryset.update(is_moder=True)
        self.message_user(request, _(f"Режим модерации включена!"))

    @admin.action(description=_('Выключить режим модерации'))
    def unmoderate(self, request, queryset):
        queryset.update(is_moder=False)
        self.message_user(request, _(f"Режим модерации выключена!"))


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'quantity_announce', 'discount', 'created_date')
    search_fields = ('title', )


@admin.register(VipStatus)
class VipStatusAdmin(admin.ModelAdmin):
    list_display = ('end_date', 'is_active')


@admin.register(IsColored)
class IsColoredAdmin(admin.ModelAdmin):
    list_display = ('end_date', 'is_active')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('cost', 'cabinet', 'is_paid')
    list_filter = ('is_paid', )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(cabinet__user__email__icontains=search_term)
        return queryset, use_distinct

    search_fields = ('cabinet__user__email', )

    actions = ['weekly_report', 'monthly_report', 'yearly_report']

    @admin.action(description=_("Недельный отчет"))
    def weekly_report(self, request, queryset):
        report = queryset.annotate(week=TruncWeek('created_date')).values('week').annotate(count=Count('id'),
                                                                                           total=Sum('cost')).order_by('week')

        formatted_report = "\n".join(
            _(f"Неделя {item['week'].date()}: {item['count']} платежи, Итого: {item['total']}")
            for item in report
        )

        self.message_user(request, _(f"Недельный отчет:\n{formatted_report}"))

    @admin.action(description=_("Месячный отчет"))
    def monthly_report(self, request, queryset):
        # Группировка и подсчет платежей по месяцам
        report = queryset.annotate(month=TruncMonth('created_date')).values('month').annotate(count=Count('id'),
                                                                                              total=Sum('cost')).order_by('month')
        formatted_report = "\n".join(
            _(f"Месяц {item['month'].date()}: {item['count']} платежи, Итого: {item['total']}")
            for item in report
        )
        self.message_user(request, _(f"Месячный отчет: \n{formatted_report}"))

    @admin.action(description=_("Годовой отчет"))
    def yearly_report(self, request, queryset):
        # Группировка и подсчет платежей по годам
        report = queryset.annotate(year=TruncYear('created_date')).values('year').annotate(count=Count('id'),
                                                                                           total=Sum('cost')).order_by('year')
        formatted_report = "\n".join(
            _(f"Годовые  {item['year'].date()}: {item['count']} платежи, Итого: {item['total']}")
            for item in report
        )
        self.message_user(request, _(f"Годовой отчет: {formatted_report}"))

    weekly_report.short_description = _("Недельный отчет")
    monthly_report.short_description = _("Месячный отчет")
    yearly_report.short_description = _("Годовой отчет")
