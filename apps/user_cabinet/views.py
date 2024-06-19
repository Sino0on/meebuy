import datetime
import json
import plotly.graph_objs as go

from datetime import timedelta
from functools import reduce
from operator import and_
from plotly.offline import plot

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.timezone import now
from django.views import generic
from django.views.decorators.http import require_POST, require_GET

from rest_framework.generics import ListAPIView

from apps.authentication.forms import (
    ProviderForm,
    UserUpdateForm
)
from apps.product.models import (
    Product,
    ProductCategory,
    PriceColumn
)
from apps.provider.models import (
    ProvideImg,
    Provider,
    Category
)
from apps.user_cabinet.models import (
    PackageStatus,
    ActiveUserStatus,
    Transaction,
    ViewsCountProfile,
    SiteOpenCount,
    OpenNumberCount
)
from apps.user_cabinet.models import (
    Status,
    Upping,
    Cabinet
)
from .forms import (
    ChangePasswordForm,
    PasswordResetForm,
    NewPasswordForm,
    SupportMessageForm
)
from ..tender.models import (
    Tender,
    Country,
    Region,
    City,
    SearchRequest
)
from .models import Contacts, FAQ
from apps.user_cabinet.seriazliers import StatusSerializer
from apps.buyer.models import BuyerImg
from apps.chat.models import Message


# from .freedompay import initiate_payment


