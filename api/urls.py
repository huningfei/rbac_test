from django.conf.urls import url, include
from django.contrib import admin
from api import views

urlpatterns = [

    url(r'^login/$', views.login, name='login'),
    # 注销
    url(r'^logout/$', views.login),
    # 个人中心
    url(r'^userinfo/$', views.userinfo, name='userinfo'),

    url(r'^app/list/$', views.app_list, name='app_list'),
    url(r'^app/add/$', views.app_add, name='app_add'),
    url(r'^app/edit/(\d+)/$', views.app_edit, name='app_edit'),
    url(r'^app/del/(\d+)/$', views.app_del, name='app_del'),

    url(r'^api/list/$', views.api_list, name='api_list'),
    url(r'^api/add/$', views.api_add, name='api_add'),
    url(r'^api/edit/(\d+)/$', views.api_edit, name='api_edit'),
    url(r'^api/del/(\d+)/$', views.api_del, name='api_del'),
    url(r'^api/test/(\d+)/$', views.api_test, name='api_test'),

]
