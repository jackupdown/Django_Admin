from django.template import Library
from types import FunctionType
from django.forms.models import ModelChoiceField
from django.urls import reverse
from  dap.service import v1
register = Library()


def body(ret_list, list_display, obj):
    for row in ret_list:
        if list_display == '__all__':
            yield [str(row)]
        else:
            yield [name(obj, obj=row) if isinstance(name, FunctionType) else getattr(row, name) for name in list_display]


def head(list_dispaly, obj):
    print(list_dispaly)
    if list_dispaly == '__all__':
        yield '对象列表'
    else:
        for item in list_dispaly:
            if isinstance(item, FunctionType):
                yield item(obj, is_header=True)
            else:
                yield obj.model_class._meta.get_field(item).verbose_name
    # return [title.__name__.title() if isinstance(title, FunctionType) else title.title() for title in list_dispaly]


@register.inclusion_tag("dap/md.html")
def func(ret_list, list_display, obj):
    return {'body': body(ret_list, list_display, obj), 'head': head(list_display, obj)}


@register.inclusion_tag("dap/add_edit_md.html")
def show_add_edit_form(form):
    from django.forms.boundfield import BoundField
    # print(form)
    w_form = []
    for item in form:
        # print(tag,'----------------------------\r')
        row = {'is_popup': False, 'popup_url': None, 'item': item}
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in v1.site._registry:
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            url_name = "{0}:{1}_{2}_add".format(v1.site.namespace, target_app_label, target_model_name)
            taget_url = "{0}?popid={1}".format(reverse(url_name), item.auto_id)
            row['is_popup'] = True
            row['popup_url'] = taget_url
        w_form.append(row)
    # print(w_form)
    return {'form': w_form}