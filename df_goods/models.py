# coding:utf-8
from django.db import models
from tinymce.models import HTMLField

# 商品分类
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        # return self.ttitle.encode('utf-8')
        return self.ttitle
"""
针对admin报错时的处理：
    " TypeError: __str__returned non-string (type bytes) "
    
某个django项目从python2迁移到python3的过程中，出现了以下问题： 
TypeError: __str__returned non-string (type bytes) 
经查证，是模型类中的 __str__ 方法造成的，原因是python3中 __str__ 不能接收bytes类型的数据，这和python2/3的编解码方式是有关系的。 
下面给出python2和python3的写法：

    def __str__(self):
        return self.typename.encode("utf-8") # python2写法
        return self.typename                 # python3写法
"""


# 商品信息
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20) # 商品名称
    gpic = models.ImageField(upload_to='df_goods/') # 图片
    gprice = models.DecimalField(max_digits=5,decimal_places=2) # 价格
    gunit = models.CharField(max_length=10,default='500g') # 单位
    isDelete = models.BooleanField(default=False)
    gclick = models.IntegerField(default=0)  # 可以在此记录下点击量（人气），减小数据库的压力。
                                    # 如果按销量等排序，最好也建立一个字段，进行记录。
    gdesc = models.CharField(max_length=200) # 商品简介
    gdetail = HTMLField() # 可以有后台人员在admin利用富文本编辑器进行商品细节的编辑
    gtype = models.ForeignKey('TypeInfo') # 外键，归属于哪类商品
    gremain_num = models.IntegerField(default=1000) # 库存剩余数量
    # 还可以添加一个库存总数，每买走减去1.
    def __str__(self):
        # return self.gtitle.encode('utf-8')
        return self.gtitle

# 广告位信息
class Advertising(models.Model):
    aname = models.CharField(max_length=20)  # 广告名称
    apic = models.ImageField(upload_to='df_goods_adv/') # 广告的图片
    alink = models.CharField(max_length=100,default='/adv/#/') # 默认链接为/adv/数字
    # 可以添加isDelete选项，实现广告的更换，并根据需要选择是否彻底删除之前的广告
    def __str__(self):
        # return self.aname.encode('utf-8')
        return self.aname



