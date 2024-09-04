from datetime import timedelta

from django.db.models import BooleanField, Case, Value, When, F, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import generic, View
from rest_framework.generics import ListAPIView

from apps.buyer.models import Banner, BannerSettings
from apps.provider.filters import ProviderFilter
from apps.provider.models import Provider, ProviderLink, VerificationDocuments
from apps.provider.serializers import CategoryListSerializer
from apps.tender.models import Category, Country, Region, City
from apps.user_cabinet.models import Contacts
from apps.user_cabinet.models import ViewsCountProfile
from .forms import PriceFilesForm
from ..pages.models import TelegramBotToken
from ..services.send_telegram_message import send_telegram_message
from ..services.tarif_checker import check_user_status_and_open_number


class ProviderListView(generic.ListView):
    model = Provider
    template_name = "providers/provider_list.html"
    paginate_by = 10
    context_object_name = "providers"

    def __init__(self):
        super().__init__()
        self.filter = None

    def get_queryset(self):
        today = now().date()
        yesterday = today - timedelta(days=1)

        queryset = Provider.objects.annotate(
            new=Case(
                When(created_at__date=today, then=Value(True)),
                When(created_at__date=yesterday, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            tariff_title=F('user__cabinet__user_status__status__status__title'),
            # Аннотация для сортировки по is_upping и end_date
            is_upping_active=Case(
                When(
                    Q(user__cabinet__is_upping__is_active=True) &
                    Q(user__cabinet__is_upping__end_date__gte=today),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            ),
            # Аннотация для сортировки по цене тарифа
            tariff_price=F('user__cabinet__user_status__status__status__price_month')
        ).filter(is_active=True, is_provider=True, title__isnull=False)

        # Получаем параметр сортировки из запроса
        order = self.request.GET.get("order")
        # Добавляем новое условие сортировки к существующему
        if order:
            queryset = queryset.order_by('-is_upping_active', 'tariff_price', order, '-is_modered', "-id")
        else:
            queryset = queryset.order_by('-is_upping_active', 'tariff_price', '-is_modered', "-id")

        self.filter = ProviderFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['wholesale'] = queryset.filter(is_modered=True, is_provider=True, type='wholesale')
        context['manufacturing'] = queryset.filter(is_modered=True, is_provider=True, type='manufacturing[')
        context['services'] = queryset.filter(is_modered=True, is_provider=True, type='services')
        categories = Category.objects.filter(category=None).annotate(
            has_children=Case(
                When(categor__isnull=False, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        for cat in categories:
            print(cat.has_children)
        context['categories'] = categories.distinct()
        context["all"] = True
        context["filter"] = self.filter
        contacts = Contacts.load()
        context["contacts"] = contacts
        context["banners"] = self.get_banners()
        context[
            "banner_settings"] = BannerSettings.objects.all().first().number if BannerSettings.objects.all().first() else ''

        context['locations'] = self.get_locations()
        return context

    def get_locations(self):
        countries = Country.objects.all()
        locations = []
        for country in countries:
            country_data = {
                'id': country.id,
                'title': country.title,
                'regions': []
            }
            regions = Region.objects.filter(country=country)
            for region in regions:
                region_data = {
                    'id': region.id,
                    'title': region.title,
                    'cities': []
                }
                cities = City.objects.filter(region=region)
                for city in cities:
                    city_data = {
                        'id': city.id,
                        'title': city.title
                    }
                    region_data['cities'].append(city_data)
                country_data['regions'].append(region_data)
            locations.append(country_data)
        return locations

    def get_banners(self):
        banners = Banner.objects.filter(page_for="provider").order_by('?')
        banner_list = []
        if banners:
            for banner in banners:
                banner_list.append(
                    {
                        'title': banner.title,
                        'image_desktop': banner.image_desktop.url,
                        'image_mobile': banner.image_mobile.url,
                        'link': banner.link
                    }
                )
        return banner_list


class ProviderCategoryListView(ProviderListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(category=self.kwargs['pk']).annotate(
            has_children=Case(
                When(categor__isnull=False, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        print(categories)
        context['categories'] = categories.distinct()
        context["all"] = False

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
        context["documents"] = self.object.documents.filter(verified=True)
        context["links"] = self.object.links.filter(verified=True)

        if self.request.GET.get("open"):
            open_status = check_user_status_and_open_number(self.request)
            if open_status == "open":
                context["open"] = "open"

        return context


class CategoryListView(ListAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return Category.objects.filter(category=None)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user_id = self.kwargs.get("pk")

        user = get_object_or_404(Provider, id=user_id)
        context.update({"request": self.request, "categories": user.category.all()})

        return context


def upload_file(request):
    if request.method == "POST":

        form = PriceFilesForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            instance = form.save(commit=False)
            instance.providers = request.user.provider
            instance.save()
            return redirect("view_profile")
        else:
            print("Form is not valid", form.errors)
    else:
        print("Form is not valid")
        form = PriceFilesForm()

    context = {
        "form": form,
        "provider": Provider.objects.get(user=request.user),
    }
    return render(request, "cabinet/provider_profile.html", context)


class DocumentCreateView(View):
    def get(self, request):
        context = {
            'documents': VerificationDocuments.objects.filter(provider=request.user.provider),
        }
        return render(request, 'cabinet/documents.html', context=context)

    def post(self, request):
        files = request.FILES.getlist('documents')
        for file in files:
            VerificationDocuments.objects.create(document=file, provider=request.user.provider)

        message = f'Пользователь {request.user} отправил документы для проверки.'

        token = TelegramBotToken.objects.first()
        for chat in (chat.strip() for chat in token.report_channels.split(',')):
            send_telegram_message(token.bot_token, chat, message)

        return redirect('documents')


class DocumentDeleteView(View):
    def post(self, request, pk):
        document = get_object_or_404(VerificationDocuments, pk=pk)
        document.delete()
        return redirect('documents')


class AddLinkView(View):
    template_name = 'cabinet/provider_profile.html'

    def get(self, request):
        # Отображение пустой формы при GET запросе
        return render(request, self.template_name)

    def post(self, request):
        # Получение списков данных для каждого поля
        names = request.POST.getlist('name')
        links = request.POST.getlist('link')

        # Проверка количества элементов в обоих списках
        if len(names) == len(links):
            # Удаление всех предыдущих ссылок пользователя
            ProviderLink.objects.filter(provider=request.user.provider).delete()

            # Создание новых объектов ProviderLink
            for name, link in zip(names, links):
                if name.strip() and link.strip():  # Сохранение только непустых значений
                    ProviderLink.objects.create(name=name, link=link, provider=request.user.provider)

            # Перенаправление на профиль пользователя после сохранения
            return redirect('view_profile')
        else:
            # Обработка ошибки, если списки имеют разное количество элементов
            return render(request, self.template_name, {
                'error': 'Количество названий и ссылок не совпадает.'
            })

        return redirect('view_profile')
