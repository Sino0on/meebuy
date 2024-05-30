from django import forms
from django.forms import modelformset_factory

from .models import Product, ProductCategory, PriceColumn


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'mini_desc',
            'type',
            'manufacturer',
            'price',
            'currency',
            'min_quantity',
            'category',
            'phone',
            'terms_of_sale',
            'country_of_manufacture',
            'characterization',
            'product_link',
        ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Указываем, какие поля не обязательные
        self.fields['description'].required = False
        self.fields['mini_desc'].required = False
        self.fields['type'].required = False
        self.fields['manufacturer'].required = False
        self.fields['currency'].required = False
        self.fields['phone'].required = False
        self.fields['terms_of_sale'].required = False
        self.fields['country_of_manufacture'].required = False
        self.fields['characterization'].required = False
        self.fields['product_link'].required = False


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(label='Excel файл', required=False)


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'parent', ]


class PriceColumnForm(forms.ModelForm):
    class Meta:
        model = PriceColumn
        fields = ['name', 'formula', 'min_order_amount']


