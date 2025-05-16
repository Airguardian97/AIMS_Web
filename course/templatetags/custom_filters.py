# course/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Safely retrieve an item from a dictionary using the key."""
    try:
        key = int(key)
    except (ValueError, TypeError):
        pass
    return dictionary.get(key) if isinstance(dictionary, dict) else None

@register.filter
def get_grade(grade_dict, args):
    """Retrieve grade from a dict using (subject_id, period) tuple as key."""
    try:
        subject_id_str, period = args.split(',', 1)
        subject_id = int(subject_id_str)
        print()
        return grade_dict.get((subject_id, period))
    except Exception:
        return None

@register.filter
def get_by_tuple_key(dict_obj, key_tuple):
    """Retrieve value using a tuple key from a dictionary."""
    if isinstance(dict_obj, dict):
        return dict_obj.get(key_tuple)
    return None

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add CSS class to a form field widget."""
    return field.as_widget(attrs={'class': css_class})

@register.filter
def currency(value):
    """Format a number as Philippine Peso currency."""
    try:
        value = float(value)
        return "₱{:,.2f}".format(value)
    except (ValueError, TypeError):
        return "₱0.00"
