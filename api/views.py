from django.shortcuts import render, HttpResponse, redirect
from api import models
from rbac import models as rbac_model
# 导入权限初始化
from rbac.service.permission import init_permission
from api.modelform import ApiModelForm, ApplicationModelForm
import requests
from functools import wraps


# session 登录装饰器
def login_check(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        next_url = request.path_info

        if request.session.get('user'):
            return func(request, *args, **kwargs)
        else:
            return redirect("/login/?next_url={}".format(next_url))

    return inner


# 注销页面
@login_check
def logout(request):
    # 删除所有当前请求相关的session
    request.session.delete()
    return redirect("/login/")


def userinfo(request):
    '''
    个人中心
    :param request:
    :return:
    '''
    return render(request, "api/user_info.html")


def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'api/login.html')

    user = request.POST.get('username')
    pwd = request.POST.get('password')

    user = rbac_model.UserInfo.objects.filter(username=user, password=pwd).first()
    if not user:
        return render(request, 'api/login.html', {'msg': '用户名或密码错误'})
    else:
        init_permission(user, request)

        return redirect('/api/app/list/')


def app_list(request):
    """
    应用列表
    :param request:
    :return:
    """
    app_queryset = models.Application.objects.all()

    return render(request, 'api/app_list.html', {'app_queryset': app_queryset})


def app_add(request):
    """
    添加应用
    :param request:
    :return:
    """

    appname = request.POST.get("title")
    if request.method == "GET":
        form = ApplicationModelForm()

    else:
        form = ApplicationModelForm(request.POST)
        if form.is_valid():
            old_name = models.Application.objects.filter(title=appname)
            if old_name:
                data = "应用名已经存在"
                return render(request, "api/app_add.html", locals())
            else:
                form.save()
                return redirect("/api/app/list")
    return render(request, 'api/app_add.html', {'form': form})


def app_edit(request, nid):
    """
    编辑应用
    :param request:
    :return:
    """
    appname = request.POST.get("title")
    obj = models.Application.objects.filter(id=nid).first()
    if request.method == "GET":
        form = ApplicationModelForm(instance=obj)
        return render(request, 'api/app_edit.html', {"form": form})
    else:
        form = ApplicationModelForm(instance=obj, data=request.POST)
        if form.is_valid():
            old_name = models.Application.objects.filter(title=appname)
            if old_name:
                data = "应用名字已存在"
                return render(request, "api/app_edit.html", locals())

            form.save()
            return redirect("/api/app/list")


def app_del(request, nid):
    """
    删除应用
    :param request:
    :return:
    """
    models.Application.objects.filter(id=nid).delete()
    return redirect("/api/app/list")


def api_list(request):
    """
    接口列表
    :param request:
    :return:
    """
    api_queryset = models.Api.objects.all()

    return render(request, 'api/api_list.html', {'app_queryset': api_queryset})


def api_add(request):
    """
    添加接口
    :param request:
    :return:
    """
    Api = request.POST.get("url")
    if request.method == "GET":
        form = ApiModelForm()
        app_name = models.Application.objects.all()
        return render(request, "api/api_add.html", locals())
    else:
        form_post = ApiModelForm(request.POST)
        if form_post.is_valid():
            old_name = models.Api.objects.filter(url=Api)
            if old_name:
                data = "应用名已经存在"
                return render(request, "api/api_add.html", locals())
            else:
                form_post.save()
                return redirect("/api/api/list")
    return render(request, 'api/api_add.html', {'form': form_post})


def api_edit(request, nid):
    """
    编辑接口
    :param request:
    :return:
    """
    api_name = request.POST.get("url")
    obj = models.Api.objects.filter(id=nid).first()
    if request.method == "GET":
        form = ApiModelForm(instance=obj)
        app_name_id = models.Api.objects.get(id=nid)
        app_name = models.Application.objects.all()
        return render(request, 'api/api_edit.html', locals())
    else:
        form = ApiModelForm(instance=obj, data=request.POST)
        if form.is_valid():
            old_name = models.Api.objects.filter(url=api_name)
            if old_name:
                data = "接口名字已存在"
                return render(request, "api/api_edit.html", locals())

            form.save()
            return redirect("/api/api/list")


def api_del(request, nid):
    """
    删除接口
    :param request:
    :return:
    """
    models.Api.objects.filter(id=nid).delete()
    return redirect("/api/api/list")


def api_test(request, nid):
    """
    接口测试
    :param request:
    :param nid:
    :return:
    """
    api_query = models.Api.objects.filter(id=nid).values()
    api_url = api_query[0].get('url')
    try:

        response = requests.get(url=api_url)
    except Exception:
        return HttpResponse('此网站通')
    result = response.status_code
    return render(request, 'api/api_test.html', {'result': result})
