from django.db import models

# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name='姓名')
    email = models.EmailField(verbose_name='邮箱')
    ug = models.ForeignKey('UserGroup', null=True, blank=True, verbose_name='用户组')
    u2r = models.ManyToManyField('Role', null=True, blank=True, verbose_name='角色')

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色')
    info = models.TextField(verbose_name='备注')

    def __str__(self):
        return self.name


class UserGroup(models.Model):
    name = models.CharField(max_length=32, verbose_name='用户组')
    info = models.TextField(verbose_name='备注')

    def __str__(self):
        return self.name
