import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['title', 'price_min', 'price_max', 'category']
