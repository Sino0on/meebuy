from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from apps.buyer.models import Banner, BannerSettings
from apps.provider.models import Provider
from apps.tender.models import Category, Country, Region, City
from apps.provider.filters import ProviderFilter
from apps.user_cabinet.models import ViewsCountProfile, OpenNumberCount
from rest_framework.generics import ListAPIView
from apps.provider.serializers import CategoryListSerializer
from apps.user_cabinet.models import Contacts
from .forms import PriceFilesForm


class ProviderListView(generic.ListView):
    model = Provider
    template_name = "providers/provider_list.html"
    paginate_by = 10
    context_object_name = "providers"

    def __init__(self):
        super().__init__()
        self.filter = None

    def get_queryset(self):
        queryset = Provider.objects.filter(is_modered=True, is_provider=True)
        order = self.request.GET.get("order")
        if order:
            queryset = queryset.order_by(order)
        self.filter = ProviderFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['wholesale'] = queryset.filter(is_modered=True, is_provider=True, type='wholesale')
        context['manufacturing'] = queryset.filter(is_modered=True, is_provider=True, type='manufacturing[')
        context['services'] = queryset.filter(is_modered=True, is_provider=True, type='services')
        context["categories"] = Category.objects.all()
        # context["types"] = Tag.objects.all()
        context["filter"] = self.filter
        contacts = Contacts.load()
        context["contacts"] = contacts
        context["banners"] = self.get_banners()
        context["banner_settings"] = BannerSettings.objects.all().first().number if BannerSettings.objects.all().first() else ''

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
        banners = Banner.objects.filter(page_for="provider").order_by('?')
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


class ProviderDetailView(generic.DetailView):
    template_name = "providers/provider_detail.html"
    model = Provider
    context_object_name = "provider"
    # lookup_field = 'id'

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            if request.user.is_authenticated:
                ViewsCountProfile.objects.create(
                    quest=request.user, user=self.get_object().user.cabinet
                )
            else:
                ViewsCountProfile.objects.create(user=self.get_object().user.cabinet)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.object.products.all()[:3]
        context["images"] = self.object.images.all()
        context["companies"] = Provider.objects.exclude(id=self.object.id).filter(
            is_provider=True, is_modered=True, is_active=True
        )
        if self.request.GET.get("open"):
            if self.request.user.is_authenticated:
                print(self.get_object().user)
                if self.get_object().user.cabinet.user_status:
                    if (
                        self.get_object().user.cabinet.user_status.status.is_publish_phone
                    ):
                        OpenNumberCount.objects.create(
                            user=self.get_object().user.cabinet
                        )
                        context["open"] = "open"
        return context


class CategoryListView(ListAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return Category.objects.filter(category=None)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user_id = self.kwargs.get("pk")

        user = get_object_or_404(Provider, id=user_id)
        context.update({"request": self.request, "categories": user.category.all()})
 
        return context


def upload_file(request):
    if request.method == "POST":
        form = PriceFilesForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.providers = request.user.provider
            instance.save()
            return redirect("view_profile")
        else:
            print("Form is not valid", form.errors)
    else:
        form = PriceFilesForm()

    context = {
        "form": form,
        "provider": Provider.objects.get(user=request.user),
    }
    return render(request, "cabinet/provider_profile.html", context)