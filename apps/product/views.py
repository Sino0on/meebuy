import os

import openpyxl
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from urllib.parse import quote

from apps.product.filters import ProductFilter
from apps.product.models import Product, ProductImg
from apps.product.forms import ProductForm, UploadExcelForm
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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['similar_products'] = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = '/products'

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImg.objects.create(product=self.object, image=image)
        return response


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = '/products'

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImg.objects.create(product=self.object, image=image)
        return response


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


class ExcelTemplateDownloadView(View):
    def get(self, request, *args, **kwargs):
        filepath = os.path.join(settings.BASE_DIR, 'apps', 'static', 'excel', 'template.xlsx')
        filename = "Шаблон_добавления_продуктов.xlsx"
        with open(filepath, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(filename)}'
            return response


class ExcelUploadView(FormView):
    template_name = 'products/upload_file.html'
    form_class = UploadExcelForm
    success_url = reverse_lazy('success_url_name')

    def form_valid(self, form):
        form = self.form_class(self.request.POST, self.request.FILES)
        file = self.request.FILES['excel_file']
        print(file)
        print(type(file))
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            print(row)
            try:
                category_instance, _ = Category.objects.get_or_create(title=row[1])
                Product.objects.create(
                    type=row[0],
                    category=category_instance,
                    title=row[2],
                    description=row[3],
                    manufacturer=row[4],
                    price=row[5],
                    retail_price=row[6],
                    wholesale_price=row[7],
                    min_quantity=row[8],
                    terms_of_sale=row[9],
                    country_of_manufacture=row[10],
                    characterization=row[11],
                    phone=row[12],
                )
            except Exception as e:
                print(e)
                continue

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy('product_list')
