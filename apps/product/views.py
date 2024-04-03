from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.product.filters import ProductFilter
from apps.product.models import Product
from apps.product.forms import ProductForm
from apps.provider.models import Category


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/product_list.html'
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        title_query = self.request.GET.get('title')
        price_min_query = self.request.GET.get('price_min')
        price_max_query = self.request.GET.get('price_max')
        category_query = self.request.GET.get('category')

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)
        if price_min_query:
            queryset = queryset.filter(price__gte=price_min_query)
        if price_max_query:
            queryset = queryset.filter(price__lte=price_max_query)
        if category_query:
            queryset = queryset.filter(category__id=category_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
