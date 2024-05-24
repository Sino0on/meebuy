from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'phone']


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(label='Excel файл')