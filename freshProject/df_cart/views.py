# coding:utf-8
from django.shortcuts import render

# 购物车界面
def cart(request,buy_userid):
    return render(request,'df_cart/cart.html')
