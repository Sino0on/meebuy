from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import BooleanField, Case, Value, When, F, Q, IntegerField, Exists, OuterRef
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import generic, View
from rest_framework.generics import ListAPIView
from django.core.mail import EmailMessage

from apps.buyer.models import Banner, BannerSettings
from apps.provider.filters import ProviderFilter
from apps.provider.models import Provider, ProviderLink, VerificationDocuments, ProviderVerificationVideo
from apps.provider.serializers import CategoryListSerializer
from apps.tender.models import Category, Country, Region, City
from apps.user_cabinet.models import Contacts
from apps.user_cabinet.models import ViewsCountProfile
from .forms import PriceFilesForm
from apps.pages.models import TelegramBotToken
from apps.services.send_telegram_message import send_telegram_message
from apps.services.tarif_checker import check_user_status_and_open_number
from django.core.mail import send_mail


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
            tariff_price=Case(
                When(user__cabinet__user_status__status__status__price_month__isnull=False,
                     then=F('user__cabinet__user_status__status__status__price_month')),
                default=Value(-1),
                output_field=IntegerField()
            ),
            is_verified_case = Case(
                When(~Exists(VerificationDocuments.objects.filter(provider=OuterRef('pk'))), then=Value(0)),
                When(Exists(VerificationDocuments.objects.filter(provider=OuterRef('pk'), verified=False)), then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            )
        ).filter(is_active=True, is_provider=True, title__isnull=False)
        for q in queryset:
            print(q.is_verified_case)
        # Получаем параметр сортировки из запроса
        order = self.request.GET.get("order")
        # Добавляем новое условие сортировки к существующему
        if order:
            queryset = queryset.order_by('-is_upping_active', order, '-tariff_price', '-is_verified_case', '-is_modered', "-id")
        else:
            queryset = queryset.order_by('-is_upping_active', '-tariff_price', '-is_verified_case', '-is_modered', "-id")

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
        context['categories'] = categories.distinct()
        context["all"] = True
        context["filter"] = self.filter
        contacts = Contacts.load()
        context["contacts"] = contacts
        context["banners"] = self.get_banners()
        context[
            "banner_settings"] = BannerSettings.objects.all().first().number if BannerSettings.objects.all().first() else ''

        context['locations'] = self.get_locations()
        context["side_banner"] = Banner.objects.filter(image_vertical__isnull=False, page_for="provider" ).order_by('?').first()
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
        category_id = self.request.GET.get("category")
        if category_id:
            context['current'] = int(category_id)
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
        context["products"] = self.object.products.all().order_by("?")
        context["images"] = self.object.images.all()
        context["companies"] = Provider.objects.exclude(id=self.object.id).filter(
            is_provider=True, is_modered=True, is_active=True
        )
        context["documents"] = self.object.documents.filter(verified=True)
        context["links"] = self.object.links.filter(verified=True)
        context["video_verification_icon"] = TelegramBotToken.objects.first().video_verification_icon.url if TelegramBotToken.objects.first().video_verification_icon else ''
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
        if not files:
            return redirect('documents')  # Если файлов нет, возвращаем пользователя

        # Создание записей документов и сбор их названий
        file_names = [file.name for file in files]
        for file in files:
            VerificationDocuments.objects.create(document=file, provider=request.user.provider)

        # Формирование сообщения с перечислением имен файлов
        file_names_text = ', '.join(file_names)
        message = f'Пользователь {request.user} отправил следующие документы для проверки: {file_names_text}.'

        token = TelegramBotToken.objects.first()
        if token:
            for chat in (chat.strip() for chat in token.report_channels.split(',')):
                send_telegram_message(token.bot_token, chat, message)  # Отправка сообщения в Telegram

            if token.email:
                # Отправка email с именами файлов
                email = EmailMessage(
                    'Документы отправлены на проверку',
                    f'Юзер {request.user}, следующие документы были отправлены на проверку: {file_names_text}.',
                    'your-email@example.com',  # Этот email должен быть настроен в вашем Django settings
                    [token.email],  # Получатель
                )
                email.send(fail_silently=False)  # Отправляем email

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
        names = request.POST.getlist('name')
        links = request.POST.getlist('link')

        if len(names) == len(links):
            ProviderLink.objects.filter(provider=request.user.provider).delete()

            for name, link in zip(names, links):
                if name.strip() and link.strip():
                    ProviderLink.objects.create(name=name, link=link, provider=request.user.provider)

            return redirect('view_profile')
        else:
            return render(request, self.template_name, {
                'error': 'Количество названий и ссылок не совпадает.'
            })

        return redirect('view_profile')

class AddVideoView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'videos': ProviderVerificationVideo.objects.filter(provider=request.user.provider),
        }
        return render(request, 'cabinet/add_video.html', context=context)

    def post(self, request):
        files = request.FILES.getlist('videos')
        if not files:
            message = f'Пользователь {request.user} не отправил видео для верификации.'
            return redirect('add_video')

        file_names = [file.name for file in files]
        for file in files:
            ProviderVerificationVideo.objects.create(video=file, provider=request.user.provider)

        file_names_text = ', '.join(file_names)
        message = f'Пользователь {request.user} отправил следующие видео для верификации: {file_names_text}.'

        token = TelegramBotToken.objects.first()
        if token:
            for chat in (chat.strip() for chat in token.report_channels.split(',')):
                send_telegram_message(token.bot_token, chat, message)

            if token.email:
                email = EmailMessage(
                    'Документы отправлены на проверку',
                    f'Юзер {request.user}, следующие видео были отправлены на проверку для верификации: {file_names_text}.',
                    'your-email@example.com',
                    [token.email],
                )
                email.send(fail_silently=False)

        return redirect('add_video')

class VideoDeleteView(View):
    def post(self, request, pk):
        document = get_object_or_404(ProviderVerificationVideo, pk=pk)
        document.delete()
        return redirect('add_video')

