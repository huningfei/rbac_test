from django import forms
from api import models


class ApiModelForm(forms.ModelForm):
    class Meta:
        model = models.Api
        fields = "__all__"
        labels = {
            "url": "地址",
        }
        widgets = {  # 设置每个字段的插件信息
            "url": forms.widgets.TextInput(attrs={"class": "form-control"}),
            "app": forms.widgets.Select(attrs={"class": "form-control"}),

        }
        error_messages = {  # 设置每个字段的报错提示信息
            "url": {
                "required": "url不能为空"
            },
        }


class ApplicationModelForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = "__all__"
        error_messages = {  # 设置每个字段的报错提示信息
            "title": {
                "required": "title不能为空"
            },
        }
        widgets = {  # 设置每个字段的插件信息
            "title": forms.widgets.TextInput(attrs={"class": "form-control"}),


        }
