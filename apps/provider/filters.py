import django_filters
from django import forms
from apps.provider.models import Provider, Category
from apps.tender.models import City, Country, Region


class ProviderFilter(django_filters.FilterSet):
    ORDER_CHOICES = [
        ('name', 'Имя (A-Z)'),
        ('-name', 'Имя (Z-A)'),
        ('created_at', 'Дата добавления (сначала новые)'),
        ('-created_at', 'Дата добавления (сначала старые)'),
    ]

    order_by = django_filters.ChoiceFilter(label='Сортировка', choices=ORDER_CHOICES, method='filter_by_order')

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Имя',
                                      method='filter_by_title_and_keywords')
    country = django_filters.CharFilter(label='Страна', method='filter_by_country')
    region = django_filters.CharFilter(label='Регион', method='filter_by_region')
    city = django_filters.CharFilter(label='Город', method='filter_by_city')

    large_wholesale = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Крупный опт',
                                                   method='filter_boolean_field')
    small_wholesale = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Мелкий опт',
                                                   method='filter_boolean_field')
    retail = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Поштучно', method='filter_boolean_field')

    # Conditions
    installment = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Возможна рассрочка',
                                               method='filter_boolean_field')
    credit = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Возможен кредит',
                                          method='filter_boolean_field')
    deposit = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Возможен депозит',
                                           method='filter_boolean_field')
    consignment = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Возможна передача под реализацию',
                                               method='filter_boolean_field')
    dropshipping = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Возможен дропшиппинг',
                                                method='filter_boolean_field')
    showroom = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Есть шоурум',
                                            method='filter_boolean_field')
    marketplace_sale = django_filters.BooleanFilter(widget=forms.CheckboxInput,
                                                    label='Разрешена продажа на маркетплейсах',
                                                    method='filter_boolean_field')

    # Deliveries
    pickup = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Самовывоз', method='filter_boolean_field')
    transport_company = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Транспортной компанией',
                                                     method='filter_boolean_field')
    by_car = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Автомобилем',
                                          method='filter_boolean_field')
    air_transport = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Авиатранспортом',
                                                 method='filter_boolean_field')
    rail_transport = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Железной дорогой',
                                                  method='filter_boolean_field')
    courier = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Курьером', method='filter_boolean_field')

    # Payment Types
    cash = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Наличными', method='filter_boolean_field')
    bank_transfer = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Безналичная оплата',
                                                 method='filter_boolean_field')
    credit_card = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Кредитные карты',
                                               method='filter_boolean_field')
    electronic_money = django_filters.BooleanFilter(widget=forms.CheckboxInput, label='Электронные деньги',
                                                    method='filter_boolean_field')
    category = django_filters.CharFilter(label='Категория', method='filter_by_category')

    class Meta:
        model = Provider
        fields = [
            'title',
            'country',
            'region',
            'city',
            'large_wholesale',
            'small_wholesale',
            'retail',
            'installment',
            'credit',
            'deposit',
            'consignment',
            'dropshipping',
            'showroom',
            'marketplace_sale',
            'pickup',
            'transport_company',
            'by_car',
            'air_transport',
            'rail_transport',
            'courier',
            'cash',
            'bank_transfer',
            'credit_card',
            'electronic_money',
            'order_by',
        ]

    def filter_by_country(self, queryset, name, value):
        if value:
            try:
                country = Country.objects.get(title=value)
                return queryset.filter(user__provider__city__region__country=country.id)
            except Country.DoesNotExist:
                return queryset.none()
        return queryset

    def filter_by_region(self, queryset, name, value):
        if value:
            try:
                region = Region.objects.get(title=value)
                return queryset.filter(user__provider__city__region=region.id)
            except Region.DoesNotExist:
                return queryset.none()
        return queryset

    def filter_by_city(self, queryset, name, value):
        if value:
            try:
                city = City.objects.get(title=value)
                return queryset.filter(user__provider__city=city.id)
            except City.DoesNotExist:
                return queryset.none()
        return queryset

    def filter_by_title_and_keywords(self, queryset, name, value):
        if value:
            keywords = [k.strip() for k in value.split(',')]
            query = queryset.filter(title__icontains=value)
            for keyword in keywords:
                query |= queryset.filter(keywords__icontains=keyword)
            return query.distinct()
        return queryset

    def filter_boolean_field(self, queryset, name, value):
        if value is None:
            return queryset
        if value in [True, 'True', 'on']:
            return queryset.filter(**{name: True})
        return queryset

    def filter_by_order(self, queryset, name, value):
        if value:
            return queryset.order_by(value)
        return queryset

    def filter_by_category(self, queryset, name, value):
        if value:
            try:
                category = Category.objects.get(title=value)
                return queryset.filter(category=category)
            except Category.DoesNotExist:
                return queryset.none()
        return queryset