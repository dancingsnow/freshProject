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
    fruits_word = typelist[0].goodsinfo_set.filter(isDelete=0).order_by('-gclick') #标题边的推荐文字内容
    fruits = typelist[0].goodsinfo_set.filter(isDelete=0).order_by('-id')  # 水果默认推荐最新的
    sea_word = typelist[1].goodsinfo_set.filter(isDelete=0).order_by('-gclick') # 海鲜水产
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
def detail(request,num):
    # 检索得到数据，默认是按id升序排列，可以直接根据切片角标得到数据组
    # 得到的数据按照最大的id即为最新的数据，也就是最新品，取最后两个个进行新品推荐的推送
    typelist = TypeInfo.objects.all()

    fruit_list = typelist[0].goodsinfo_set.filter(isDelete=0)
    sea_list = typelist[1].goodsinfo_set.filter(isDelete=0)
    meat_list = typelist[2].goodsinfo_set.filter(isDelete=0)
    egg_list = typelist[3].goodsinfo_set.filter(isDelete=0)
    veg_list = typelist[4].goodsinfo_set.filter(isDelete=0)
    ice_list = typelist[5].goodsinfo_set.filter(isDelete=0)

    num_id = int(num[1:])
    if num[0] == 'a': # 1.新鲜水果fruit
        goods_detail = fruit_list[num_id-1]
        goods_adv = fruit_list.order_by('-id')[0:2]
        # print('goodsADVICE:',goods_adv)
        # print(goods_adv[0].gtitle)
        # print(goods_adv[1].gtitle)
    elif num[0] == 'b': # 2.海鲜水产sea
        goods_detail = sea_list[num_id-1]
        goods_adv = sea_list.order_by('-id')[0:2]     # django不支持倒序取，所以只能倒序排序，然后取前边两个
    elif num[0] == 'c': # 3.猪牛羊肉meat
        goods_detail = meat_list[num_id - 1]
        goods_adv = meat_list.order_by('-id')[0:2]
    elif num[0] == 'd': # 4.禽类蛋品egg
        goods_detail = egg_list[num_id - 1]
        goods_adv = egg_list.order_by('-id')[0:2]
    elif num[0] == 'e': # 5.新鲜蔬菜veg
        goods_detail = veg_list[num_id - 1]
        goods_adv = veg_list.order_by('-id')[0:2]
    elif num[0] == 'f': # 6.速冻食品ice
        goods_detail = ice_list[num_id - 1]
        goods_adv = ice_list.order_by('-id')[0:2]

    context = {
        'loadin':0,
        'goods_detail':goods_detail,
        'goods_adv':goods_adv,
    }
    return render(request,'df_goods/detail.html',context)