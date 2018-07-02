# coding:utf-8
from django.shortcuts import render
from df_user.models import *
import df_user
from df_goods.models import *
from .models import *
from django.http import *

# 用于ajax请求的装饰器
def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)   # 如果检测到session则直接返回函数
        else:
            # 这里不需要获取元链接，在列表和详情界面默认是添加了url的
            return JsonResponse({'user_exist':'0'})
    return login_fun

# 列表页、详情页，添加到购物车
@login
def add_goods(request):
    goods_id = request.GET['goods_id']
    buy_num = request.GET['goods_num']
    user_id = request.session['user_id']
    # 外键对应的是一个具体的对象，要得到具体的对象信息，在直接按普通数据的方式添加进去就可以。
    buy_user = UserInfo.objects.get(id=user_id) # 用户的信息
    buy_goods = GoodsInfo.objects.get(id=goods_id) # 商品的信息
    # print(buy_user,buy_goods,buy_num)
    cart_exist = CartInfo.objects.filter(buy_user_id=user_id).filter(buy_goods_id=goods_id).exists()    # 根据用户的id得到的购物车的数据
    # print(cart_exist) # 判断，这个用户，对应的这个商品有没有
    if cart_exist:
        print('goods has exist!')
        cart =  CartInfo.objects.filter(buy_user_id=user_id).get(buy_goods_id=goods_id)  #filter得到的是集合，get得到的是一个对象。
        cart.buy_num += int(buy_num)  # 注意传送过来的数据都为字符串，记得转换格式
        cart.save()
    else:
        print('new goods!')
        # 谁？买了什么？买了多少？   # 创建新的购物对象
        cart = CartInfo(buy_user=buy_user,buy_goods=buy_goods,buy_num=buy_num)
        cart.save()
    cart_count = CartInfo.objects.filter(buy_user_id=user_id).count()
    print('cart_count',cart_count)
    return JsonResponse({'cart_count':cart_count})

# 点开界面购物车图标的值(用于ajax刷新数据的初始化)
# def cart_num(request):
#     user_id = request.session.get('user_id','')
#     if user_id == '':
#         return JsonResponse({'cart_count':0})
#     else:
#         cart_count = CartInfo.objects.filter(buy_user_id=user_id).count()
#         print('cart_count', cart_count)
#         return JsonResponse({'cart_count': cart_count})


# 购物车界面
@df_user.user_decorator.login
def cart(request):
    userid = request.session.get('user_id','')  # user_name
    uname = request.session['user_name']
    # user_name = request.session.get('user_name')  可以在此直接得到用户名就行，但是模板
    # 定义为user.uname没办法传递，所以再根据id查了一下名字（缺点是增加了数据库的工作量）
    user = UserInfo.objects.get(id=userid) # 得到用户相关信息
    cart_info = CartInfo.objects.filter(buy_user_id=userid) # 根据用户的id得到的购物车的数据

    context = {
        'loadin':1,
        'title':'购物车',
        'uname':uname, # 用于头部信息的展示
        'cart_info':cart_info, # 从数据库查询到的添加到购物车的数据
    }
    return render(request,'df_cart/cart.html',context)

# 点击删除后的处理
@df_user.user_decorator.login
def del_goods(request,goods_id):
    buy_goods = CartInfo.objects.get(id=goods_id)
    buy_goods.delete()
    print('goods has been delete!')
    return HttpResponseRedirect('/cart/')

# 购买数据有变化,通过ajax的交互，修改现存的购买数量
def change_num(request):
    cart_id = request.GET['cart_id']
    goods_num = request.GET['goods_num']
    cart_info = CartInfo.objects.get(id=cart_id)
    cart_info.buy_num = goods_num
    cart_info.save()
    # print(cart_info.buy_num)
    # print('data has changed！')
    return JsonResponse({'changed':'1'})

