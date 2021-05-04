from django import template

register = template.Library()


@register.filter
def round_chances(chances):
    if chances is not None:
        return round(chances*100)
