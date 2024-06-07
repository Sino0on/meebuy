from django.shortcuts import render
from django.views import generic

from apps.authentication.models import User
from apps.buyer.filters import BuyerFilter
from apps.provider.models import Provider
from apps.user_cabinet.models import Contacts


class BuyerListView(generic.ListView):
    template_name = "buyer/buyers.html"
    context_object_name = "buyers"
    model = User
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        order = self.request.GET.get("order")
        if order:
            queryset = queryset.order_by(order)
        self.filter = BuyerFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context["contacts"] = contacts
        return context


class BuyerDetailView(generic.DetailView):
    template_name = "buyer/buyer_detail.html"
    model = User
