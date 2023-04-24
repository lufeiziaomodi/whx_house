from django.shortcuts import render, redirect, HttpResponse
from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from django.core.exceptions import ValidationError
from app01.utils.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value = True)
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)  # 直接返回给password


class UserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.UserInfo
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd) # 直接返回给password

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入")
        # 返回，此字段保存入数据库
        return confirm


def login_page(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login_page.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 数据库校验，获取用户对象、None为失败
        admin_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login_page.html', {'form': form})
        else:
            request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
            return redirect("/index/")

    else:
        return render(request, 'login_page.html', {'form': form})


def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_add.html', {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login_page/')
    return render(request, 'user_add.html', {"form": form})  # 显示错误信息
