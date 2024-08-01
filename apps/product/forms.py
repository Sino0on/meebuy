from django import forms

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
            'small_wholesale',
            'medium_wholesale',
            'large_wholesale',
        ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
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
        self.fields['small_wholesale'].required = False
        self.fields['medium_wholesale'].required = False
        self.fields['large_wholesale'].required = False


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