def generate_chart(user):
    # Пример данных
    labels = ['Сегодня', 'Вчера', 'Месяц', 'Год']
    print(ViewsCountProfile.get_count_for_today(user))
    page_visitors = [
        ViewsCountProfile.get_count_for_today(user), ViewsCountProfile.get_count_for_yesterday(user),
        ViewsCountProfile.get_count_for_month(user), ViewsCountProfile.get_count_for_year(user)
    ]
    phone_opens = [
        OpenNumberCount.get_count_for_today(user), OpenNumberCount.get_count_for_yesterday(user),
        OpenNumberCount.get_count_for_month(user), OpenNumberCount.get_count_for_year(user)
    ]
    site_transitions = [
        SiteOpenCount.get_count_for_today(user), SiteOpenCount.get_count_for_yesterday(user),
        SiteOpenCount.get_count_for_month(user), SiteOpenCount.get_count_for_year(user)
    ]
    incoming_messages = [
        Message.get_count_for_today_recipient(user.user), Message.get_count_for_yesterday_recipient(user.user),
        Message.get_count_for_month_recipient(user.user), Message.get_count_for_year_recipient(user.user)
    ]
    outgoing_messages = [
        Message.get_count_for_today(user.user), Message.get_count_for_yesterday(user.user),
        Message.get_count_for_month(user.user), Message.get_count_for_year(user.user)
    ]

    fig = go.Figure(data=[
        go.Bar(name='Посетители страницы', x=labels, y=page_visitors, marker_color='navy'),
        go.Bar(name='Открытие телефона', x=labels, y=phone_opens, marker_color='purple'),
        go.Bar(name='Переходы на сайт', x=labels, y=site_transitions, marker_color='lightgray'),
        go.Bar(name='Входящие сообщения', x=labels, y=incoming_messages, marker_color='lightblue'),
        go.Bar(name='Исходящие сообщения', x=labels, y=outgoing_messages, marker_color='skyblue')
    ])

    fig.update_layout(
        barmode='group',
        title='Статистика',
        legend=dict(
            orientation="h",  # Горизонтальная ориентация
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    plot_div = plot(fig, output_type='div')

    return plot_div


User = get_user_model()


class UserStatusListView(LoginRequiredMixin, generic.ListView):
    template_name = 'status_list.html'
    context_object_name = 'statuses'
    model = Status
    queryset = Status.objects.all()


class UppingListView(LoginRequiredMixin, generic.ListView):
    template_name = 'upping_list.html'
    context_object_name = 'uppings'
    model = Upping
    queryset = Upping.objects.all()


class UserDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cabinet/provider_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_keys = ['one', 'two', 'three', 'four', 'five', 'six']

        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider

        images = provider.images.all()
        context_values = (images[i] if i < len(images) else None for i in range(len(context_keys)))
        context.update(dict(zip(context_keys, context_values)))
        contacts = Contacts.load()
        context['contacts'] = contacts
        context['products'] = Product.objects.filter(provider__user=self.request.user)[:5]

        return context


class UserAnketaView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'auth/edit_provider.html'
    model = Provider
    queryset = Provider.objects.all()
    form_class = ProviderForm
    context_object_name = 'form'
    success_url = '/profile/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user.provider

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)

        if form.is_valid():

            country_name = self.request.POST.get('country')
            country = Country.objects.get(title=country_name)
            region_name = self.request.POST.get('region')
            region = Region.objects.get(country=country, title=region_name)
            city_name = self.request.POST.get('city')
            city = City.objects.get(region=region, title=city_name)
            self.object = form.save(commit=False)
            self.object.city = city
            category_ids = self.request.POST.get('category')
            if category_ids:
                categories = category_ids.split(', ')
                numbers = list(map(int, categories))
                categories = Category.objects.filter(id__in=numbers)
                self.object.category.set(categories)
            self.object.comment = 'Ваша анкета на рассмотрении. Пожалуйста, подожтите.'
            self.object.save()
            return redirect(self.get_success_url())
        else:
            print(form.errors)
            return self.form_invalid(form)


class UserAnketaBuyerView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'auth/edit_buyer.html'
    model = Provider
    queryset = Provider.objects.all()
    form_class = ProviderForm
    context_object_name = 'form'
    success_url = '/profile/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user.provider

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект, который будет обновляться
        form = self.form_class(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            self.object = form.save(
                commit=False)  # Сохраняем форму с возможностью дополнительной обработки перед окончательным сохранением
            self.object.comment = 'Ваша анкета на рассмотрении. Пожалуйста, подождите'
            self.object.save()  # Сохраняем изменения в объект
            form.save_m2m()  # Сохраняем ManyToMany поля
            return redirect(self.get_success_url())  # Переадресация на страницу успеха
        else:
            print(form.errors)  # Вывод ошибок на консоль для отладки
            return self.form_invalid(form)


@require_POST
def change_avatar(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    # Получаем файл изображения из запроса
    image_data = request.FILES.get('avatar')
    if not image_data:
        return JsonResponse({'error': 'No image provided'}, status=400)

    # Сохраняем новый аватар в модель пользователя
    if request.user.user_type == 'buyer':
        request.user.buyer.image.save('image', image_data)
    else:
        request.user.provider.image.save('image', image_data)
    request.user.save()

    return JsonResponse({'message': 'Avatar updated successfully'}, status=200)


@require_POST
def change_image(request):
    image_data = request.FILES.get('image')
    if request.user.user_type == 'provider':
        if request.POST.get('oldImage'):
            image = ProvideImg.objects.filter(image__endswith=request.POST.get('oldImage')).first()
            image.image = image_data
            image.save()
        else:
            ProvideImg.objects.create(image=image_data, providers=request.user.provider)
    else:
        if request.POST.get('oldImage'):
            image = BuyerImg.objects.filter(image__endswith=request.POST.get('oldImage')).first()
            image.image = image_data
            image.save()
        else:
            BuyerImg.objects.create(image=image_data, buyer=request.user.buyer)

    return JsonResponse({'message': 'Avatar updated successfully'}, status=200)


class UserSettingsView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'auth/settings.html'
    form_class = UserUpdateForm
    model = User
    success_url = '/profile/settings/'
    context_object_name = 'form'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider
        return context

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial.update({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'phone': user.phone,
            'job_title': user.job_title,

        })
        return initial

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            user = form.save(commit=False)

            provider = user.provider
            provider.is_provider = request.POST.get('is_provider', provider.is_provider)
            provider.save()

            user.save()
            return redirect(self.success_url)
        else:
            print(form.errors)
            return self.form_invalid(form)


class BalanceView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cabinet/balance.html'

    def dispatch(self, request, *args, **kwargs):
        print(request.user.cabinet.balance)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider
        return context


class CreateTenderView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cabinet/create_tender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider
        return context


class TenderListCabinetView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cabinet/tenders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider
        context['searches'] = self.get_user_search_list()
        return context

    def get_user_search_list(self):
        search_list = []
        searches = SearchRequest.objects.filter(user=self.request.user)
        for search in searches:
            search_list.append({
                'id': search.id,
                'name': search.name,
                'city': search.city if search.city else '',
                'date': search.created_at.strftime("%B %d, %Y"),
                'range': self.get_time_range_label(search.created_at),
                'tenders_count': self.get_matching_tenders_count(search),
            })
        return search_list

    def get_matching_tenders_count(self, search):
        queryset = Tender.objects.all()

        # Применяем фильтр include_words
        if search.name:
            words = search.name.split()
            if words:
                query = reduce(and_, (Q(title__icontains=word) | Q(description__icontains=word) for word in words))
                queryset = queryset.filter(query)

        # Применяем фильтр по городу
        if search.city:
            queryset = queryset.filter(user__provider__city__title__icontains=search.city)

        return queryset.count()

    def get_time_range_label(self, date):
        today = now().date()
        delta = today - date

        if delta <= timedelta(days=7):
            return "За неделю"
        elif delta <= timedelta(days=30):
            return "За месяц"
        elif delta <= timedelta(days=365):
            return "За год"
        else:
            return "За все время"


class ProductListCabinetView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'cabinet/products.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.filter(provider__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        categories = ProductCategory.objects.filter(provider__user=self.request.user)
        context['categories'] = categories
        category_tree = self.build_category_tree(categories)
        context['category_tree'] = category_tree
        context['prices'] = PriceColumn.objects.filter(provider__user=self.request.user)
        context['decimal'] = self.request.user.provider.decimal_places
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider
        if self.get_queryset().exists():
            context['has_products'] = True
        else:
            context['has_products'] = False

        return context

    def build_category_tree(self, categories, parent=None, level=0):
        tree = []
        for category in categories:
            if category.parent == parent:
                tree.append((category, level))
                tree.extend(self.build_category_tree(categories, category, level + 1))
        return tree


class FavoritesCabinetView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cabinet/likes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider
        return context


class AnalyticCabinetView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cabinet/analytic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uppings'] = Upping.objects.all()
        context['chart'] = generate_chart(self.request.user.cabinet)
        contacts = Contacts.load()
        context['contacts'] = contacts
        provider, _ = Provider.objects.get_or_create(user=self.request.user)
        context['provider'] = provider
        return context


class TariffsCabinetView(generic.ListView):
    template_name = 'cabinet/tariffs.html'
    model = Status
    queryset = Status.objects.all()
    context_object_name = 'statasus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        context['faqs'] = FAQ.objects.all()
        return context


class StatusListView(ListAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменен!')
            return redirect('view_profile')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'cabinet/change_password.html', {'form': form})


import logging

logger = logging.getLogger(__name__)


def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            logger.info(f"Email from POST: {email}")
            try:
                user = User.objects.get(email=email)
                logger.info(f"User found: {user}")

                # Generate token and uid
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Build reset link
                current_site = get_current_site(request)
                reset_link = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                logger.info(f"Reset link: {reset_link}")

                # Create email
                mail_subject = 'Password Reset Request'
                message = f'Hi {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not make this request, please ignore this email.'

                email = EmailMessage(
                    mail_subject, message, to=[email]
                )

                # Send email
                try:
                    email.send()
                    logger.info(f"Email sent to: {email}")
                    messages.success(request, 'Ссылка для восстановления пароля отправлена на ваш email.')
                except Exception as e:
                    logger.error(f"Error sending email: {e}")
                    messages.error(request, 'Ошибка при отправке email.')

                return redirect('check_email')
            except User.DoesNotExist:
                logger.warning("User not found")
                messages.error(request, 'Пользователь с таким email не найден.')

        else:
            logger.warning("Form is not valid")
            logger.warning(form.errors)
    else:
        form = PasswordResetForm()

    return render(request, 'auth/reset_password.html', {'form': form})


def check_email(request):
    return render(request, 'auth/check_email.html')


def reset_password_confirm(request, uidb64, token):
    """
    View to handle password reset confirmation
    """
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = NewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user, backend=backend)
                return redirect('password_change_success')
        else:
            form = NewPasswordForm(user)
        return render(request, 'auth/reset_password_confirm.html', {'form': form})
    else:
        return redirect('reset_password')


def password_change_success(request):
    return render(request, 'auth/password_change_success.html')


@login_required
def send_message(request):
    if request.method == 'POST':
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('view_profile')
    else:
        form = SupportMessageForm()
    contacts = Contacts.load()
    return render(request, 'cabinet/send_message.html', {'form': form, 'contacts': contacts})


def send_message_logout(request):
    if request.method == 'POST':
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('login')
    else:
        form = SupportMessageForm()

    contacts = Contacts.load()
    return render(request, 'cabinet/send_message.html', {'form': form, 'contacts': contacts})


@require_GET
def add_provider_fav_api(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    provider = get_object_or_404(Provider, id=pk)
    if provider in request.user.cabinet.favorite_providers.all():
        request.user.cabinet.favorite_providers.remove(provider)
        request.user.cabinet.save()
    else:
        request.user.cabinet.favorite_providers.add(provider)
        request.user.cabinet.save()
    return JsonResponse({'Info': 'ok'}, status=200)


@require_GET
def add_product_fav_api(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    product = get_object_or_404(Product, id=pk)
    if product in request.user.cabinet.favorite_products.all():
        request.user.cabinet.favorite_products.remove(product)
        request.user.cabinet.save()
    else:
        request.user.cabinet.favorite_products.add(product)
        request.user.cabinet.save()
    return JsonResponse({'Info': 'ok'}, status=200)


@require_GET
def add_tender_fav_api(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    tender = get_object_or_404(Tender, id=pk)
    if tender in request.user.cabinet.favorite_tenders.all():
        request.user.cabinet.favorite_tenders.remove(tender)
        request.user.cabinet.save()
    else:
        request.user.cabinet.favorite_tenders.add(tender)
        request.user.cabinet.save()
    return JsonResponse({'Info': 'ok'}, status=200)


@require_GET
def add_buyer_fav_api(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    product = get_object_or_404(Product, id=pk)
    if product in request.user.cabinet.favorite_products.all():
        request.user.cabinet.favorite_products.remove(product)
        request.user.cabinet.save()
    else:
        request.user.cabinet.favorite_products.add(product)
        request.user.cabinet.save()
    return JsonResponse({'Info': 'ok'}, status=200)


def delete_provider_fav(request, pk):
    provider = get_object_or_404(Provider, id=pk)
    request.user.cabinet.favorite_providers.remove(provider)
    return redirect('/profile/favorites/')


def delete_product_fav(request, pk):
    product = get_object_or_404(Product, id=pk)
    request.user.cabinet.favorite_products.remove(product)
    return redirect('/profile/favorites/')


def delete_tender_fav(request, pk):
    tender = get_object_or_404(Tender, id=pk)
    request.user.cabinet.favorite_tenders.remove(tender)
    return redirect('/profile/favorites/')


def delete_buyer_fav(request, pk):
    provider = get_object_or_404(Provider, id=pk)
    request.user.cabinet.favorite_providers.remove(provider)
    return redirect('/profile/favorites/')


def add_provider_fav(request, pk):
    provider = get_object_or_404(Provider, id=pk)
    request.user.cabinet.favorite_providers.add(provider)
    return redirect(f'/provider/detail/{pk}/')


def tariff_buy(request):
    status = get_object_or_404(PackageStatus, id=int(request.GET.get('id')))
    user = request.user
    if user.cabinet.balance < status.price:
        return JsonResponse({"Error": "Недостаточно средств"}, status=400)
    if user.cabinet.user_status:
        if user.cabinet.user_status.status.status == status.status:
            user.cabinet.user_status.end_date += datetime.timedelta(days=status.months * 30)
            user.cabinet.balance -= status.price
            user.cabinet.save()
            user.cabinet.user_status.save()
            Transaction.objects.create(
                user=user.cabinet,
                total=-status.price,
                description=f"Транзакция покупки статуса пользователя {status.status.title} - {status.months} месяцев"
            )
            return JsonResponse(data={"Info": "ok"}, status=200)

    user.cabinet.user_status = ActiveUserStatus.objects.create(
        status=status,
        end_date=datetime.date.today() + datetime.timedelta(days=status.months * 30)
    )
    Transaction.objects.create(
        user=user.cabinet,
        total=-status.price,
        description=f"Транзакция покупки статуса пользователя {status.status.title}"
    )
    user.cabinet.balance -= status.price
    user.cabinet.save()
    return JsonResponse(data={"Info": "ok"}, status=200)


def redirect_to_site(request, pk):
    provider = get_object_or_404(Cabinet, id=pk)
    SiteOpenCount.objects.create(user=provider)
    return redirect(provider.user.provider.web_site)


def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'tariffs.html', {'faqs': faqs})


def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        # Получаем объект транзакции или возвращаем ошибку 404, если транзакция не найдена
        transaction = get_object_or_404(Transaction, id=transaction_id)

        # Удаляем транзакцию
        transaction.delete()

        # После удаления перенаправляем пользователя на страницу с историей платежей или другую нужную страницу
        return redirect('balance')


from .utils import generate_signature
from .freedompay import send_post_request
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import uuid


@csrf_exempt
def init_payment(request):
    if request.method == 'POST':
        # Generate unique pg_order_id
        pg_order_id = str(uuid.uuid4())

        # Generate a random string for pg_salt
        pg_salt = uuid.uuid4().hex

        # Get pg_merchant_id from settings
        pg_merchant_id = settings.PAYBOX_MERCHANT_ID

        # Get data from request body
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            pg_amount = body.get('pg_amount')
            pg_description = body.get('pg_description', 'Пополнение баланса')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'})

        # Create a dictionary with data for the request
        request_data = {
            'pg_order_id': pg_order_id,
            'pg_merchant_id': pg_merchant_id,
            'pg_amount': pg_amount,
            'pg_description': pg_description,
            'pg_salt': pg_salt,
        }

        # Generate the signature for the request data
        signature = generate_signature(request_data, 'init_payment.php')
        request_data['pg_sig'] = signature

        # Send request to API to initiate the payment
        response = send_post_request('/init_payment.php', request_data)

        if response.get('pg_redirect_url'):
            # Save transaction data to the database
            Transaction.objects.create(
                user=request.user.cabinet,
                pg_payment_id=response.get('pg_payment_id'),
                total=pg_amount,
                description=pg_description
            )

        return JsonResponse(response)
    else:
        # If the request is not POST, return an error
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def freedompay_success(request):
    if request.method == 'GET':
        try:
            pg_payment_id = request.GET.get('pg_payment_id')
            if not pg_payment_id:
                user = Cabinet.objects.get(user_id=request.user.id)
                transaction = Transaction.objects.filter(user=user).exclude(status='success').order_by('-id').first()
                if transaction:
                    transaction.status = 'success'
                    transaction.save()
                    pg_payment_id = transaction.pg_payment_id
                else:
                    return redirect('balance')


        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body'})

        pg_salt = uuid.uuid4().hex
        pg_merchant_id = settings.PAYBOX_MERCHANT_ID

        request_data = {
            'pg_merchant_id': pg_merchant_id,
            'pg_payment_id': pg_payment_id,
            'pg_salt': pg_salt,
        }

        signature = generate_signature(request_data, 'get_status3.php')
        request_data['pg_sig'] = signature

        response = send_post_request('/get_status3.php', request_data)

        transactions = Transaction.objects.filter(pg_payment_id=pg_payment_id)

        if response.get('pg_payment_status') == 'success':
            for transaction in transactions:
                user_cabinet = transaction.user
                pg_amount = response.get('pg_amount')
                user_cabinet.balance += int(pg_amount)
                user_cabinet.save()
                transaction.status = 'success'
                transaction.save()
        elif response.get('pg_payment_status') == 'error':
            for transaction in transactions:
                transaction.status = 'failed'
                transaction.save()

        return redirect('balance')
    else:
        return JsonResponse({'error': 'Invalid request method'})
