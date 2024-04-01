from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
