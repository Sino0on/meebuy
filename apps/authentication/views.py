from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, authenticate
from apps.authentication.forms import LoginForm


class LoginView(generic.TemplateView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('/')
        return render(request, self.template_name, self.get_context_data())
