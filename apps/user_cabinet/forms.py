from django import forms
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext as _
from .models import SupportMessage


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'input'
        self.fields['new_password1'].widget.attrs['class'] = 'input'
        self.fields['new_password2'].widget.attrs['class'] = 'input'


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email *'})
    )


class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'input'
        self.fields['new_password2'].widget.attrs['class'] = 'input'


class SupportMessageForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['name', 'phone', 'email', 'message', 'regret_to_register', 'agree_to_policy']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'border border-[#E6E6E6] bg-[#F9F9F9] outline-none rounded-[15px] w-full px-5 py-3',
                'placeholder': 'Как к Вам обращаться'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'border border-[#E6E6E6] bg-[#F9F9F9] outline-none rounded-[15px] w-full px-5 py-3',
                'placeholder': '+996 XXX XXX XXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'border border-[#E6E6E6] bg-[#F9F9F9] outline-none rounded-[15px] w-full px-5 py-3',
                'placeholder': 'example@gmail.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'border border-[#E6E6E6] bg-[#F9F9F9] outline-none rounded-[15px] w-full px-5 py-3',
                'placeholder': 'Например: Здравствуйте, интересуют наушники оптом'
            }),
            'regret_to_register': forms.RadioSelect(attrs={
                'class': 'border border-[#E6E6E6] bg-[#F9F9F9] outline-none rounded-[15px] w-middle'
                         ' px-5 py-3'
            }),
            'agree_to_policy': forms.CheckboxInput(attrs={'class': 'h-6 w-6'}),
        }
