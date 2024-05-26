from django.shortcuts import render
from django.views import generic
from apps.provider.models import Provider, Tag
from apps.tender.models import Category
from apps.provider.filters import ProviderFilter
from rest_framework.generics import ListAPIView
from apps.provider.serializers import CategoryListSerializer
from apps.user_cabinet.models import Contacts


class ProviderListView(generic.ListView):
    model = Provider
    queryset = Provider.objects.filter(is_modered=True)
    template_name = 'providers/provider_list.html'
    paginate_by = '10'
    filter_class = ProviderFilter
    context_object_name = 'providers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['types'] = Tag.objects.all()
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class ProviderDetailView(generic.DetailView):
    template_name = 'providers/provider_detail.html'
    model = Provider
    context_object_name = 'provider'
    # lookup_field = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.all()[:3]
        context['images'] = self.object.images.all()
        return context


class CategoryListView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(category=None)


