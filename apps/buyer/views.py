from django.shortcuts import render
from django.views import generic

from apps.authentication.models import User
from apps.buyer.filters import BuyerFilter
from apps.buyer.models import Banner, BannerSettings
from apps.provider.filters import ProviderFilter
from apps.provider.models import Provider, Category
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
        context["banner_settings"] = BannerSettings.objects.all().first().number if BannerSettings.objects.all().first() else ''

        return context

    def get_banners(self):
        banners = Banner.objects.filter(page_for="buyer").order_by('?')
        banner_list = []
        if banners:
            for banner in banners:
                banner_list.append(
                    {
                        'title': banner.title,
                        'image_desktop': banner.image_desktop,
                        'image_mobile': banner.image_mobile,
                        'link': banner.link
                    }
                )
        return banner_list


class BuyerDetailView(generic.DetailView):
    template_name = "buyer/buyer_detail.html"
    model = User
