from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.db.models import ExpressionWrapper, F, DecimalField

from .models import Car, Manufacturer, Tag, Comment


# Калькулируемое поле: краткая информация (п.7)
@admin.display(description="Краткая информация")
def brief_info(obj):
    return f"Описание: {len(obj.description)} символов" if obj.description else "Нет описания"


# Калькулируемое поле: цена с налогом (п.7)
@admin.display(description="Цена с налогом")
def price_with_tax(obj):
    if obj.price is not None:
        return f"${round(float(obj.price) * 1.2, 2)}"
    return "$0.00"


# Фильтр по статусу публикации
class PublishedFilter(SimpleListFilter):
    title = "Статус публикации"
    parameter_name = "pub_status"

    def lookups(self, request, model_admin):
        return [
            ("published", "Опубликовано"),
            ("draft", "Черновик"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "published":
            return queryset.filter(is_published=Car.Status.PUBLISHED)
        elif self.value() == "draft":
            return queryset.filter(is_published=Car.Status.DRAFT)
        return queryset


# Фильтр по диапазону цены
class PriceRangeFilter(SimpleListFilter):
    title = "Диапазон цены"
    parameter_name = "price_range"

    def lookups(self, request, model_admin):
        return [
            ('low', 'Низкая (<20000)'),
            ('medium', 'Средняя (20000–50000)'),
            ('high', 'Высокая (>50000)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=20000)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=20000, price__lte=50000)
        elif self.value() == 'high':
            return queryset.filter(price__gt=50000)
        return queryset


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'slug', 'description', 'price', 'manufacturer', 'tags', 'image']
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['time_create', 'time_update']
    list_display = (
        'id', 'title', 'author', 'time_create', 'is_published',
        brief_info, price_with_tax,
    )
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    list_per_page = 5
    search_fields = ['title', 'author__username']
    list_filter = [PublishedFilter, 'manufacturer', PriceRangeFilter]
    actions = ['set_published', 'set_draft']

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Car.Status.PUBLISHED)
        self.message_user(request, f"Статус 'Опубликовано' обновлён для {count} записей.", messages.SUCCESS)

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Car.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации.", messages.WARNING)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'country')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'author', 'created')
    list_display_links = ('id',)
    search_fields = ('car__title', 'author__username', 'text')