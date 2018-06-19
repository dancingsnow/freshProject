# coding:utf-8
from django.conf.urls import url
import views
urlpatterns = [
    url(r'^no_setting/$',views.noSetting),
    url(r'^$|^index/$',views.index),
    url(r'^list/(\d+)_(\d+)_(\d+)/$',views.list), # 商品列表!!!!!!!!!!!!!!!!!!
    url(r'^detail/(\d+)_(\d+)/$', views.detail), # 商品细节
    url(r'^adv/(\d+)/$',views.adv_link),  # 广告位置

]