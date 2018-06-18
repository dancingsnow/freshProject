# coding:utf-8
from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$|^index/$',views.index),
    url(r'^list/$',views.list),
    url(r'^detail/(\d+)/$', views.detail),
    url(r'^adv/(\d+)/$',views.adv_link),  # 广告位置

]