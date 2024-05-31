from django.shortcuts import render
from django.views import generic

from apps.authentication.models import User
from apps.buyer.filters import BuyerFilter
from apps.provider.models import Provider
from apps.user_cabinet.models import Contacts


class BuyerListView(generic.ListView):
    template_name = 'buyer/buyers.html'
    context_object_name = 'buyers'
    model = User
    queryset = User.objects.filter(tenders=not None)
    filter_class = BuyerFilter
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context
