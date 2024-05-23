import os

import openpyxl
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from urllib.parse import quote

from apps.product.filters import ProductFilter
from apps.product.models import Product, ProductImg, ProductCategory
from apps.product.forms import ProductForm, UploadExcelForm
from apps.provider.models import Category, Provider


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 20
    template_name = 'products/product_list.html'
    filter_class = ProductFilter

    def get_queryset(self):
        query = self.queryset
        filter = self.filter_class(self.request.GET, queryset=query)
        query = filter.qs
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
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
        provider = Provider.objects.get(user=self.request.user)
        form.instance.provider = provider
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

        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        provider = Provider.objects.get(user=self.request.user)

        for row in sheet.iter_rows(min_row=2, values_only=True):
            try:
                category_instance, _ = ProductCategory.objects.get_or_create(title=row[1])
                Product.objects.create(
                    provider=provider,
                    type=row[0],
                    category=category_instance,
                    title=row[2],
                    mini_desc=row[3],
                    description=row[4],
                    manufacturer=row[5],
                    price=row[6],
                    retail_price=row[7],
                    wholesale_price=row[8],
                    min_quantity=row[9],
                    terms_of_sale=row[10],
                    country_of_manufacture=row[11],
                    characterization=row[12],
                    phone=row[13],
                )
            except Exception as e:
                print(e)
                continue

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy('product_list')
