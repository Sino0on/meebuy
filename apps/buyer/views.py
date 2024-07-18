from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, BooleanField, When
from django.shortcuts import redirect
from django.views import generic

from apps.authentication.forms import ProviderForm
from apps.authentication.models import User
from apps.buyer.models import Banner, BannerSettings
from apps.provider.filters import ProviderFilter
from apps.provider.models import Provider, Category
from apps.tender.models import Country, Region, City
from apps.user_cabinet.models import Contacts


class BuyersStepView(LoginRequiredMixin, generic.UpdateView):
    template_name = "buyer/buyers_step.html"
    model = Provider
    queryset = Provider.objects.all()
    form_class = ProviderForm
    context_object_name = 'form'
    success_url = '/profile/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user.provider

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект, который будет обновляться
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            self.object = form.save(
                commit=False)  # Сохраняем форму с возможностью дополнительной обработки перед окончательным сохранением
            self.object.comment = 'Ваша анкета на рассмотрении. Пожалуйста, подождите'
            self.object.save()  # Сохраняем изменения в объект
            form.save_m2m()  # Сохраняем ManyToMany поля
            return redirect(self.get_success_url())  # Переадресация на страницу успеха
        else:
            print(form.errors)  # Вывод ошибок на консоль для отладки
            return self.form_invalid(form)


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
        categories = Category.objects.filter(category=None).annotate(
            has_children=Case(
                When(categor__isnull=False, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        for cat in categories:
            print(cat.has_children)
        context['categories'] = categories.distinct()
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


class BuyerCategoryListView(BuyerListView):
    def get_queryset(self):
        queryset = Provider.objects.filter(is_modered=True, is_provider=False, category=self.kwargs['pk'])
        order = self.request.GET.get("order")
        if order:
            queryset = queryset.order_by(order)
        self.filter = ProviderFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(category=self.kwargs['pk']).annotate(
            has_children=Case(
                When(categor__isnull=False, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        print(categories)
        context['categories'] = categories.distinct()
        context["all"] = False

        return context


class BuyerDetailView(generic.DetailView):
    template_name = "buyer/buyer_detail.html"
    model = User
