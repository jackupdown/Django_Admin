from django.shortcuts import HttpResponse, render, redirect
from django.conf.urls import url, include
from django.urls import reverse
from django.forms import ModelForm
from django.forms import fields
from django.forms import widgets
from dap.static.dap.pagnition import PageInfo
import json
import copy


class BaseDap():
    list_display = '__all__'
    myMF = None

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        # self.list_display = []
        self.info = model_class._meta.app_label, model_class._meta.model_name

    def getMyMF(self):
        if self.myMF:
            return self.myMF
        else:
            """
            class MyMF(ModelForm):
                class Meta:
                    model = self.model_class
                    fields = '__all__'
            """
            _m = type('Meta', (object,), {'model': self.model_class, 'fields': '__all__'})
            MyMF = type('MyMF', (ModelForm,), {'Meta': _m})
            return MyMF

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
        self.request = request
        # print(request.get_full_path())
        param_str = request.get_full_path().split('/')[-1]
        # print(param_str)
        # 生成页面添加数据按钮
        from django.http.request import QueryDict
        param_dict = QueryDict(mutable=True)
        if request.GET:
            param_dict['_changelistfilter'] = request.GET.urlencode()
        base_add_url = reverse("{2}:{0}_{1}_add".format(self.info[0],  self.info[1], self.site.namespace))
        add_url = "{0}?{1}".format(base_add_url, param_dict.urlencode())

        # 分页开始
        conditions = {}
        all_count = self.model_class.objects.filter(**conditions).count()
        base_page_url = reverse("{2}:{0}_{1}_changelist".format(self.info[0],  self.info[1], self.site.namespace))
        page_param_dict = copy.deepcopy(request.GET)
        page_param_dict._mutable = True
        page_obj = PageInfo(current_page=request.GET.get('page'), all_count=all_count, base_url=base_page_url, page_param_dict=page_param_dict)
        ret = self.model_class.objects.filter(**conditions)[page_obj.start_data:page_obj.end_data]
        # print(ret, self.list_display)
        context = {
            'ret_list': ret,
            'list_display': self.list_display,
            'base_dap_obj': self,
            'add_url': add_url,
            'param_str': param_str,
            'page_str': page_obj.pager(),
        }
        # print(context)
        return render(request, 'dap/change_list.html', context)

    def add_view(self, request):
        """增加数据"""
        if request.method == 'GET':
            mf_obj = self.getMyMF()()
            # test widgets
            for item in mf_obj:
                # print(item.field.label)
                v = self.model_class._meta.get_field(item.name)
                v.error_messages = {
                    'required': '该字段不能为空'
                }
        else:
            mf_obj = self.getMyMF()(data=request.POST, files=request.FILES)

            if mf_obj.is_valid():
                obj = mf_obj.save()
                popid = request.GET.get('popid')
                if popid:
                    data = {'popid': popid, 'id': obj.pk, 'text': str(obj)}
                    # print(data, 'v1..add')
                    return render(request, 'dap/popup_response.html', {'data': data})
                # 添加成功，跳转回页面
                base_url = reverse("{2}:{0}_{1}_changelist".format(self.info[0],  self.info[1], self.site.namespace))
                list_url = "{0}?{1}".format(base_url, request.GET.get('_changelistfilter'))
                # print(list_url)
                return redirect(list_url)
        context = {
            'form': mf_obj
        }
        return render(request, 'dap/add.html', context)

    def delete_view(self, request, pk):
        """删除"""
        if request.method == 'GET':
            # print(pk)
            ret_dict = {'code': 1, 'msg': None}
            obj = self.model_class.objects.filter(pk=pk)
            if not obj:
                ret_dict['code'] = 0
                ret_dict['msg'] = 'ID does not exist!'
                return HttpResponse(json.dumps(ret_dict))
            obj.delete()
            return HttpResponse(json.dumps(ret_dict))
        return HttpResponse('-----delete_view')

    def change_view(self, request, pk):
        """修改"""
        edit_obj = self.model_class.objects.filter(pk=pk).first()
        if not edit_obj: return HttpResponse('ID does not exist!')
        if request.method == 'GET':
            mf_obj = self.getMyMF()(instance=edit_obj)
        else:
            mf_obj = self.getMyMF()(data=request.POST, files=request.FILES, instance=edit_obj)
            if mf_obj.is_valid():
                mf_obj.save()
                # 添加成功，跳转回页面
                base_url = reverse("{2}:{0}_{1}_changelist".format(self.info[0], self.info[1], self.site.namespace))
                list_url = "{0}?{1}".format(base_url, request.GET.get('_changelistfilter'))
                return redirect(list_url)
        context = {
            'form': mf_obj
        }
        return render(request, 'dap/edit.html/', context)


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
            # print(app_label, model_name)
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
