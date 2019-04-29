# coding:utf-8
from django.conf.urls import url
from freshProject.df_cart import views

urlpatterns = [
    url(r'^$',views.cart),
    # url(r'^cart_num/', views.cart_num),  # 界面购物车数字的初始化(对应ajax的方式)
    url(r'^del_goods/(\d+)/$', views.del_goods),  # 删除购物车的商品
    url(r'^add_goods/',views.add_goods),  # 添加商品，有？加数量；没有？加新的数据。
    url(r'^change_num/', views.change_num),  # 修改商品数据。

]