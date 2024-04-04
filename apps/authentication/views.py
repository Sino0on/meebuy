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

        authenticated_user = authenticate(email=user.email, password=form.cleaned_data['password1'])
        if authenticated_user is not None:
            auth_login(self.request, authenticated_user)

        return super().form_valid(form)


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('view_profile')  

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            auth_login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(None, "Неверный email или пароль")
        return self.render_to_response(self.get_context_data(form=form))


class SelectUserTypeView(FormView):
    form_class = UserTypeSelectionForm
    template_name = 'select_user_type.html'
    success_url = reverse_lazy('view_profile')  

    def form_valid(self, form):
        if self.request.user.is_authenticated:  
            user_profile = self.request.user 
            user_profile.user_type = form.cleaned_data['user_type']  
            user_profile.save()  
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
    