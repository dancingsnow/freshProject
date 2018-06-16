# coding:utf-8
from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$|^index/$',views.index),
    # url(r'adv/(\d+)',views.advtising), # 广告位置
    url(r'^list/$',views.list),
    url(r'^detail/$', views.detail),
]