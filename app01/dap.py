print('this is from app01')
from dap.service import v1
from app01 import models
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.


class DapUserInfo(v1.BaseDap):
    def checkBox(self, obj):
        tag = "<input type='checkbox' val={0}/>".format(obj.pk)
        return mark_safe(tag)

    def edit(self, obj):
        name = "{0}:{1}_{2}_change".format(self.site.namespace, obj._meta.app_label, obj._meta.model_name)
        url = reverse(name, args=(obj.pk,))
        tag = "<a href='{0}'>编辑</>".format(url)
        return mark_safe(tag)
    list_display = [checkBox, 'id', 'name', 'email', edit]

v1.site.register(models.UserInfo, DapUserInfo)


class DapRole(v1.BaseDap):
    list_display = ['id', 'name', 'info']
v1.site.register(models.Role, DapRole)
