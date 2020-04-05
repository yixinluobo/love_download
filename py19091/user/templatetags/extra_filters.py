from django.template.defaultfilters import register


@register.filter(is_safe=True)
def sex(value):
    if value == 'm':
        return '男'
    elif value == 'f':
        return '女'
    return '保密'
