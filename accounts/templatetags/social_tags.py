from django import template
from django.utils import timezone


register = template.Library()


@register.simple_tag
def current_year():
    return "2021-" + timezone.now().strftime("%Y")
