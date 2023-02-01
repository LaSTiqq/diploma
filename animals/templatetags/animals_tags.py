from django import template
from django.db.models import Count
from animals.models import *

register = template.Library()


@register.simple_tag()
def get_families():
    return Family.objects.all()


@register.inclusion_tag('animals/list_families.html')
def show_families():
    families = Family.objects.annotate(cnt=Count('animals')).filter(cnt__gt=0)
    return {"families": families}
