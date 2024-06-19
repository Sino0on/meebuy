from django.shortcuts import render

from .models import StaticPage


def privacy_policy_view(request):
    privacy_policy, created = StaticPage.objects.get_or_create(slug='provicy')
    if created:
        privacy_policy.title = 'Политика конфиденциальности'
        privacy_policy.description = 'Здесь вы можете создать описание "Политика конфиденциальности" для вашего сайта meebuy.ru'
        privacy_policy.save()
        return render(request, 'staticpages/privacy_policy.html', {'policy': privacy_policy})
    else:
        return render(request, 'staticpages/privacy_policy.html', {'policy': privacy_policy})


def rules_view(request):
    rules, created = StaticPage.objects.get_or_create(slug='rules')
    if created:
        rules.title = 'Правила'
        rules.description = 'Здесь вы можете создать описание "Правила" для вашего сайта meebuy.ru'
        rules.save()
        return render(request, 'staticpages/rules.html', {'rules': rules})
    else:
        return render(request, 'staticpages/rules.html', {'rules': rules})


def banner_view(request):
    banner, created = StaticPage.objects.get_or_create(slug='banners')
    if created:
        banner.title = 'Баннер'
        banner.description = 'Здесь вы можете создать описание "Баннер" для вашего сайта meebuy.ru'
        banner.save()
        return render(request, 'staticpages/banner.html', {'banner': banner})
    else:
        return render(request, 'staticpages/banner.html', {'banner': banner})
