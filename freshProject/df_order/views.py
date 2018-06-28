# coding:utf-8
from django.shortcuts import render
from django.http import *
from .models import *
from df_user.models import *
from df_cart.models import *
import df_user
from django.db import transaction
from datetime import datetime

# order界面
@df_user.user_decorator.login
def place_order(request):
# cart_list = []  # 因为参数是分两次传递过来的，所以为两次访问而list表数据会自动清除情况。用全局变量可以做，但是用户多了，就不能实现。
    # global cart_list
    # if request.is_ajax():
    #     print('IS AJAX!')
    #     id_list = request.GET.getlist('id_num_list[]')  #与ajax传递过来的数据格式有关，key后边要加[]。详见ajax的traditional参数。
    #
    #     for i in id_list:
    #         id_num = i.encode('utf-8')   # 传过来的数据为Unicode格式。
    #         # print CartInfo.objects.get(id=id_num)
    #         cart_list.append(CartInfo.objects.get(id=id_num))
    #     # print(cart_list)
    #     return JsonResponse({'get_id':'1'})
    id_num_list1 = request.GET['id_num_list']   #得到的是一个逗号分割的Unicode编码的字符串  u'27,28,30'
    id_num_list2 = id_num_list1.encode('utf-8').split(',')   # 传过来的数据为Unicode格式
    cart_list = []
    for i in id_num_list2:
        cart_list.append(CartInfo.objects.get(id=int(i)))
    # print(cart_list)

    user = UserInfo.objects.get(id=request.session['user_id'])  # user_name
    context = {
        'title':'提交订单',
        'loadin':1,
        'user':user,
        'cart_list':cart_list,
    }
    resp = render(request,'df_order/place_order.html',context)
    resp.set_cookie('url',request.get_full_path())  # 为了修改地址后可以跳回来
    return resp

# <QueryDict: {u'id_list[]': [u'27', u'28', u'29', u'30']}>
'''
事务：一旦操作失败，则全部回退（利用transaction）
1、创建订单对象
2、判断商品的库存
3、修改商品的库存
4、创建详单对象
5、删除购物车
'''
# 订单完成后的提交
# 编号:谁的订单、订单日期、订单总金额（可以计算，也可以直接保存）、支付状态、订单的收货地址（付款的时候可能会更改）
@transaction.atomic()   # django中利用数据库的事务的方式
@df_user.user_decorator.login
def order_handle(request):
    # 设置一个回退点
    tran_id = transaction.savepoint()

    user_id = request.session.get('user_id')
    addr = request.POST['addr']
    final_cost = request.POST['final_cost']
    id_str = request.POST['id_str']
    # print(addr)
    # print(final_cost)
    # print(request.path)
    # print(request.get_full_path())
    # print(id_str)
    # print(type(id_str))
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.now() # 当前时间
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),user_id) #订单id设置为时间+用户id
        order.ouser = UserInfo.objects.get(id=user_id)
        order.otime = now #原则上，已经定义auto_now=true，便不能手动复制。
        order.ototal = final_cost
        order.oaddr = addr
        order.save()
        print('Create order_info ... OK!')
        # 创建订单的详情
        id_list = id_str.split(',')[0:-1]
        for i in id_list:  # 编码还没改！！！！！！！！！！！！！！！！！！！！！！
            cart = CartInfo.objects.get(id=i)  # 得到购物车信息
            # 查看库存
            goods = cart.buy_goods # 得到这条购物车信息中的商品信息
            if goods. gremain_num >= cart.buy_num:  # 大于等于保存，跳转到订单页
                goods.gremain_num -= cart.buy_num  # 更改库存
                goods.save()
                print(goods.id,'remain_num:',goods.gremain_num,',has changed...')
                # 库存没问题，创建订单详情
                detail = OrderDetailInfo()
                detail.order = order
                detail.goods = goods
                detail.price = goods.gprice
                detail.count = cart.buy_num
                detail.save()
                print('Add order_detail ... OK!')
                # 删除购物车里边的信息。
                cart.delete()
                print('Delete cartInfo ... OK!')
            else:
                transaction.savepoint_rollback(tran_id)  #库存不够，回滚到之前的状态。
                return HttpResponseRedirect('/cart/')
        transaction.savepoint_commit(tran_id) #保存状态id信息
    except Exception as e:
        print('======Wrong Info=====:%s'%e)
        transaction.savepoint_rollback(tran_id)  # 出现异常，回滚到之前的状态。

    # 最终回到订单中心（正常，出错回中心；库存不足回购物车）
    return HttpResponseRedirect('/user/user_center_order/')







