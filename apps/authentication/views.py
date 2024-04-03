from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login

from .forms import UserRegistrationForm, UserProfileForm, UserTypeSelectionForm, UserLoginForm


def home(request): 
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.auth_provider = False
            form.save()
            return redirect('select_user_type')  
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)  
                return redirect('select_user_type') if user.auth_provider else redirect('view_profile')
            else:
                form.add_error(None, "Неверный email или пароль")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def select_user_type(request):
    if request.method == 'POST':
        form = UserTypeSelectionForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']

            return redirect('login')
    else:
        form = UserTypeSelectionForm()
    return render(request, 'select_user_type.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def view_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile') 
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})
