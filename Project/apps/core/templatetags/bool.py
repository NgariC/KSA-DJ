from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def icon(value):
    if value is False:
        return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')
    else:
        return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
