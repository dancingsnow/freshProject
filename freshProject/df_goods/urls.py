# coding:utf-8
from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$|^index/$',views.index),
    url(r'^list/$',views.list),
    url(r'^detail/(\w+\d+)/$', views.detail), # 商品细节
    url(r'^adv/(\d+)/$',views.adv_link),  # 广告位置

]