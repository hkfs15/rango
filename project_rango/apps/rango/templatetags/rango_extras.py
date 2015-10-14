from django import template
from project_rango.apps.rango.models import Category

register = template.Library()


@register.inclusion_tag('cats.html')
def get_cat_list():
    return {'cats': Category.objects.all()}
