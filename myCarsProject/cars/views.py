# File: cars/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
    FormView, CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Car, Comment
from .forms import CarForm, CarModelForm, UploadForm, CommentForm
from .utils import DataMixin


class HomeView(DataMixin, ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    paginate_by = 5
    queryset = Car.published.all()
    title = 'Главная'


class AboutView(DataMixin, TemplateView):
    template_name = 'cars/about.html'
    title = 'О сайте'


class CarDetailView(DataMixin, DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = ctx['car'].title
        ctx['comments'] = ctx['car'].comments.select_related('author')
        ctx['comment_form'] = CommentForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.car = self.object
            comment.author = request.user
            comment.save()
            return redirect(self.object.get_absolute_url())
        ctx = self.get_context_data(comment_form=form)
        return self.render_to_response(ctx)


class AddCarCustomView(LoginRequiredMixin, DataMixin, FormView):
    login_url = reverse_lazy('users:login')
    form_class = CarForm
    template_name = 'cars/add_car_custom.html'
    success_url = reverse_lazy('cars:home')
    title = 'Добавить (Form)'

    def form_valid(self, form):
        cd = form.cleaned_data
        car = Car.objects.create(
            author=self.request.user,
            title=cd['title'],
            slug=cd['title'].lower().replace(' ', '-'),
            description=cd['description'],
            price=cd['price'],
            is_published=Car.Status.DRAFT
        )
        image = cd.get('image')
        if image:
            car.image = image
            car.save()
        return super().form_valid(form)


class CarCreateView(LoginRequiredMixin, DataMixin, CreateView):
    login_url = reverse_lazy('users:login')
    model = Car
    form_class = CarModelForm
    template_name = 'cars/add_car_model.html'
    success_url = reverse_lazy('cars:home')
    title = 'Добавить (ModelForm)'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CarUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    model = Car
    form_class = CarModelForm
    template_name = 'cars/add_car_model.html'
    success_url = reverse_lazy('cars:home')
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'
    title = 'Редактировать автомобиль'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class CarDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    login_url = reverse_lazy('users:login')
    model = Car
    template_name = 'cars/car_confirm_delete.html'
    success_url = reverse_lazy('cars:home')
    slug_field = 'slug'
    slug_url_kwarg = 'car_slug'
    title = 'Удалить автомобиль'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class ToggleLikeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def post(self, request, car_slug):
        car = get_object_or_404(Car, slug=car_slug)
        if request.user in car.likes.all():
            car.likes.remove(request.user)
        else:
            car.likes.add(request.user)
        return redirect(car.get_absolute_url())


class UploadFileView(DataMixin, FormView):
    form_class = UploadForm
    template_name = 'cars/upload.html'
    success_url = reverse_lazy('cars:upload_file')
    title = 'Загрузка файла'

    def form_valid(self, form):
        form.save_file()
        return super().form_valid(form)