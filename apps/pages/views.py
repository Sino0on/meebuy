from .models import StaticPage
from django.shortcuts import render


def privacy_policy_view(request):
    privacy_policy, created = StaticPage.objects.get_or_create(slug='provicy')
    if created:
        privacy_policy.title = 'Политики конфиденциальности'
        privacy_policy.description = 'Здесь вы можете создать описание "Политики конфиденциальности" для вашего сайта meebuy.ru'
        privacy_policy.save()
        return render(request, 'staticpages/privacy_policy.html', {'policy': privacy_policy})
    else:
        return render(request, 'staticpages/privacy_policy.html', {'policy': privacy_policy})


def rules_view(request):
    rules, created = StaticPage.objects.get_or_create(slug='rules')
    if created:
        rules.title = 'Политики конфиденциальности'
        rules.description = 'Здесь вы можете создать описание "Политики конфиденциальности" для вашего сайта meebuy.ru'
        rules.save()
        return render(request, 'staticpages/rules.html', {'rules': rules})
    else:
        return render(request, 'staticpages/rules.html', {'rules': rules})
