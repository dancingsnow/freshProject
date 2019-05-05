# coding:utf-8
from django.conf.urls import url
from df_order import views

urlpatterns = [
    url(r'^place_order/',views.place_order),
    url(r'^order_handle',views.order_handle), # 提交订单
]