from django import template
register = template.Library()

@register.filter
def fix_date(value, *args):
    datetime =  value.split("T")
    date = datetime[0]
    return date