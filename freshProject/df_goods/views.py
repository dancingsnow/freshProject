# coding:utf-8
from django.shortcuts import render
from django.http import *
from .models import *

# index首页
def index(request):
    adv = Advertising.objects.all()
    fruits = GoodsInfo.objects.filter(isDelete=0,gtype_id=1)   # gtype_id = 2   ,过滤外键的方式
    # print(fruits)
    # print(type(fruits))
    # print(len(fruits))


    context = {
        'title':'首页',
        'loadin':0,
        'adv01_link':adv[0].alink,
        'adv02_link':adv[1].alink,
        'adv01':adv[0].apic,
        'adv02':adv[1].apic,
        'fruits':fruits,
    }
    return render(request,'df_goods/index.html',context)

# 两个广告位的链接
def adv_link(request,num):
    print(num)
    if num == 01:
        return HttpResponse('这是广告一的跳转！')
    elif num == 02:
        return HttpResponse('这是广告二的跳转！')
    else:
        return HttpResponse('广告跳转还未定义，为原始的‘/adv/#/‘')

# list商品列表界面
def list(request):
    context = {'loadin':0}
    return render(request,'df_goods/list.html',context)

# 商品细节界面
def detail(request):
    context = {'loadin':0}
    return render(request,'df_goods/detail.html',context)