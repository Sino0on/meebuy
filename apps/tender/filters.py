import django_filters
from django.utils import timezone
from django.db.models import Q
from apps.tender.models import Tender, City, Country


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
    has_phone = django_filters.BooleanFilter(
        field_name='user__provider__phone',
        method='filter_by_phone',
        label='Наличие телефона'
    )

    country = django_filters.ModelChoiceFilter(
        field_name='user__provider__city__region__country',
        queryset=Country.objects.all(),
        label='Страна',
        method='filter_by_country'
    )
    city = django_filters.ModelChoiceFilter(
        field_name='user__provider__city',
        queryset=City.objects.all(),
        label='Город',
        method='filter_by_city'
    )

    def filter_title(self, queryset, name, value):
        search_term = value
        return queryset.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        )

    def filter_exclude(self, queryset, name, value):
        search_term = value
        return queryset.exclude(Q(title__icontains=search_term) | Q(description__icontains=search_term))

    def filter_by_order(self, queryset, name, value):
        if value == 'yesterday':
            start_date = timezone.now() - timezone.timedelta(days=1)
            return queryset.filter(created_at__date__gte=start_date.date())
        elif value == 'last_3_days':
            start_date = timezone.now() - timezone.timedelta(days=3)
            return queryset.filter(created_at__date__gte=start_date.date())
        elif value == 'last_week':
            start_date = timezone.now() - timezone.timedelta(days=7)
            return queryset.filter(created_at__date__gte=start_date.date())
        return queryset

    def filter_by_country(self, queryset, name, value):
        if value:
            print(f"Filtering by country: {value}")  # Отладочное сообщение
            return queryset.filter(user__provider__city__region__country=value)
        return queryset

    def filter_by_city(self, queryset, name, value):
        if value:
            print(f"Filtering by city: {value}")  # Отладочное сообщение
            return queryset.filter(user__provider__city=value)
        return queryset

    def filter_by_phone(self, queryset, name, value):
        if value is None:
            return queryset
        if value in [True, 'True', 'on']:
            return queryset.filter(user__provider__phone__isnull=False).exclude(user__provider__phone='')
        return queryset


    class Meta:
        model = Tender
        fields = ['title', 'ordering_date', 'exclude_words', 'price_from', 'price_to', 'country', 'city']
