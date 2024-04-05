from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.user_cabinet.models import Status, Upping
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class UserStatusListView(LoginRequiredMixin, generic.ListView):
    template_name = 'status_list.html'
    context_object_name = 'statuses'
    model = Status
    queryset = Status.objects.all()


class UppingListView(LoginRequiredMixin, generic.ListView):
    template_name = 'upping_list.html'
    context_object_name = 'uppings'
    model = Upping
    queryset = Upping.objects.all()

# @login_required()
# def buy_status(request):
#     pass
