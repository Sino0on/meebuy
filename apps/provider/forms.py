from django import forms

from .models import PriceFiles


class PriceFilesForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = PriceFiles
        fields = ['file']
