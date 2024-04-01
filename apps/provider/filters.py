from django.db.models import Q

from apps.provider.models import Provider
import django_filters


class ProviderFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', method='filter_title')

    def filter_title(self, queryset, name, value):
        # print(len(queryset))
        search_term = value
        queryset = queryset.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        )
        print('title')
        return queryset

    class Meta:
        model = Provider
        fields = ['title', 'category', 'conditions', 'type_pay', 'deliveries']
