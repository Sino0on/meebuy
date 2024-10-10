from django.contrib import admin
from django.db import transaction
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Provider, ProvideImg, ProvideFiles, PriceFiles, VerificationDocuments, ProviderLink, \
    ProviderVerificationVideo


class ProvideImgInline(admin.TabularInline):
    model = ProvideImg
    extra = 0
    fields = ['image']


class PriceFilesInline(admin.TabularInline):
    model = PriceFiles
    extra = 0
    fields = ['file']


class ProvideFilesInline(admin.TabularInline):
    model = ProvideFiles
    extra = 0
    fields = ['image']


class ProviderVerificationDocInline(admin.TabularInline):
    model = VerificationDocuments
    extra = 0


class ProviderLinkInline(admin.TabularInline):
    model = ProviderLink
    extra = 0


class ProviderVerificationVideoInline(admin.TabularInline):
    model = ProviderVerificationVideo
    extra = 0


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'address', 'is_active', 'is_modered', 'is_provider')
    list_filter = ('is_active', 'is_modered', 'type', 'is_provider')
    search_fields = ('title', 'description', 'mini_descr', 'post_index', 'address')
    fieldsets = ()
    inlines = [ProvideImgInline, ProvideFilesInline, PriceFilesInline, ProviderVerificationDocInline, ProviderLinkInline, ProviderVerificationVideoInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all()

        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'category', 'is_main_category', 'created_at')
    list_display_links = ('indented_title',)
    mptt_indent_field = "title"
    search_fields = ('title',)

    def indented_title(self, instance):
        Category.objects.rebuild()

        """ Добавляет отступы в зависимости от уровня вложенности категории. """
        return '---' * instance.level + instance.title
    indented_title.short_description = 'Название'



# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('title',)
#     search_fields = ('title',)


# Register your models here
admin.site.register(Provider, ProviderAdmin)
admin.site.register(ProvideImg)  # Optional: If you want to manage images separately as well
admin.site.register(ProvideFiles)  # Optional: If you want to manage files separately as well
admin.site.register(ProviderVerificationVideo)