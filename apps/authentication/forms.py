from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.auth.forms import UserChangeForm
from apps.product.models import ProductCategory
from .models import User
from apps.provider.models import Provider
from django.utils.translation import gettext_lazy as _
from django.contrib import admin


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'border border-[#E6E6E6] bg-[#F9F9F9] rounded-2xl px-5 py-3 text-[#737373]',
        'placeholder': 'Email *',
    }))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'border border-[#E6E6E6] bg-[#F9F9F9] rounded-2xl px-5 py-3 text-[#737373]',
        'placeholder': '+996 *** *** ***',
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'border border-[#E6E6E6] bg-[#F9F9F9] rounded-2xl px-5 py-3 text-[#737373]',
        'placeholder': 'ФИО',
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'password-input border border-[#E6E6E6] bg-[#F9F9F9] rounded-2xl px-5 py-3 text-[#737373]',
        'placeholder': '********'
    }), validators=[validate_password])
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'password-input border border-[#E6E6E6] bg-[#F9F9F9] rounded-2xl px-5 py-3 text-[#737373]',
        'placeholder': '********'
    }))

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'password1', 'password2')

    def validate_password2(self, password2):
        if self.cleaned_data.get("password1") != password2:
            raise forms.ValidationError(_("Пароли не совпадают."))

        return password2

    def validate_password1(self, password1):
        if not validate_password(password1):
            return password1

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already taken")
        return phone
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        self.clean_password2()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        

class UserTypeSelectionForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('provider', 'Поставщик'),
        ('buyer', 'Покупатель'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='Выберите тип пользователя')


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'border border-[#E6E6E6] w-[100%] bg-[#F9F9F9] rounded-2xl px-5 py-3 text-[#737373]',
        'placeholder': 'example@mail.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'password-input border border-[#E6E6E6] bg-[#F9F9F9] rounded-2xl px-5 py-3 text-[#737373]',
        'placeholder': '*******',
    }))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'avatar', 'position']  

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = False  


class ProviderForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ProductCategory.objects.all(),
        widget=AutocompleteSelect(Provider._meta.get_field('category').remote_field, admin.site)
    )

    class Meta:
        fields = '__all__'
        model = Provider


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'input  mt-3.5 lg-md:mt-[18px]',
        'placeholder': 'Email *',
    }))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'input  mt-3.5 lg-md:mt-[18px]',
        'placeholder': '+996 *** *** ***',
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'input  mt-3.5 lg-md:mt-[18px]',
        'placeholder': 'ФИО',
    }))
    job_title = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input  mt-3.5 lg-md:mt-[18px]',
        'placeholder': 'Не указана должность',
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance

        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            raise forms.ValidationError('Этот email уже используется другим пользователем.')

        return email

    def clean_job_title(self):
        job_title = self.cleaned_data.get('job_title')

        return job_title

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'job_title')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = self.instance
        if User.objects.filter(phone=phone).exclude(pk=user.pk).exists():
            raise forms.ValidationError("Этот номер телефона уже используется другим пользователем")
        return phone
