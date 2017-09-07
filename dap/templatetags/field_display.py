from django.template import Library
from types import FunctionType

register = Library()


def body(ret_list, list_display, obj):
    for row in ret_list:
        yield [name(obj, row) if isinstance(name, FunctionType) else getattr(row, name) for name in list_display]


def head(list_dispaly):
    print(list_dispaly)
    return [title.__name__.title() if isinstance(title, FunctionType) else title.title() for title in list_dispaly]

@register.inclusion_tag("dap/md.html")
def func(ret_list, list_display, obj):
    if list_display and isinstance(list_display, list):

        return {'body': body(ret_list, list_display, obj), 'head': head(list_display)}
    else:
        return {'body': None, 'head': None}