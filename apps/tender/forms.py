from django import forms

from apps.tender.models import Tender, SearchRequest


class TenderForm(forms.ModelForm):
    period = forms.IntegerField(
        label='Количество дней',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Например: 30'}),
        required=False
    )

    class Meta:
        model = Tender
        fields = ['title', 'phone', 'description',
                  'email', 'period', 'requirements',
                  'price', 'currency', 'place_of_sale', 'quantity',
                  'retail_store',
                  'marketplaces',
                  'online_store',
                  'social_networks',
                  'wholesale_resale',
                  'group_purchases',
                  'for_personal_use',
                  'purchase_frequency',
                  'large_wholesale',
                  'small_wholesale',
                  'retail',
                  'official_distributor',
                  ]


class SearchRequestForm(forms.ModelForm):
    class Meta:
        model = SearchRequest
        fields = ['name', 'city']
