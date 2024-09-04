from django.contrib import messages

from apps.chat.models import Chat
from apps.product.models import Product
from apps.user_cabinet.models import OpenNumberCount
from datetime import datetime


def check_user_status_and_open_number(request):
    today = datetime.now().date()
    if request.user.is_authenticated:
        if request.user.cabinet.user_status:
            if request.user.cabinet.user_status.end_date > today and request.user.cabinet.user_status.is_active:
                if request.user.cabinet.user_status.status:
                    if request.user.cabinet.user_status.status:
                        can_be_opened = request.user.cabinet.user_status.status.status.quantity_opening
                        count_today = OpenNumberCount.get_count_for_today(request.user.cabinet)
                        if can_be_opened > count_today:
                            OpenNumberCount.objects.create(
                                user=request.user.cabinet
                            )
                            return "open"
                        else:
                            messages.error(request, 'У вас закончились открытия на сегодня.')
                            return None
                    else:
                        messages.error(request, 'У вас закончились открытия на сегодня.')
                        return None
            else:
                messages.error(request, 'Ваш тариф не активен.')
                request.user.cabinet.user_status.is_active = False
                request.user.cabinet.user_status.save()
                return None
        else:
            messages.error(request, 'У вас не подключен ни один тариф.')
            return None
    else:
        messages.error(request, 'Вы не авторизованы .')
        return None


def check_user_status_and_create_new_chat(request):
    today = datetime.now().date()
    if request.user.is_authenticated:
        if request.user.cabinet.user_status:
            print(request.user.cabinet.user_status.end_date, today)
            print(request.user.cabinet.user_status.is_active)

            if request.user.cabinet.user_status.end_date > today:
                if request.user.cabinet.user_status.status:
                    can_be_created = request.user.cabinet.user_status.status.status.dayly_message
                    count_today = Chat.get_count_for_today(request.user)
                    print(count_today, can_be_created)
                    if can_be_created >= count_today:
                        return True
                    else:
                        messages.error(request, 'Вы не можете открыть больше чатов за сегодня.')
                        return None
                else:
                    messages.error(request, 'Вы не можете открыть больше чатов за сегодня.')
                    return None
            else:
                messages.error(request, 'Ваш тариф истек.')
                request.user.cabinet.user_status.is_active = False
                request.user.cabinet.user_status.save()
                return None
        else:
            messages.error(request, 'У вас не подключен ни один тариф.')
            return None
    else:
        messages.error(request, 'Вы не авторизованы .')
        return None


def check_user_status_and_create_new_product(request):
    today = datetime.now().date()
    if request.user.is_authenticated:
        if request.user.cabinet.user_status:
            if request.user.cabinet.user_status.end_date > today and request.user.cabinet.user_status.is_active:
                if request.user.cabinet.user_status.status:
                    can_be_created = request.user.cabinet.user_status.status.status.dayly_message
                    count_today = Chat.get_count_for_today(request.user)
                    if can_be_created > count_today:

                        return True
                    else:
                        messages.error(request, 'Вы не можете открыть больше чатов за сегодня.')
                        return None
                else:
                    messages.error(request, 'Вы не можете открыть больше чатов за сегодня.')
                    return None
            else:
                messages.error(request, 'Ваш тариф истек.')
                request.user.cabinet.user_status.is_active = False
                request.user.cabinet.user_status.save()
                return None
        else:
            messages.error(request, 'У вас не подключен ни один тариф.')
            return None
    else:
        messages.error(request, 'Вы не авторизованы .')
        return None