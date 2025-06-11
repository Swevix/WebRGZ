from django.views.generic.base import ContextMixin

MENU = [
    {'title': 'Главная',              'url_name': 'cars:home'},
    {'title': 'О сайте',              'url_name': 'cars:about'},
    {'title': 'Добавить (Form)',      'url_name': 'cars:add_car_custom'},
    {'title': 'Добавить (ModelForm)', 'url_name': 'cars:add_car_model'},
    {'title': 'Загрузка файла',       'url_name': 'cars:upload_file'},
]

class DataMixin(ContextMixin):
    """
    Добавляет в контекст:
      - global menu
      - title, если задано
      - page_range для ListView с пагинацией
    """
    title = None

    def get_context_data(self, *, object_list=None, **kwargs):
        # Сначала получаем весь контекст от родительских классов,
        # в том числе paginator, page_obj, object_list
        context = super().get_context_data(object_list=object_list, **kwargs)

        # Базовый контекст
        context['menu'] = MENU
        if self.title:
            context['title'] = self.title

        # Если есть пагинация — вычисляем ограниченный диапазон страниц
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        if paginator and page_obj:
            total = paginator.num_pages
            current = page_obj.number
            window = 2
            start = max(current - window, 1)
            end   = min(current + window, total)
            context['page_range'] = range(start, end + 1)

        return context
