from urllib.parse import urlencode

from django import template

from goods.models import Categories

register = template.Library()


# Тег шаблону, що повертає всі категорії.
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()


# Тег шаблону, що оновлює GET-параметри поточного запиту і повертає їх рядком.
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)
