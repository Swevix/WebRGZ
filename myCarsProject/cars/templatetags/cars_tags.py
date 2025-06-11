from django import template

# Пример фиктивного списка категорий
categories_db = [
    {'id': 1, 'name': 'Седаны'},
    {'id': 2, 'name': 'Кроссоверы'},
    {'id': 3, 'name': 'Хэтчбеки'},
]

register = template.Library()

@register.simple_tag()
def get_categories():
    return categories_db
