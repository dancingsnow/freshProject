# coding:utf-8
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# 如果没有登陆，那么就转到登陆界面
# 用户中心的装饰器，防止强制访问
def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)   # 如果检测到session则直接返回函数
        else:
            result = HttpResponseRedirect('/user/login/')
            result.set_cookie('url',request.get_full_path())  # path只得到地址，full_path得到包括后边的请求信息
            return result
    return login_fun



