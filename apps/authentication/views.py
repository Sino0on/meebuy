from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView, FormView, UpdateView, RedirectView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout, login as auth_login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, get_object_or_404
from django.contrib import messages


from apps.authentication.forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserTypeSelectionForm
from apps.authentication.token import account_activation_token
from apps.buyer.models import Buyer
from apps.product.models import Product
from apps.tender.models import Tender
from apps.provider.models import Provider, Category
from apps.user_cabinet.models import Cabinet, Contacts


class HomeView(TemplateView):
    template_name = 'auth/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rec_products'] = Product.objects.all().order_by('-id')[:6]
        context['new_products'] = Product.objects.all().order_by('-id')[:6]
        context['new_providers'] = Provider.objects.filter(is_modered=True, is_provider=True)[:4]
        context['categories'] = Category.objects.filter(category=None)
        context['tenders'] = Tender.objects.all()[:8]
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'auth/auth.html'
    success_url = reverse_lazy('view_profile')

    def post(self, request, *args, **kwargs):
        if request.POST.get('password1'):
            register_form = UserRegistrationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.save()
                Cabinet.objects.get_or_create(user=user)
                current_site = get_current_site(request)
                print(current_site)
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
                    return redirect(reverse_lazy('choice'))
                else:
                    messages.error(request, 'Ошибка аутентификации пользователя.')
                    return redirect(reverse_lazy('home'))


            else:
                print(register_form.errors)
                return self.render_to_response(self.get_context_data(register_form=register_form))

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {'register_form': UserRegistrationForm()}
        context.update(super().get_context_data(**kwargs))
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None and user.is_active:  # Проверка, что пользователь активирован
            auth_login(self.request, user)
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(None, "Неверный email или пароль")
        return self.render_to_response(self.get_context_data(form=form))


class SelectUserTypeView(LoginRequiredMixin, FormView):
    form_class = UserTypeSelectionForm
    template_name = 'auth/auth_choice.html'
    success_url = reverse_lazy('view_profile')  

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
    if not request.user.user_type:  
        return redirect('/select_user_type/')
    else:
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
