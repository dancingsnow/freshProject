# coding:utf-8
from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^register/$',views.register), # 注册界面
    url(r'^check_uname/',views.check_uname),
    url(r'^register_handle/$',views.register_handle),
    url(r'^login/$',views.login), #　登录界面
    url(r'^login_handle/$',views.login_handle),
    url(r'^login_handle_2/$', views.login_handle_2),

    url(r'^user_center_info/$',views.user_center_info),  # 用户中心界面(默认为个人信息界面)
    url(r'^user_center_order/$',views.user_center_order),   # 用户中心-全部订单
    url(r'^user_center_site/$',views.user_center_site),   # 用户中心-收货地址
    url(r'^user_center_site_handle/$',views.user_center_site_handle),  # 用户中心-收货地址-处理提交上来的地址信息。
]

