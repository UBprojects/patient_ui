from django import template

register = template.Library()


@register.filter
def replace_space(string, with_value="_"):
    return string.replace(' ', with_value)

@register.filter
def first_dict_key(dict):
    return list(dict.keys())[0]
