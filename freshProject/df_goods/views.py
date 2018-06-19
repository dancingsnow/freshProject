# coding:utf-8
from django.shortcuts import render
from django.http import *
from .models import *
from django.core.paginator import Paginator
# 未设置地址的链接
def noSetting(request):
    return HttpResponse('这个链接还未定义！')

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
def list(request,type_num,sort_num=1,pIndex=1):
    # 1.先得到list_id对应的分类
    type = TypeInfo.objects.get(id=type_num)
    # 2.1根据列表类别，得到新品推荐栏的两条数据
    goods_adv = type.goodsinfo_set.filter(isDelete=0).order_by('-id')
    # 2.2根据列表的类别，按着sort的排序方式进行排序,筛选出按排序的所有数据
    if sort_num == '1': # 默认按id倒序排列
        list_info = type.goodsinfo_set.filter(isDelete=0).order_by('-id')
    elif sort_num == '2':  # 按价格正序排列
        list_info = type.goodsinfo_set.filter(isDelete=0).order_by('gprice')
    elif sort_num == '3':  # 按点击量倒序排列
        list_info = type.goodsinfo_set.filter(isDelete=0).order_by('-gclick')
    # 3.1根据得到的数据列表，进行分页处理
    p = Paginator(list_info,5)  # 进行分页，每页五条数据
    # 3.2根据传来的pindex的值，确定访问第几页的数据
    page = p.page(int(pIndex))   # paginator负责处理进行分页，page负责每页的数据进行处理，以及上下页数据存在与否的判断！

    context = {
        'loadin':0,
        'title':type.ttitle,
        'type':type,
        'sort_num':sort_num,
        'goods_adv': goods_adv[0:2],
        'p':p,  # paginator对象
        'page':page,  # 当前页page对象
    }
    return render(request,'df_goods/list.html',context)

# 商品细节界面
def detail(request,type_num,goods_index):
    type = TypeInfo.objects.get(id=type_num)  # 类别
    goods_adv = type.goodsinfo_set.filter(isDelete=0).order_by('-id')   # 广告
    goods_detail = type.goodsinfo_set.get(id=goods_index)    # 商品细节详情

    context = {
        'loadin':0,
        'link':'detail',  # 为了设置链接的三段归属链接的设置（detail需要‘商品详情’这四个字）
        'title':goods_detail.gtitle,    # 标题显示内容
        'type':type,    # 所属类别
        'goods_adv':goods_adv[0:2],  # 广告部分
        'goods_detail':goods_detail,  # 具体商品的细节

    }
    return render(request,'df_goods/detail.html',context)





