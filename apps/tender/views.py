from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from apps.tender.forms import TenderForm
from apps.tender.models import Tender, TenderImg
from apps.provider.models import Category
from apps.tender.filters import TenderFilter
from apps.user_cabinet.models import Contacts


class TenderListView(generic.ListView):
    model = Tender
    queryset = Tender.objects.all()
    template_name = 'tender_list.html'
    paginate_by = '10'
    filter_class = TenderFilter
    context_object_name = 'tenders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        contacts = Contacts.load()
        context['contacts'] = contacts
        return context


class TenderDetailView(generic.DetailView):
    template_name = 'tender_detail.html'
    model = Tender
    context_object_name = 'tender'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['products'] = Provider.products.all()
        return context


class TenderCreateView(generic.CreateView):
    template_name = 'cabinet/tender_create.html'
    form_class = TenderForm
    model = Tender
    queryset = Tender.objects.all()
    success_url = '/'

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            tender = form.save(commit=False)
            days = request.POST.get('period')
            tender.user = request.user
            tender.end_date = timezone.now() + timezone.timedelta(days=int(days))
            tender.save()
            for i in request.FILES.getlist('file'):
                TenderImg.objects.create(tender=tender, image=i)
            return redirect('/')
        print(form.errors)
        return super().post(request, *args, **kwargs)


class TenderUpdateView(generic.UpdateView):
    template_name = 'cabinet/tender_update.html'
    form_class = TenderForm
    model = Tender
    queryset = Tender.objects.all()
    success_url = '/profile/tender/list/'

    def get_context_data(self, **kwargs):
        print(self.request.user.user_type)
        context = super().get_context_data(**kwargs)
        context_keys = ['one', 'two', 'three', 'four', 'five', 'six']
        obj = self.get_object()
        images = obj.tender_images.all()
        context_values = (images[i] if i < len(images) else None for i in range(len(context_keys)))
        context.update(dict(zip(context_keys, context_values)))
        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        if request.POST.get('period'):
            days = request.POST.get('period')
            obj.end_date += timezone.timedelta(days=int(days))
            obj.save()

        print(request.FILES)
        file_fields = ['file1', 'file2', 'file3', 'file4', 'file5', 'file6']
        new_images = [request.FILES.get(file) for file in file_fields if request.FILES.get(file)]
        existing_images = obj.tender_images.all()
        for idx, file_field in enumerate(file_fields):
            if request.FILES.get(file_field):
                # Удаление старого изображения, если существует
                if idx < len(existing_images):
                    existing_images[idx].delete()
                # Сохранение нового изображения

        for i in new_images:
            TenderImg.objects.create(tender=obj, image=i)
        return super().post(request, *args, **kwargs)


def delete_tender(request, pk):
    tender = get_object_or_404(Tender, id=pk)
    if request.user == tender.user:
        tender.delete()
        return redirect('/profile/tender/list/')
