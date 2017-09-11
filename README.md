Django Admin组件重写！
1. 自定义列表页面及数据表头
    models.UserInfo._meta.app_label 获取app name
    models.UserInfo._meta.model_name    获取Model name

2. 通过继承ModelForm自定义MyModelForm
    通过type元类动态生成MyModelForm
    自定义form表单，替代 {{ form.as_p }}

3. 动态生成url

4. 增加popup窗口功能
    window.open(url, "xxx", "status=1, height=500, width=600, toolbar=1, resizeable=0")
    可嵌套生成，但注意第2个参数不能重复，否则会覆盖

5. 分页，并保留当前页的get参数
    通过request.GET获得封装了参数的QueryDict对象
    通过urlencode()方法生成url '?'后的参数
