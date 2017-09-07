from django.shortcuts import HttpResponse, render
from django.conf.urls import url, include


class BaseDap():
    list_display = '__all__'

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        # self.list_display = []
        self.info = model_class._meta.app_label, model_class._meta.model_name


    @property
    def urls(self):
        # info = self.model_class._meta.app_label, self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % self.info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % self.info),
            # url(r'^(.+)/history/$', self.history_view, name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % self.info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % self.info),
            # For backwards compatibility (was the change url before 1.9)
            # url(r'^(.+)/$', wrap(RedirectView.as_view(
                # pattern_name='%s:%s_%s_change' % ((self.admin_site.name,) + info)
            # ))),
        ]
        return urlpatterns

    def changelist_view(self, request):
        """查看数据列表"""
        ret = self.model_class.objects.all()
        print(ret, self.list_display)
        context = {
            'ret_list': ret,
            'list_display': self.list_display,
            'base_dap_obj': self
        }
        return render(request, 'dap/change_list.html', context)

    def add_view(self, request):
        """增加数据"""
        # self.model_class.objects.all()
        return HttpResponse((self.info, '-----add_view'))

    def delete_view(self, request, pk):
        """删除"""
        return HttpResponse((self.info, pk, '-----delete_view'))

    def change_view(self, request, pk):
        """修改"""
        return HttpResponse((self.info, pk, '-----change_view'))


class DapSite():
    def __init__(self):
        self._registry = {}
        self.namespace = "dap"
        self.app_name = "dap"

    def register(self, model_class, default_class=BaseDap):
        self._registry[model_class] = default_class(model_class, self)

    def get_urls(self):

        ret = [
            url(r'^login/', self.login, name='login'),
            url(r'^logout/', self.logout, name='logout'),
        ]
        for model_cls, model_obj in self._registry.items():
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name
            print(app_label, model_name)
            ret.append(url(r'^%s/%s/' % (app_label, model_name), include(model_obj.urls)))
        return ret

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

    def login(self, request):
        return HttpResponse('login')

    def logout(self, request):
        return HttpResponse('logout')


site = DapSite()
