import django_filters
from apps.product.models import Product, Category
from django.db.models import Q


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', method='filter_title')
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

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
        model = Product
        fields = ['title', 'price_min', 'price_max', 'category']
