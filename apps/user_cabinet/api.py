import datetime

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.user_cabinet.models import PackageStatus, ActiveUserStatus, ActiveUpping, Transaction, Upping
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN


User = get_user_model()


class BuyStatusView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        status = get_object_or_404(PackageStatus, id=kwargs['pk'])
        user = request.user
        if not user.cabinet:
            return Response(status=HTTP_403_FORBIDDEN)
        if user.cabinet.balance < status.price:
            return Response(data={"Info": "Недостаточно средств"}, status=HTTP_400_BAD_REQUEST)
        user.cabinet.user_status = ActiveUserStatus.objects.create(
            status=status,
            end_date=datetime.date.today() + datetime.timedelta(days=status.months*30)
        )
        Transaction.objects.create(
            user=user.cabinet,
            total=-status.price,
            description=f"Транзакция покупки статуса пользователя {status.status.title}"
        )
        user.cabinet.balance -= status.price
        user.cabinet.save()
        return Response(status=HTTP_200_OK)


class BuyUppingView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        upping = get_object_or_404(Upping, id=kwargs['pk'])
        user = request.user
        if not user.cabinet:
            return Response(data={"Error": "Неавторизованный"}, status=HTTP_403_FORBIDDEN)
        if user.cabinet.balance < upping.price:
            return Response(data={"Error": "Недостаточно средств"}, status=HTTP_400_BAD_REQUEST)
        user.cabinet.is_upping = ActiveUpping.objects.create(
            upping=upping,
            end_date=datetime.date.today() + datetime.timedelta(days=upping.days)
        )
        Transaction.objects.create(
            user=user.cabinet,
            total=-upping.price,
            description=f"Транзакция покупки топ магазина на - {upping.days} дней"
        )
        user.cabinet.balance -= upping.price
        user.cabinet.save()
        return Response(data={"Info": "Успешно подключено"}, status=HTTP_200_OK)
