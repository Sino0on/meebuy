import django_filters
from apps.product.models import Product
from apps.tender.models import Category, Country, City, Region
from django.db.models import Q
from django.shortcuts import get_object_or_404


class BuyerFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', method='filter_title')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), method='filter_category')
    country = django_filters.CharFilter(
        label='Страна',
        method='filter_by_country'
    )
    region = django_filters.CharFilter(
        label='Регион',
        method='filter_by_region'
    )
    city = django_filters.CharFilter(
        label='Город',
        method='filter_by_city'
    )

    def filter_title(self, queryset, name, value):
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

    def filter_by_country(self, queryset, name, value):
        if value:
            print(value)
            try:
                country = Country.objects.get(title=value)
                return queryset.filter(provider__city__region__country=country.id)
            except Country.DoesNotExist:
                return queryset.none()
        return queryset

    def filter_by_region(self, queryset, name, value):
        if value:
            try:
                country = Region.objects.get(title=value)
                return queryset.filter(user__provider__city__region=country.id)
            except Country.DoesNotExist:
                return queryset.none()
        return queryset

    def filter_by_city(self, queryset, name, value):
        if value:
            print(value)
            try:
                city = City.objects.get(title=value)
                return queryset.filter(provider__city=city.id)
            except City.DoesNotExist:
                return queryset.none()
        return queryset

    class Meta:
        model = Product
        fields = ['title', 'category', 'city', 'region', 'country']
