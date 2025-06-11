from django.test import TestCase

# Create your tests here.
# Создание
Car.objects.create(
    title="Honda Accord 2023",
    slug="honda-accord-2023",
    description="Стильный седан с передовыми технологиями.",
    price=27000.00,
    is_published=Car.Status.PUBLISHED
)

# Изменение
car = Car.objects.get(slug="toyota-camry-2023")
car.price = 26000.00
car.save()

# Удаление
car = Car.objects.get(slug="mazda-cx-5-2023")
car.delete()

# Фильтрация и сортировка
Car.objects.filter(price__gte=25000).order_by('price')