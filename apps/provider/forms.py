from django import forms
from .models import PriceFiles


class PriceFilesForm(forms.ModelForm):
    class Meta:
        model = PriceFiles
        fields = ['image']
