# coding:utf-8
from django.contrib import admin
from .models import *
from django.contrib.admin import SimpleListFilter

class GoodsInline(admin.TabularInline):     # 也可以引入admin.StackedInline 为全部数列展示
    model = GoodsInfo
    extra = 2

# 关联查询（在添加type的时候，可以直接添加一对多的属性）
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle','isDelete']
    search_fields = ['ttitle']
    inlines = [GoodsInline]

# 重写了admin内部针对对应属性的过滤器。（覆盖admin的内部函数，实现按需求过滤）
class GremainFilter(SimpleListFilter):
    title = '货物库存剩余'  # 界面上要展现的内容
    parameter_name = 'gremain_num'  # 数据库内存储的具体的数据的列名称
    def lookups(self, request, model_admin):
        return [(0, '货物很充足(>200)'),(1, '需要补货(100~200)'), (2, '急需补货(<100)')]

    def queryset(self, request, queryset):
        value_num = self.value()   # self.value()得到的是个字符串，记得根据对应格式进行比较。
        if value_num == '0':
            return queryset.filter(gremain_num__gt=200) # 字段__方法
        elif value_num == '1':
            return queryset.filter(gremain_num__range=(100,200))
        elif value_num == '2':
            return queryset.filter(gremain_num__lt=100)

class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'gtitle', 'isDelete','gclick','gremain_num','gtype']
    list_filter = ['isDelete', 'gtype',GremainFilter]
    search_fields = ['gtitle']
    list_per_page = 10
    # fields = [('gtitle','gtype')]
    # 再添加数据时界面的呈现方式，属性的先后顺序，默认的排序方式（fields和fieldsets二选一,或者不用））
    # fieldsets = [
    #     ('basic', {'fields': ['btitle']}),
    #     ('more', {'fields': ['bpub_date']}),
    # ]


class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ['id','aname','alink','apic']
    search_fields = ['aname']

admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)
admin.site.register(Advertising,AdvertisingAdmin)

