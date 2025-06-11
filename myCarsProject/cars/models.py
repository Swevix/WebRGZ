import os
import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def car_image_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('cars', new_filename)

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Производитель")
    country = models.CharField(max_length=100, verbose_name="Страна")

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")

    def __str__(self):
        return self.name

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Car.Status.PUBLISHED)

class Car(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=255, verbose_name="Название автомобиля")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(
        upload_to=car_image_path,
        null=True, blank=True,
        verbose_name='Изображение'
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name='liked_cars',
        verbose_name='Лайки'
    )
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.IntegerField(
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус публикации"
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE,
        related_name='cars', verbose_name="Производитель",
        null=True, blank=True
    )
    tags = models.ManyToManyField(
        Tag, related_name='cars',
        verbose_name="Теги", blank=True
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-time_create']
        permissions = [
            ('can_publish_car', 'Может публиковать автомобиль'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cars:car_detail', kwargs={'car_slug': self.slug})

class Comment(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автомобиль'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Комментарий {self.id} к {self.car.title}"
