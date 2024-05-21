from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.generics import ListAPIView
from apps.authentication.forms import ProviderForm, UserUpdateForm
from apps.user_cabinet.models import Status, Upping
from apps.provider.models import ProvideImg, Provider, Category
from apps.buyer.models import BuyerImg
from django.contrib.auth import get_user_model
from django.views import generic
from apps.user_cabinet.seriazliers import StatusSerializer
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


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


class UserDetailView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/provider_profile.html'

    def get_template_names(self):
        if self.request.user.user_type == 'buyer':
            template_name = 'cabinet/buyer_profile.html'
        else:
            template_name = self.template_name
        return template_name

    def get_context_data(self, **kwargs):
        print(self.request.user.user_type)
        context = super().get_context_data(**kwargs)
        context_keys = ['one', 'two', 'three', 'four', 'five', 'six']
        if self.request.user.user_type == 'buyer':
            images = self.request.user.buyer.images.all()
        else:
            images = self.request.user.provider.images.all()
        context_values = (images[i] if i < len(images) else None for i in range(len(context_keys)))
        context.update(dict(zip(context_keys, context_values)))

        return context


class UserAnketaView(generic.UpdateView, LoginRequiredMixin):
    template_name = 'auth/edit_provider.html'
    model = Provider
    queryset = Provider.objects.all()
    form_class = ProviderForm
    context_object_name = 'form'

    def get_object(self, queryset=None):
        return self.request.user.provider

    def get_template_names(self):
        if self.request.user.user_type == 'buyer':
            print('buyter')
            template_name = 'auth/edit_buyer.html'
        else:
            template_name = self.template_name
            print('provider')
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # print(form)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("Valid form data:", form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid form data:", form.data)
        print("Errors:", form.errors)
        return super().form_invalid(form)


@require_POST
def change_avatar(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    # Получаем файл изображения из запроса
    image_data = request.FILES.get('avatar')
    if not image_data:
        return JsonResponse({'error': 'No image provided'}, status=400)

    # Сохраняем новый аватар в модель пользователя
    if request.user.user_type == 'buyer':
        request.user.buyer.image.save('image', image_data)
    else:
        request.user.provider.image.save('image', image_data)
    request.user.save()

    return JsonResponse({'message': 'Avatar updated successfully'}, status=200)


@require_POST
def change_image(request):
    image_data = request.FILES.get('image')
    if request.user.user_type == 'provider':
        if request.POST.get('oldImage'):
            image = ProvideImg.objects.filter(image__endswith=request.POST.get('oldImage')).first()
            image.image = image_data
            image.save()
        else:
            ProvideImg.objects.create(image=image_data, providers=request.user.provider)
    else:
        if request.POST.get('oldImage'):
            image = BuyerImg.objects.filter(image__endswith=request.POST.get('oldImage')).first()
            image.image = image_data
            image.save()
        else:
            BuyerImg.objects.create(image=image_data, buyer=request.user.buyer)

    return JsonResponse({'message': 'Avatar updated successfully'}, status=200)


class UserSettingsView(generic.UpdateView, LoginRequiredMixin):
    template_name = 'auth/settings.html'
    form_class = UserUpdateForm
    model = User
    context_object_name = 'form'

    def get_object(self, queryset=None):
        return self.request.user


class BalanceView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/balance.html'

    def dispatch(self, request, *args, **kwargs):
        print(request.user.cabinet.balance)
        return super().dispatch(request, *args, **kwargs)


class CreateTenderView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/create_tender.html'


class TenderListCabinetView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/tenders.html'


class ProductListCabinetView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/products.html'


class FavoritesCabinetView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/likes.html'


class AnalyticCabinetView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'cabinet/analytic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uppings'] = Upping.objects.all()
        return context


class TariffsCabinetView(generic.ListView, LoginRequiredMixin):
    template_name = 'cabinet/tariffs.html'
    model = Status
    queryset = Status.objects.all()
    context_object_name = 'statasus'


class StatusListView(ListAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

