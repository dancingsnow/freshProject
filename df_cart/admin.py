from django.contrib import admin
from .models import *

class CartInfoAdmin(admin.ModelAdmin):
    list_display = ['id','buy_user','buy_goods','buy_num']
    search_fields = ['id','buy_user','buy_goods','buy_num']

admin.site.register(CartInfo,CartInfoAdmin)

