# coding:utf-8
from django.contrib import admin
from .models import *
# Register your models here.
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['oid','ouser','otime','ototal','isPay']
    search_fields = ['oid','ouser','otime','ototal']
    list_filter = ['isPay']

class OrderDetailAdmin(admin.ModelAdmin):
    list_filter = ['order','goods','price','count']
    search_fields = ['order','goods','price','count']


admin.site.register(OrderInfo,OrderInfoAdmin)
admin.site.register(OrderDetailInfo,OrderDetailAdmin)