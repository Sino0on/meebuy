from django import forms
from apps.tender.models import Tender


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
                  'price', 'currency', 'place_of_sale', 'quantity']
