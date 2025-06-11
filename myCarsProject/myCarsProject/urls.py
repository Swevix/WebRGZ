# myCarsProject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # При заходе на '/', перенаправляем на '/cars/'
    path('', RedirectView.as_view(pattern_name='cars:home', permanent=False)),

    # Все пути приложения cars теперь начинаются с '/cars/...'
    path('cars/', include(('cars.urls', 'cars'), namespace='cars')),

    # Авторизация/регистрация
    path('users/', include(('users.urls', 'users'), namespace='users')),

    # Админка
    path('admin/', admin.site.urls),
]
