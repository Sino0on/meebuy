from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from apps.provider.models import Provider, Tag
from apps.tender.models import Category
from apps.provider.filters import ProviderFilter
from apps.user_cabinet.models import ViewsCountProfile
from rest_framework.generics import ListAPIView
from apps.provider.serializers import CategoryListSerializer
from apps.user_cabinet.models import Contacts


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
        context["categories"] = Category.objects.all()
        context["types"] = Tag.objects.all()
        context["filter"] = self.filter
        contacts = Contacts.load()
        context["contacts"] = contacts
        return context


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
        return context


class CategoryListView(ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(category=None)
