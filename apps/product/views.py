import os
from urllib.parse import quote, unquote
from django.db.models import Count, BooleanField
import random
import openpyxl
import requests
from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import IntegerField, When, Case, Value
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    FormView,
)
from six import BytesIO

from apps.pages.models import TelegramBotToken
from apps.product.filters import ProductFilter
from apps.product.forms import (
    ProductForm,
    UploadExcelForm,
    ProductCategoryForm,
    PriceColumnForm, AddNewCategoryRequestForm,
)
from apps.product.models import (
    Product,
    ProductImg,
    ProductCategory,
    PriceColumn, Currency,
    ProductBanner, AddNewCategoryRequest
)
from apps.provider.models import (
    Category,
    Provider,
    PriceFiles
)
from apps.services.send_telegram_message import send_telegram_message
from apps.services.tarif_checker import check_user_status_and_open_number
from apps.user_cabinet.models import Contacts, OpenNumberCount


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    paginate_by = 20
    template_name = "products/product_list.html"
    filter_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.annotate(
            provider_status_priority=Case(
                When(provider__user_cabinet__user_status__status__priorety=True, then=Value(-1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )

        order = self.request.GET.get("order")

        if order:
            queryset = queryset.order_by(order, 'provider_status_priority', '-id').distinct(order,
                                                                                            'provider_status_priority',
                                                                                            'id')
        else:
            queryset = queryset.order_by('provider_status_priority', '-id').distinct('provider_status_priority', 'id')
        filter = self.filter_class(self.request.GET, queryset=queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.filter(children__isnull=False).annotate(
            has_children=Case(
                When(children__isnull=False, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        context['categories'] = categories.distinct()
        context["all"] = False
        contacts = Contacts.load()
        context["contacts"] = contacts
        context["best_products"] = Product.objects.filter(is_recommended=True).order_by('?')[:8]
        wide_count = ProductBanner.objects.filter(wide_banner__isnull=False).count()
        if wide_count > 0:
            random_index = random.randint(0, wide_count - 1)
            context["banner_1"] = ProductBanner.objects.filter(wide_banner__isnull=False)[random_index]

        left_count = ProductBanner.objects.filter(left_banner__isnull=False).count()
        if left_count > 0:
            random_index = random.randint(0, left_count - 1)
            context["banner_2"] = ProductBanner.objects.filter(left_banner__isnull=False)[random_index]

        right_count = ProductBanner.objects.filter(right_banner__isnull=False).count()
        if right_count > 0:
            random_index = random.randint(0, right_count - 1)
            context["banner_3"] = ProductBanner.objects.filter(right_banner__isnull=False)[random_index]

        bottom_count = ProductBanner.objects.filter(bottom_banner__isnull=False).count()
        if bottom_count > 0:
            random_index = random.randint(0, bottom_count - 1)
            context["banner_4"] = ProductBanner.objects.filter(bottom_banner__isnull=False)[random_index]

        return context


class ProductCategoryListView(ProductListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.filter(parent__id=self.kwargs['pk']).annotate(
            has_children=Case(
                When(children__isnull=False, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        context['categories'] = categories.distinct()
        context["all"] = False

        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"

    def get_product_prices(self):
        product = self.get_object()
        prices = []
        formulas = PriceColumn.objects.filter(provider=self.object.provider)
        decimal = product.provider.decimal_places
        if formulas:
            for formula in formulas:
                prices.append(
                    {
                        "name": formula.name,
                        "price": formula.apply_formula(product.price),
                        "min_order_amount": formula.min_order_amount,
                        "decimal": decimal,
                    }
                )
        else:
            prices.append({"name": "Цена", "price": product.price, "decimal": decimal, 'min_order_amount': False})
        return prices

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["categories"] = ProductCategory.objects.all()
        context["similar_products"] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:5]
        context["prices"] = self.get_product_prices()

        if self.request.GET.get("open"):
            open_status = check_user_status_and_open_number(self.request)
            if open_status == "open":
                context["open"] = "open"

        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "cabinet/products.html"
    success_url = reverse_lazy("user_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = Currency.objects.all()
        if not currency:
            currency = Currency.objects.create(name="Сом", code="KGS")
        categories = ProductCategory.objects.filter(provider__user=self.request.user)
        context["currencies"] = Currency.objects.all()
        context['categories'] = categories
        category_tree = self.build_category_tree(categories)
        context['category_tree'] = category_tree
        return context

    def build_category_tree(self, categories, parent=None, level=0):
        tree = []
        for category in categories:
            if category.parent == parent:
                tree.append((category, level))
                tree.extend(self.build_category_tree(categories, category, level + 1))
        return tree

    def form_valid(self, form):
        provider = get_object_or_404(Provider, user=self.request.user)
        cabinet = provider.user.cabinet
        active_user_status = cabinet.user_status

        if active_user_status:
            max_products = active_user_status.status.status.quantity_products
            current_product_count = Product.objects.filter(provider=provider, is_active=True).count()
            if current_product_count >= max_products:
                form.instance.is_active = False
                messages.warning(self.request, 'Превышен лимит активных продуктов. Продукт создан, но он неактивен.')
            else:
                form.instance.is_active = True
                messages.success(self.request, 'Продукт успешно создан и активен.')
        else:
            if Product.objects.filter(provider=provider, is_active=True).count() >= 100:
                messages.warning(self.request, 'Превышен лимит активных продуктов. Продукт создан, но он неактивен.')
                form.instance.is_active = False
            else:
                form.instance.is_active = True

        form.instance.provider = provider

        response = super().form_valid(form)
        category = self.request.POST.get("category")
        currency = self.request.POST.get("currency")
        c = Currency.objects.get(id=currency)
        self.object.currency = c.code
        self.object.save()

        # Обработка изображений
        images = self.request.FILES.getlist("images")
        if images:
            main_image = images[0]
            ProductImg.objects.create(product=self.object, image=main_image)
            self.object.image = main_image
            self.object.save()

        for image in images[1:]:
            ProductImg.objects.create(product=self.object, image=image)

        return response

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "cabinet/product_update.html"
    success_url = reverse_lazy("user_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()
        currency = Currency.objects.all()
        if not currency:
            currency = Currency.objects.create(name="Сом", code="KGS")
        context["currencies"] = Currency.objects.all()
        product_images = list(ProductImg.objects.filter(product=self.object))
        for i in range(1, 7):
            context[f"image_{i}"] = product_images[i - 1] if i <= len(product_images) else None

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        currency = self.request.POST.get("currency")
        c = Currency.objects.get(id=currency)
        self.object.currency = c.code
        self.object.save()

        current_images = list(ProductImg.objects.filter(product=self.object))

        if current_images:
            self.object.image = current_images[0].image
            self.object.save()

        for i in range(1, 7):
            image_file = self.request.FILES.get(f"image_{i}")
            if image_file:
                if i <= len(current_images):
                    current_images[i - 1].image = image_file
                    current_images[i - 1].save()
                else:
                    ProductImg.objects.create(product=self.object, image=image_file)

        return response


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("user_products")


class ExcelTemplateDownloadView(View):
    def get(self, request, *args, **kwargs):
        filepath = os.path.join(
            settings.BASE_DIR, "apps", "static", "excel", "template.xlsx"
        )
        filename = "Шаблон_добавления_продуктов.xlsx"
        with open(filepath, "rb") as excel_file:
            response = HttpResponse(
                excel_file.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = (
                f"attachment; filename*=UTF-8''{quote(filename)}"
            )
            return response


class DownloadPriceFileView(View):
    def get(self, request, *args, **kwargs):
        # Получение и декодирование относительного пути к файлу из параметров запроса
        relative_path = request.GET.get('filename')
        if not relative_path:
            print("Имя файла не указано")
            raise Http404("Имя файла не указано")

        # Декодирование пути
        safe_path = unquote(relative_path)

        # Построение полного пути к файлу
        filepath = os.path.join(settings.MEDIA_ROOT, safe_path)
        print(f"Attempting to access file at: {filepath}")

        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            raise Http404("Файл не найден")

        try:
            with open(filepath, "rb") as excel_file:
                response = HttpResponse(
                    excel_file.read(),
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                response["Content-Disposition"] = f"attachment; filename*=UTF-8''{quote(os.path.basename(filepath))}"
                return response
        except Exception as e:
            print(f"Error reading file: {e}")
            raise Http404("Ошибка при чтении файла")


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFileView(View):
    def post(self, request, *args, **kwargs):
        import json
        data = json.loads(request.body)
        file_id = data.get('file_id')
        if file_id:
            try:
                file_instance = PriceFiles.objects.get(id=file_id)
                file_instance.delete()
                return JsonResponse({'status': 'success'}, status=200)
            except PriceFiles.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'File not found'}, status=404)
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


class ExcelUploadView(FormView):
    template_name = "products/upload_file.html"
    form_class = UploadExcelForm
    success_url = reverse_lazy("user_products")

    def form_valid(self, form):
        form = self.form_class(self.request.POST, self.request.FILES)
        file = self.request.FILES.get("file")

        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        provider = Provider.objects.get(user=self.request.user)

        for row in sheet.iter_rows(min_row=3, values_only=True):
            try:
                category_instance, _ = ProductCategory.objects.get_or_create(
                    name=row[1], provider=provider
                )

                image_url = row[12]
                if image_url and isinstance(image_url, str):
                    print(image_url)
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    image_io = BytesIO()
                    image.save(image_io, format="WEBP")
                    image_content = ContentFile(image_io.getvalue(), name="image.webp")
                else:
                    image_content = None
                product = Product.objects.create(
                    provider=provider,
                    type=row[0],
                    category=category_instance,
                    title=row[2],
                    mini_desc=row[3],
                    description=row[4],
                    manufacturer=row[5],
                    price=row[6],
                    min_quantity=row[7],
                    terms_of_sale=row[8],
                    country_of_manufacture=row[9],
                    characterization=row[10],
                    phone=row[11],
                )
                if image_content:
                    product.image.save(image_content.name, image_content)
            except Exception as e:
                print(e)
                continue

        return super().form_valid(form)


class AddNewCategoryRequestView(CreateView):
    model = AddNewCategoryRequest
    form_class = AddNewCategoryRequestForm
    template_name = "cabinet/products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()
        context['categories_change'] = 2

        return context

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        print(form)
        message = f"Запрос на добавление категории от пользователя {self.request.user}:\n"
        message += f"Название новой категории: {form.cleaned_data['new_category_name']}\n"
        if form.cleaned_data['parent']:
            message += f"Родительская категория: {form.cleaned_data['parent']}\n"
        token = TelegramBotToken.objects.first()
        for chat in (chat.strip() for chat in token.report_channels.split(',')):
            send_telegram_message(token.bot_token, chat, message)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_products') + '?categories_change=2'


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = "cabinet/product_includes/edit_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductCategory.objects.all()
        return context

    def form_valid(self, form):
        form.instance.provider = self.request.user.provider
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('user_products') + '?categories_change=2'


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = "cabinet/product_includes/delete_category.html"
    success_url = reverse_lazy("user_products")


class PriceColumnCreateView(CreateView):
    model = PriceColumn
    form_class = PriceColumnForm
    template_name = "cabinet/products.html"
    success_url = reverse_lazy("user_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context["contacts"] = contacts
        categories = ProductCategory.objects.filter(provider__user=self.request.user)
        context["categories"] = categories
        context["prices"] = PriceColumn.objects.filter(provider__user=self.request.user)
        context["decimal"] = self.request.user.provider.decimal_places
        if self.get_queryset().exists():
            context["has_products"] = True
        else:
            context["has_products"] = False

        return context

    def form_valid(self, form):
        form.instance.provider = self.request.user.provider

        # Получаем данные из формы
        post_data = self.request.POST
        names = post_data.getlist("name")
        formulas = post_data.getlist("formula")
        min_order_amounts = post_data.getlist("min_order_amount")
        decimal = post_data.get("decimal")
        form.instance.provider.decimal_places = decimal
        form.instance.provider.save()
        PriceColumn.objects.filter(provider__user=self.request.user).delete()
        for index, (name, formula, min_order_amount) in enumerate(
                zip(names, formulas, min_order_amounts)
        ):
            if index != len(names) - 1:
                PriceColumn.objects.create(
                    provider=form.instance.provider,
                    name=name,
                    formula=formula,
                    min_order_amount=int(min_order_amount),
                )

        return super().form_valid(form)

    def form_invalid(self, form):
        PriceColumn.objects.filter(provider__user=self.request.user).delete()
        return HttpResponseRedirect(reverse("user_products"))


class PriceColumnUpdateView(UpdateView):
    model = PriceColumn
    form_class = PriceColumnForm
    template_name = "cabinet/products.html"
    success_url = reverse_lazy("user_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context["contacts"] = contacts
        categories = ProductCategory.objects.filter(provider__user=self.request.user)
        context["categories"] = categories
        context["prices"] = PriceColumn.objects.filter(provider__user=self.request.user)
        context["decimal"] = self.request.user.provider.decimal_places
        if self.get_queryset().exists():
            context["has_products"] = True
        else:
            context["has_products"] = False

        return context


class PriceColumnDeleteView(DeleteView):
    model = PriceColumn
    template_name = "cabinet/products.html"
    success_url = reverse_lazy("user_products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context["contacts"] = contacts
        categories = ProductCategory.objects.filter(provider__user=self.request.user)
        context["categories"] = categories
        context["prices"] = PriceColumn.objects.filter(provider__user=self.request.user)
        context["decimal"] = self.request.user.provider.decimal_places
        if self.get_queryset().exists():
            context["has_products"] = True
        else:
            context["has_products"] = False

        return context
