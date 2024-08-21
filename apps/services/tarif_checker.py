from django.contrib import messages

from apps.user_cabinet.models import OpenNumberCount


def check_user_status_and_open_number(request):
    if request.user.is_authenticated:
        if request.user.cabinet.user_status:
            if request.user.cabinet.user_status.status:
                OpenNumberCount.objects.create(
                    user=request.user.cabinet
                )
                return "open"
            else:
                messages.error(request, 'У вас закончились открытия на сегодня.')
                return None
        else:
            messages.error(request, 'У вас не подключен ни один тариф.')
            return None
    else:
        messages.error(request, 'Вы не авторизованы .')
        return None
