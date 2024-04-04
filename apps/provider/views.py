from django.shortcuts import render
from django.views import generic
from apps.provider.models import Provider, Category
from apps.provider.filters import ProviderFilter


class ProviderListView(generic.ListView):
    model = Provider
    queryset = Provider.objects.filter(is_active=True)
    template_name = 'auth/home.html'
    paginate_by = '10'
    filter_class = ProviderFilter
    context_object_name = 'providers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProviderDetailView(generic.DetailView):
    template_name = 'provider_detail.html'
    model = Provider
    context_object_name = 'provider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Provider.products.all()
        return context
