from django import template
register = template.Library()

@register.filter
def fix_datetime(value, *args):
    return value.replace("T", " ")
    
@register.filter
def fix_error(value, *args):
    splitsemicolon = value.replace(":")
    colon = splitsemicolon[1]
    return colon

@register.filter
def fix_duration(value, *args):
    value = int(value)
    hr = str(int(value/60))+"h"
    mi = str(int(value%60))+"m"
    return hr+" "+mi

@register.filter
def fix_time(value, *args):
    datetime =  value.split("T")
    time = datetime[1]
    return time

@register.filter
def fix_split(value, *args):
    data =  value.split(". ")
    time = data[0]
    return time

@register.filter
def sort_prices(value, *args):
    new_list = sorted(value, key=lambda d: d["totalPriceList"][0]["fd"]["ADULT"]["fC"]["TF"])
    return new_list


@register.filter
def fix_date(value, *args):
    datetime =  value.split("T")
    date = datetime[0]
    return date

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def manage_fee(value, arg):
    value = float(value)
    arg = float(arg)
    mark_up = value - arg
    perc = (mark_up*18)/100
    total_markup = mark_up+perc
    print(total_markup)
    return total_markup



