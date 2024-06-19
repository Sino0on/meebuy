from django.views import generic

from apps.authentication.models import User
from apps.buyer.models import Banner, BannerSettings
from apps.provider.filters import ProviderFilter
from apps.provider.models import Provider, Category
from apps.tender.models import Country, Region, City
from apps.user_cabinet.models import Contacts


class BuyerListView(generic.ListView):
    template_name = "buyer/buyers.html"
    context_object_name = "buyers"
    model = Provider
    paginate_by = 20

    def get_queryset(self):
        queryset = Provider.objects.filter(is_active=True, title__isnull=False, user__tenders__isnull=False)
        order = self.request.GET.get("order")
        if order:
            queryset = queryset.order_by(order)
        self.filter = ProviderFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context["contacts"] = contacts
        context['categories'] = Category.objects.all()
        context["banners"] = self.get_banners()
        context[
            "banner_settings"] = BannerSettings.objects.all().first().number if BannerSettings.objects.all().first() else ''

        context['locations'] = self.get_locations()
        return context

    def get_locations(self):
        countries = Country.objects.all()
        locations = []

        for country in countries:
            country_data = {
                'id': country.id,
                'title': country.title,
                'regions': []
            }

            regions = Region.objects.filter(country=country)
            for region in regions:
                region_data = {
                    'id': region.id,
                    'title': region.title,
                    'cities': []
                }

                cities = City.objects.filter(region=region)
                for city in cities:
                    city_data = {
                        'id': city.id,
                        'title': city.title
                    }
                    region_data['cities'].append(city_data)

                country_data['regions'].append(region_data)

            locations.append(country_data)

        return locations

    def get_banners(self):
        banners = Banner.objects.filter(page_for="buyer").order_by('?')
        banner_list = []
        if banners:
            for banner in banners:
                banner_list.append(
                    {
                        'title': banner.title,
                        'image_desktop': banner.image_desktop.url,
                        'image_mobile': banner.image_mobile.url,
                        'link': banner.link
                    }
                )
        return banner_list


class BuyerDetailView(generic.DetailView):
    template_name = "buyer/buyer_detail.html"
    model = User
