# coding:utf-8
from django.shortcuts import render
from django.http import *
from .models import *

# index首页
def index(request):
    adv = Advertising.objects.all()
    typelist = TypeInfo.objects.all()
    # fruits = GoodsInfo.objects.filter(isDelete=0,gtype_id=1)
    # gtype_id = 2   ,过滤外键的方式
    # fru = typelist[0].goodsinfo_set.filter(id=1)  # 利用外键追溯到属于它的数据
    # print(fru[0].gtitle)
    fruits_word = typelist[0].goodsinfo_set.filter(isDelete=0).order_by('-gremain_num') #标题边的推荐文字内容
    fruits = typelist[0].goodsinfo_set.filter(isDelete=0).order_by('-id')  # 水果默认推荐最新的
    sea_word = typelist[1].goodsinfo_set.filter(isDelete=0).order_by('-gremain_num') # 海鲜水产
    sea = typelist[1].goodsinfo_set.filter(isDelete=0).order_by('-id')

# 还有猪牛羊肉、禽类蛋品、新鲜蔬菜、速冻食品等模块，同样的方式！

    context = {
        'title':'首页',
        'loadin':0,
        'adv01_link':adv[0].alink,
        'adv02_link':adv[1].alink,
        'adv01':adv[0].apic,
        'adv02':adv[1].apic,
        'fruits_word':fruits_word[0:3],
        'fruits':fruits[0:4],
        'sea_word': sea_word[0:3],
        'sea': sea[0:4],
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
def detail(request,num_id):

    context = {
        'loadin':0,
        'num_id':num_id,
    }
    return render(request,'df_goods/detail.html',context)