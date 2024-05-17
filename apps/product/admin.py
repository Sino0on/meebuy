from django.contrib import admin
from .models import Product, ProductImg


class ProductImgInline(admin.TabularInline):
    model = ProductImg
    extra = 0
    fields = ['image']


class ProductAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'price', 'retail_price', 'wholesale_price', 'min_quantity', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at', 'country_of_manufacture')
    search_fields = (
    'title', 'description', 'mini_desc', 'manufacturer', 'phone', 'terms_of_sale', 'country_of_manufacture', 'characterization')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImgInline]

    fieldsets = (
        (None, {
            'fields': (
            'title', 'provider', 'image', 'description', 'mini_desc', 'type', 'manufacturer', 'price', 'retail_price', 'wholesale_price', 'min_quantity',
            'category')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('phone', 'terms_of_sale', 'country_of_manufacture', 'characterization'),
        }),
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImg)  # If you want basic management for ProductImg outside the inline
