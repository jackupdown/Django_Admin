# print('this is from app01')
from dap.service import v1
from app01 import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
# Register your models here.


class DapUserInfo(v1.BaseDap):
    def checkBox(self, obj=None, is_header=False):
        if is_header:
            return mark_safe("<input id='sel_all' type='checkbox'/>")
        tag = "<input type='checkbox' val={0}/>".format(obj.pk)
        return mark_safe(tag)

    def edit(self, obj=None, is_header=False):
        if is_header:
            return '操作'
        param_dict = QueryDict(mutable=True)
        param_dict['_changelistfilter'] = self.request.GET.urlencode()
        name = "{0}:{1}_{2}_change".format(self.site.namespace, obj._meta.app_label, obj._meta.model_name)
        url = reverse(name, args=(obj.pk,))
        # print(param_dict, '\r', param_dict.urlencode())
        tag = "<a href='{0}?{1}' class='btn btn-primary'>编辑</a>".format(url, param_dict.urlencode())
        return mark_safe(tag)

    def delete(self, obj=None, is_header=False):
        if is_header:
            return '操作'
        param_dict = QueryDict(mutable=True)
        param_dict['_changelistfilter'] = self.request.GET.urlencode()
        name = "{0}:{1}_{2}_delete".format(self.site.namespace, obj._meta.app_label, obj._meta.model_name)
        url = reverse(name, args=(obj.pk,))
        tag = '<button url-value="{0}?{1}" value="{2}" type="button" data-toggle="modal" data-target="#mymodal" class="delf btn btn-primary">删除</button>'.format(url, param_dict.urlencode(), obj.pk)
        return mark_safe(tag)

    list_display = [checkBox, 'id', 'name', 'email', edit, delete]

v1.site.register(models.UserInfo, DapUserInfo)


class DapRole(v1.BaseDap):
    list_display = ['id', 'name', 'info']
v1.site.register(models.Role, DapRole)


v1.site.register(models.UserGroup)