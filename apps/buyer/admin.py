from django.contrib import admin
from apps.buyer.models import Banner, BannerSettings, Buyer


admin.site.register(Buyer)

class BannerInline(admin.StackedInline):
    model = Banner
    extra = 0

@admin.register(BannerSettings)
class BannerSettingsAdmin(admin.ModelAdmin):
    list_display = ["number"]
    inlines = [BannerInline]

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "link", "page_for", "is_active", "settings", "created_at"]
    list_filter = ["title", "page_for", "is_active", "created_at"]
    search_fields = ["title", "page_for", "link", "created_at"]
    date_hierarchy = "created_at"
    fields = (
        "title",
        "link",
        "page_for",
        "settings",
        "image_desktop",
        "get_image_desktop",
        "image_mobile",
        "get_image_mobile",
        "is_active",
        "created_at",
    )
    readonly_fields = ("get_image_desktop", "get_image_mobile", "created_at", 'settings')
