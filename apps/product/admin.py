from django.contrib import admin

from .models import (
    Product,
    ProductImg,
    ProductCategory,
    PriceColumn, Currency, ProductBanner
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


class ProductImgInline(admin.TabularInline):
    model = ProductImg
    extra = 0
    fields = ['image']


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'price', 'min_quantity', 'category', 'created_at',
        'updated_at', 'is_new', 'is_recommended', 'is_active')
    list_filter = ('category', 'created_at', 'updated_at', 'country_of_manufacture')
    search_fields = (
        'title', 'description', 'mini_desc', 'manufacturer', 'phone', 'terms_of_sale', 'country_of_manufacture',
        'characterization')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImgInline]

    fieldsets = (
        (None, {
            'fields': (
                'is_new', 'is_recommended', 'is_active',
                'title', 'provider', 'image', 'description', 'mini_desc', 'type', 'manufacturer', 'price',
                'min_quantity',
                'category', 'currency')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('phone', 'terms_of_sale', 'country_of_manufacture', 'characterization'),
        }),
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImg)  # If you want basic management for ProductImg outside the inline
admin.site.register(PriceColumn)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductBanner)
class ProductBannerAdmin(admin.ModelAdmin):
    pass
