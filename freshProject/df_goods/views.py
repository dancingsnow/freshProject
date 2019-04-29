# coding:utf-8
from django.shortcuts import *
from django.http import *
from .models import *
from django.core.paginator import Paginator
from freshProject.df_cart.models import *
from haystack.views import SearchView

# 未设置地址的链接
def noSetting(request):
    return HttpResponse('这个链接还未定义！')

# 装饰器  ： 商品界面，进行登陆验证的界面显示的装饰器。
def login_ensure(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            user_id = request.session.get('user_id')
            loadin = 1
            uname = request.session.get('user_name')
            cart_count = CartInfo.objects.filter(buy_user_id=user_id).count()

        else:
            loadin = 0
            uname = ''
            cart_count = 0
        return func(request, loadin, uname,cart_count,*args, **kwargs)
    return login_fun

# index首页
@login_ensure
def index(request,loadin,uname,cart_count):
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
        'loadin':loadin,
        'uname':uname,
        'cart_count':cart_count,
        'adv01_link':adv[0].alink,
        'adv02_link':adv[1].alink,
        'adv01':adv[0].apic,
        'adv02':adv[1].apic,
        'fruits_word':fruits_word[0:3],
        'fruits':fruits[0:4],
        'sea_word': sea_word[0:3],
        'sea': sea[0:4],
    }
    # 返回数据时先把自己的url保存下来，有别的链接，则咎会被更改。然后随时可供登录页使用
    # t1 = loader.get_template('df_goods/index.html')
    # con = RequestContext(request,context)
    # resp = HttpResponse(t1.render(con))
    resp = render(request,'df_goods/index.html',context)
    resp.set_cookie('url',request.get_full_path())
    return resp

# 两个广告位的链接
def adv_link(request,num):
    print(num)
    if num == '01':
        return HttpResponse('这是广告一的跳转！')
    elif num == '02':
        return HttpResponse('这是广告二的跳转！')
    else:
        return HttpResponse('广告跳转还未定义，为原始的‘/adv/#/‘')

# list商品列表界面
@login_ensure
def list(request,loadin,uname,cart_count,type_num,sort_num=1,pIndex=1,):
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
        'loadin':loadin,
        'uname':uname,
        'cart_count':cart_count,
        'title':type.ttitle,
        'type':type,
        'sort_num':sort_num,
        'goods_adv': goods_adv[0:2],
        'p':p,  # paginator对象
        'page':page,  # 当前页page对象
    }
    resp = render(request,'df_goods/list.html',context)
    resp.set_cookie('url',request.get_full_path())
    return resp

# 商品细节界面
@login_ensure
def detail(request,loadin,uname,cart_count,type_num,goods_index):
    type = TypeInfo.objects.get(id=type_num)  # 类别
    goods_adv = type.goodsinfo_set.filter(isDelete=0).order_by('-id')   # 广告
    goods_detail = type.goodsinfo_set.get(id=goods_index)    # 商品细节详情
    goods_detail.gclick += 1  # 每进一次详情页，对应的商品的点击量增加1
    goods_detail.save()  # 修改数据后记得保存
    context = {
        'loadin':loadin,
        'uname':uname,
        'cart_count':cart_count,
        'link':'detail',  # 为了设置链接的三段归属链接的设置（detail需要‘商品详情’这四个字）
        'title':goods_detail.gtitle,    # 标题显示内容
        'type':type,    # 所属类别
        'goods_adv':goods_adv[0:2],  # 广告部分
        'goods_detail':goods_detail,  # 具体商品的细节
    }
    resp = render(request,'df_goods/detail.html',context)
    resp.set_cookie('url',request.get_full_path())

    # 用cookie记录下点击的内容，按照最新访问的在前，后访问在后，在用户中心展示最近浏览
    # 因为要存储为可遍历的形式，才能输出数据，id为数字,不知道他有几位，没办法分割数据，
    # 所以这里只能用可修改，有容易区分遍历的列表！！！
    goods_ids = request.COOKIES.get('goods_ids','')  # 获取当地存储的商品id列表
    goods_id = str(goods_detail.id)     # 得到现在的商品的id，转换为字符串
    if goods_ids == '':
        goods_ids = goods_id
        resp.set_cookie('goods_ids',goods_ids)
    else:
        goods_ids2 = goods_ids.split(',')  # 把字符串按 逗号 分割成列表
        if goods_ids2.count(goods_id) == 0:  # 如果列表里边没有
            goods_ids2.insert(0,goods_id)  # 在列表的第0位插入新的id
        if len(goods_ids2) > 5:
            del goods_ids2[5:]  # 大于5，则删除5以后的，其实最大也就能删除6
        goods_ids = ','.join(goods_ids2)  # 再将列表拼成 逗号 分割的字符串
    # 修改完goods_ids的值，再重新写会cookie
    resp.set_cookie('goods_ids',goods_ids)
    return resp

@login_ensure
def context_handle(request,loadin, uname,cart_count,):
    return loadin, uname,cart_count



# 根据haystack自己定义的检索的视图
class MySearchView(SearchView):
    def extra_context(self):  # 额外的上下文数据
        context = super(MySearchView,self).extra_context()
        context['title'] = '搜索'
        context['loadin'] = context_handle(self.request)[0]
        context['uname'] = context_handle(self.request)[1]
        context['cart_count'] = context_handle(self.request)[2]
        return context
    def create_response(self): # 重写了response，详见源代码
        context = self.get_context()
        resp = render(self.request,self.template,context)
        resp.set_cookie('url',self.request.get_full_path()) # 搜索到登陆，跳回原结果
        return resp