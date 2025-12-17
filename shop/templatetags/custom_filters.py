from django import template

register = template.Library()

@register.filter
def div(value, arg):
    """Divide value by arg"""
    try:
        return round(float(value) / float(arg), 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return ''
