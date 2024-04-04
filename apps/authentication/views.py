from django.views.generic import TemplateView, FormView, UpdateView, RedirectView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone


from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserTypeSelectionForm


class HomeView(TemplateView):
    template_name = 'home.html'


class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('select_user_type')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.auth_provider = False
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('select_user_type')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            auth_login(self.request, user)
            if user.auth_provider:
                self.success_url = reverse_lazy('select_user_type')
            else:
                self.success_url = reverse_lazy('view_profile')
            return super().form_valid(form)
        else:
            form.add_error(None, "Неверный email или пароль")
            return self.form_invalid(form)


class SelectUserTypeView(FormView):
    form_class = UserTypeSelectionForm
    template_name = 'select_user_type.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if self.request.user.is_authenticated:  # Проверка аутентификации пользователя
            user_profile = self.request.user  # Получаем профиль пользователя
            user_profile.user_type = form.cleaned_data['user_type']  # Сохраняем выбранный тип пользователя
            user_profile.save()  # Сохраняем изменения
            if hasattr(self.request.user, 'auth_provider') and self.request.user.auth_provider:  # Проверка наличия и значения атрибута auth_provider
                self.success_url = reverse_lazy('view_profile')
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ViewProfile(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('view_profile')

    def get_object(self):
        return self.request.user


@login_required
def login_redirect(request):
    if not request.user.user_type:  
        return redirect('/select_user_type/')
    else:
        return redirect('/profile/')
    