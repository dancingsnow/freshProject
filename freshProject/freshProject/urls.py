# coding:utf-8
"""freshProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, static
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),  # 富文本编辑器
    url(r'^user/',include('freshProject.df_user.urls',namespace='user')),  # 命名空间，用于反向解析地址，便于维护
    url(r'^',include('freshProject.df_goods.urls')),
    url(r'^cart/',include('freshProject.df_cart.urls')), # 购物车
    url(r'^order/',include('freshProject.df_order.urls')), # 订单
    url(r'^search/',include('haystack.urls')),  # 全文检索
]

