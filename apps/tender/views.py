from django.shortcuts import render
from django.views import generic
from apps.tender.models import Tender
from apps.provider.models import Category
from apps.tender.filters import TenderFilter


class TenderListView(generic.ListView):
    model = Tender
    queryset = Tender.objects.filter(is_active=True)
    template_name = 'tender_list.html'
    paginate_by = '10'
    filter_class = TenderFilter
    context_object_name = 'tenders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProviderDetailView(generic.DetailView):
    template_name = 'tender_detail.html'
    model = Tender
    context_object_name = 'tender'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['products'] = Provider.products.all()
        return context
