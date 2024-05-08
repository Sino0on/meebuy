import django_filters
from apps.provider.models import Provider
from apps.tender.models import Category
from django.db.models import Q
from django.shortcuts import get_object_or_404


class ProviderFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', method='filter_title')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), method='filter_category')

    def filter_title(self, queryset, name, value):
        # print(len(queryset))
        search_term = value
        queryset = queryset.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        )
        print('title')
        return queryset

    def filter_category(self, queryset, name, value):
        categories = Category.get_category_descendants(get_object_or_404(Category, id=value))
        queryset = queryset.filter(category__in=categories)
        return queryset


    class Meta:
        model = Provider
        fields = ['title', 'category', 'type']
