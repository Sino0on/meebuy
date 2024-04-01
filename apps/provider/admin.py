from django.contrib import admin
from apps.provider.models import (Provider, Category, Tag, Condition, ProvideImg,
                                  ProvideFiles, Delivery)


admin.site.register(Provider)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Condition)
admin.site.register(ProvideImg)
admin.site.register(ProvideFiles)
admin.site.register(Delivery)
