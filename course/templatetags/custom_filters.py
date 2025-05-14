# course/templatetags/custom_filters.py
from django import template
import locale

register = template.Library()
# Set locale to handle currency format properly (it may vary depending on your environment)
locale.setlocale(locale.LC_ALL, 'en_PH.UTF-8')  # 'en_PH.UTF-8' is for Philippine Peso


@register.filter
def get_item(dictionary, key):
    try:
        # Try integer conversion if possible
        key = int(key)
    except (ValueError, TypeError):
        pass

    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def get_grade(grade_dict, args):
    try:
        # Split the key into subject_id and period from the string
        subject_id_str, period = args.split(',', 1)
        subject_id = int(subject_id_str)
        return grade_dict.get((subject_id, period))  # Using tuple as key
    except Exception:
        return None
    
    


@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key, "-")
    return "-"

@register.filter
def get_tuple_value(dict_obj, key_tuple):
    try:
        return dict_obj.get(key_tuple)
    except Exception:
        return None
    
    
@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter
def currency(value):
    try:
        # Convert the value to a float
        value = float(value)
        # Format it as currency with thousands separator
        return locale.currency(value, grouping=True)
    except (ValueError, TypeError):
        return "₱0.00"
    
    
# @register.filter
# def get_item(dictionary, key):
#     return dictionary.get(key)