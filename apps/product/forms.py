from django import forms
from django.forms import modelformset_factory

from .models import Product, ProductCategory, PriceColumn


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'phone']


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(label='Excel файл', required=False)



class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'parent',]


class PriceColumnForm(forms.ModelForm):
    class Meta:
        model = PriceColumn
        fields = ['name', 'formula', 'min_order_amount']

# PriceColumnFormSet = modelformset_factory(PriceColumn, form=PriceColumnForm, extra=1)
