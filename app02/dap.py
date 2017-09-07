from django.contrib import admin
from dap.service import v1
from app02 import models
# Register your models here.


class DapUserInfo(v1.BaseDap):
    list_display = ['id', 'name', 'email']
v1.site.register(models.UserInfo, DapUserInfo)


class DapRole(v1.BaseDap):
    list_display = ['id', 'name', 'info']
v1.site.register(models.Role, DapRole)
