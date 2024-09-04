from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db.models import When, Case, BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView, UpdateView, RedirectView
from django.views.generic.edit import FormView

from apps.authentication.forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserProfileForm,
    UserTypeSelectionForm
)
from apps.authentication.token import account_activation_token
from apps.product.models import Product
from apps.provider.models import Provider, Category
from apps.tender.models import Tender, Country
from apps.user_cabinet.models import Cabinet, Contacts


class HomeView(TemplateView):
    template_name = 'auth/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_recommended=True).order_by('-id')[:6]
        context['rec_products'] = products if products else Product.objects.all().order_by('?')[:6]
        context['new_products'] = Product.objects.all().order_by('-id')[:6]
        context['new_providers'] = Provider.objects.filter(is_modered=True, is_provider=True).order_by('-id')[:4]
        categories = Category.objects.filter(category=None, is_main_category=True).annotate(
            has_children=Case(
                When(categor__isnull=False, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        context['categories'] = categories.distinct()

        context['tenders'] = Tender.objects.all()[:8]
        contacts = Contacts.load()
        context['contacts'] = contacts
        context['home'] = True

        return context


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'auth/auth.html'
    success_url = reverse_lazy('view_profile')

    def post(self, request, *args, **kwargs):
        if request.POST.get('password1'):
            print(request.POST)
            register_form = UserRegistrationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=True)
                code = self.request.POST.get('country_code')
                phone = self.request.POST.get('phone')
                user.phone = str(code) + str(phone)
                Provider.objects.create(user=user)
                if self.request.POST.get('user-role') == 'provider':
                    print(self.request.POST.get('user-role'))
                    user.provider.is_provider = True
                else:
                    user.provider.is_provider = False

                user.provider.save()
                Cabinet.objects.get_or_create(user=user)
                current_site = get_current_site(request)
                protocol = 'https' if request.is_secure() else 'http'
                mail_subject = 'Ссылка для активации была отправлена на ваш адрес электронной почты'
                message = render_to_string('auth/acc_active_email.html', {
                    'user': user,
                    'protocol': protocol,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = register_form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                authenticated_user = authenticate(email=user.email, password=register_form.clean_password2())
                if authenticated_user is not None:
                    auth_login(self.request, authenticated_user)
                    if user.provider.is_provider == False:
                        return redirect(reverse_lazy('buyer_step'))

                    return redirect(reverse_lazy('home'))

                    # return redirect(reverse_lazy('choice'))
                else:
                    messages.error(request, 'Ошибка аутентификации пользователя.')
                    return redirect(reverse_lazy('home'))


            else:
                self.request.session['form_data'] = request.POST
                self.request.session['form_errors'] = register_form.errors
                return redirect('register')

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {'register_form': UserRegistrationForm()}
        context.update(super().get_context_data(**kwargs))
        context['countries'] = Country.objects.all()
        return context

    def form_valid(self, form):
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=username, password=password)
        if user is not None and user.is_active:
            auth_login(self.request, user)  # Аутентификация пользователя

            # Проверяем, входил ли пользователь ранее и является ли он поставщиком
            if not user.login_before and not user.provider.is_provider:
                user.login_before = True  # Обновляем флаг первого входа
                user.save(update_fields=['login_before'])
                return redirect('buyer_step')  # Путь для покупателей, входящих в первый раз
            else:
                return redirect('home')  # Стандартный путь для входа
        else:
            # Если аутентификация не удалась, добавляем сообщение об ошибке
            messages.error(self.request, 'Неверный логин или пароль.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        self.request.session['form_data'] = form.data
        messages.error(self.request, 'Неверный email или пароль.')

        return redirect('authentication')


class RegistrationView(LoginView):
    template_name = 'auth/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form_data' in self.request.session:
            data = self.request.session.pop('form_data')
            errors = self.request.session.pop('form_errors', None)
            register_form = UserRegistrationForm(data)

            if errors:
                # Инициализация _errors как пустого словаря, если он None
                register_form._errors = register_form._errors or {}
                for field, error_list in errors.items():
                    for error in error_list:
                        if field not in register_form._errors:
                            register_form._errors[field] = register_form.error_class()
                        register_form._errors[field].append(error)
                register_form.is_valid()  # Просто вызываем для обновления состояния формы после добавления ошибок

            context['register_form'] = register_form
        else:
            context['register_form'] = UserRegistrationForm()
        context['countries'] = Country.objects.all()
        return context


class AuthenticationView(LoginView):
    template_name = 'auth/authentication.html'


class SelectUserTypeView(LoginRequiredMixin, FormView):
    form_class = UserTypeSelectionForm
    template_name = 'auth/auth_choice.html'
    success_url = reverse_lazy('view_profile')

    def dispatch(self, request, *args, **kwargs):
        user_profile = self.request.user
        if user_profile.is_authenticated:
            if user_profile.user_type and user_profile.provider:
                return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_profile = self.request.user
        user_profile.user_type = form.cleaned_data['user_type']
        user_profile.save()

        if form.cleaned_data['user_type'] == 'provider':
            provider, created = Provider.objects.get_or_create(user=user_profile)
            provider.is_provider = True
            provider.save()
        else:
            provider, created = Provider.objects.get_or_create(user=user_profile)
            provider.is_provider = False
            provider.save()
            return redirect('buyer_step')

        return super().form_valid(form)


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ViewProfile(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'auth/profile.html'
    success_url = reverse_lazy('view_profile')

    def get_object(self):
        return self.request.user


@login_required
def login_redirect(request):
    # if not request.user.user_type:
    #     return redirect('/select_user_type/')
    # else:
    return redirect('/profile/')


class SelectAuthUserTypeView(FormView):
    form_class = UserTypeSelectionForm
    template_name = 'auth/cabinet_choice.html'
    success_url = reverse_lazy('view_profile')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.user_type:
            return redirect(reverse_lazy('view_profile'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            user_profile = self.request.user
            user_profile.user_type = form.cleaned_data['user_type']
            print(form.cleaned_data['user_type'])
            user_profile.save()
            if form.cleaned_data['user_type'] == 'provider':
                Provider.objects.get_or_create(user=user_profile, is_provider=True)
            elif user_profile.user_type == 'buyer':
                Provider.objects.get_or_create(user=user_profile, is_provider=False)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


def cabinet_create(request):
    try:
        cabinet = request.user.cabinet
    except ObjectDoesNotExist:
        cabinet = Cabinet.objects.create(user=request.user)
    return redirect(reverse_lazy('choice'))


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.provider.is_active = True
        user.provider.save()
        messages.success(request, 'Ваш аккаунт успешно активирован!')
        return redirect('view_profile')
    else:
        return HttpResponse('Activation link is invalid!')



# REGISTER V2
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .forms import CustomUserCreationForm
import random
import string
from django.core.mail import send_mail

User = get_user_model()


def register_v2(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Генерация случайного пароля
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            # Создание пользователя
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(password)  # Хеширование пароля
            )

            # Отправка пароля на почту пользователя
            send_mail(
                'Ваш пароль для входа на сайт',
                f'Ваш пароль: {password}\nИспользуйте его для входа на сайт.',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            print(request.POST.get('user-role'))
            if request.POST.get('user-role') == 'provider':
                provider, _ = Provider.objects.get_or_create(user=user)
                provider.is_provider = True
                provider.is_active = True
                provider.save()

            else:
                provider, _ = Provider.objects.get_or_create(user=user)
                provider.is_provider = False
                provider.is_active = True
                provider.save()

            messages.success(request, 'Регистрация прошла успешно, мы выслали ваш пароль вам на почту!')
            return redirect('authentication')

    else:
        form = CustomUserCreationForm()
    countries = Country.objects.all()
    return render(request, 'auth/authentication.html', {'form': form, 'countries': countries})