from django.contrib import admin

from .models import Country, Region, City, Tender, TenderImg, TenderOpenHelpText


@admin.register(TenderOpenHelpText)
class TenderOpenHelpTextAdmin(admin.ModelAdmin):
    list_display = ['title', 'text']


class TenderImgInline(admin.TabularInline):
    model = TenderImg
    extra = 1
    fields = ['image']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['title', 'country']
    list_filter = ['country']
    search_fields = ['title']
    autocomplete_fields = ['country']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['title', 'region']
    list_filter = ['region__country', 'region']
    search_fields = ['title']
    autocomplete_fields = ['region']


class TenderAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'city', 'user', 'created_at', 'end_date', 'is_phone']
    list_filter = ['created_at', 'end_date', 'city__region__country', 'city__region', 'city', 'category']
    search_fields = ['title', 'description', 'requirements', 'place_of_sale']
    autocomplete_fields = ['category', 'city', 'user']
    date_hierarchy = 'created_at'

    readonly_fields = ('created_at', 'updated_at')
    inlines = [TenderImgInline]


admin.site.register(Tender, TenderAdmin)
