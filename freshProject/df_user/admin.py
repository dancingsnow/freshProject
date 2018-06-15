# coding:utf-8
from django.contrib import admin
from .models import *

# Register your models here.
# 设计用户管理界面的内容
class UserInfoAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserInfo,UserInfoAdmin)
