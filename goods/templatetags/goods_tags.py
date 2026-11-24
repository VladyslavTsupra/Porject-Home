from urllib.parse import urlencode

from django import template

from goods.models import Categories

register = template.Library()


# Template tag that returns all categories.
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()


# Template tag that updates the current request's GET params and returns them as a string.
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)
