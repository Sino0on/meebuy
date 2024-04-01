from django.contrib import admin
from apps.tender.models import (TypePay, Country, City, Region,
                                Tender, Category)


admin.site.register(TypePay)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(Tender)
