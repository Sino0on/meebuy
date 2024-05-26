from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from rest_framework.generics import ListAPIView, GenericAPIView
from apps.authentication.forms import ProviderForm, UserUpdateForm
from apps.product.models import Product, ProductCategory
from apps.user_cabinet.models import Status, Upping
from apps.provider.models import ProvideImg, Provider
from apps.buyer.models import BuyerImg
from django.contrib.auth import get_user_model
from django.views import generic
from apps.user_cabinet.seriazliers import StatusSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from .forms import ChangePasswordForm, PasswordResetForm, NewPasswordForm, SupportMessageForm
from .models import Contacts

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


class UserDetailView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/provider_profile.html'

    def get_template_names(self):
        if self.request.user.user_type == 'buyer':
            template_name = 'cabinet/buyer_profile.html'
        else:
            template_name = self.template_name
        return template_name

    def get_context_data(self, **kwargs):
        print(self.request.user.user_type)
        context = super().get_context_data(**kwargs)
        context_keys = ['one', 'two', 'three', 'four', 'five', 'six']
        if self.request.user.user_type == 'buyer':
            images = self.request.user.buyer.images.all()
        else:
            images = self.request.user.provider.images.all()
        context_values = (images[i] if i < len(images) else None for i in range(len(context_keys)))
        context.update(dict(zip(context_keys, context_values)))
        contacts = Contacts.load()
        context['contacts'] = contacts

        return context


class UserAnketaView(generic.UpdateView, LoginRequiredMixin):
    template_name = 'auth/edit_provider.html'
    model = Provider
    queryset = Provider.objects.all()
    form_class = ProviderForm
    context_object_name = 'form'

    def get_object(self, queryset=None):
        return self.request.user.provider

    def get_template_names(self):
        if self.request.user.user_type == 'buyer':
            print('buyter')
            template_name = 'auth/edit_buyer.html'
        else:
            template_name = self.template_name
            print('provider')
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # print(form)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("Valid form data:", form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid form data:", form.data)
        print("Errors:", form.errors)
        return super().form_invalid(form)


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


class UserSettingsView(generic.UpdateView, LoginRequiredMixin):
    template_name = 'auth/settings.html'
    form_class = UserUpdateForm
    model = User
    context_object_name = 'form'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class BalanceView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/balance.html'

    def dispatch(self, request, *args, **kwargs):
        print(request.user.cabinet.balance)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class CreateTenderView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/create_tender.html'


class TenderListCabinetView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/tenders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class ProductListCabinetView(generic.ListView, LoginRequiredMixin):
    object = Product
    template_name = 'cabinet/products.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class FavoritesCabinetView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/likes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class AnalyticCabinetView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/analytic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uppings'] = Upping.objects.all()
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class TariffsCabinetView(generic.ListView, LoginRequiredMixin):
    template_name = 'cabinet/tariffs.html'
    model = Status
    queryset = Status.objects.all()
    context_object_name = 'statasus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
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
    return JsonResponse({'ok': 'ok'}, status=200)


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
    return JsonResponse({'ok': 'ok'}, status=200)


def delete_provider_fav(request, pk):
    provider = get_object_or_404(Provider, id=pk)
    request.user.cabinet.favorite_providers.remove(provider)
    return redirect('/profile/favorites/')


def add_provider_fav(request, pk):
    provider = get_object_or_404(Provider, id=pk)
    request.user.cabinet.favorite_providers.add(provider)
    return redirect(f'/provider/detail/{pk}/')
