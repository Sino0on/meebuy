from django.utils import timezone

from django.db.models import Q

from apps.tender.models import Tender
import django_filters


class TenderFilter(django_filters.FilterSet):
    CHOICES = (
        ('all', 'Все время'),
        ('yesterday', 'Вчера'),
        ('last_3_days', 'Последние 3 дня'),
        ('last_week', 'Последняя неделя'),
    )

    ordering_date = django_filters.ChoiceFilter(label='Дата создания', choices=CHOICES, method='filter_by_order')
    title = django_filters.CharFilter(lookup_expr='icontains', method='filter_title')
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    exclude_words = django_filters.CharFilter(method='filter_exclude')

    def filter_title(self, queryset, name, value):
        search_term = value
        queryset = queryset.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        )
        return queryset

    def filter_exclude(self, queryset, name, value):
        search_term = value
        queryset = queryset.exclude(title=search_term)
        return queryset

    def filter_by_order(self, queryset, name, value):
        if value == 'yesterday':
            start_date = timezone.now() - timezone.timedelta(days=1)
            return queryset.filter(created_at__date=start_date.date())
        elif value == 'last_3_days':
            start_date = timezone.now() - timezone.timedelta(days=3)
            return queryset.filter(created_at__date__gte=start_date.date())
        elif value == 'last_week':
            start_date = timezone.now() - timezone.timedelta(days=7)
            return queryset.filter(created_at__date__gte=start_date.date())
        return queryset  # 'all' или неизвестное значение

    class Meta:
        model = Tender
        fields = ['title', 'ordering_date', 'exclude_words',
                  'price_from', 'price_to', 'country', 'region',
                  'region', 'city']
