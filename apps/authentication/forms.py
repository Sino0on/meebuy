from django import forms

from .models import User


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone', 'username', 'password1', 'password2')

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
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'avatar', 'position']  

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = False  
