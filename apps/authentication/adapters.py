from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from apps.user_cabinet.models import Cabinet


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        Cabinet.objects.get_or_create(user=user)
        return user
