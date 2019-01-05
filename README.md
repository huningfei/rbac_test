主管用户名：xb 密码123  管理员用户

员工用户名：xy 密码123  普通用户

查看页面的时候必须先登录,也有注销功能，点击人头即可
url:   http://127.0.0.1:8001/api/login/

里面分为应用列表和接口列表都可以增删改查。

实现了不用的用户登录显示不同的菜单，权限控制到了颗粒度



#################################################################################
{% if "app_edit"|permission:request or "app_del"|permission:request %}

app_edit当做第一个参数，冒号后面的reqest当做第二个参数传过来，permission是刚才定义在rbac文件里面
的fiflter函数，可以用在if后面，而simple_tag 和inclusion_tag是不能在if后面用的

![image](https://github.com/huningfei/rbac_test/blob/master/images/rbac_img.png)
