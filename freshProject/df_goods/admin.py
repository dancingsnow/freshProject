from django.contrib import admin
from .models import *
# Register your models here.

class TypeInfoAdmin(admin.ModelAdmin):
    pass

class GoodsInfoAdmin(admin.ModelAdmin):
    pass

class AdvertisingAdmin(admin.ModelAdmin):
    pass

admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)
admin.site.register(Advertising,AdvertisingAdmin)