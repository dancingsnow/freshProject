# coding:utf-8
from django.db import models

# 订单 模型类
# 编号:谁的订单、订单日期、订单总金额（可以计算，也可以直接保存）、支付状态、订单的收货地址（付款的时候可能会更改）
class OrderInfo(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)  # 手动创建主键，迁移时便不在创建
    ouser = models.ForeignKey('df_user.UserInfo')
    otime = models.DateTimeField(auto_now=True) # 为最后一次更改数据的时间
    ototal = models.DecimalField(max_digits=6,decimal_places=2)  # 总价
    isPay = models.BooleanField(default=False)
    oaddr = models.CharField(max_length=150)  # 用于保存具体订单的地址
    def __str__(self):
        return self.oid

# 订单的具体信息:订单编号、商品信息、商品单价（买的时候可能跟现在不同，所以订单里边最好记录下。单位不变）、数量、小计(界面再计算)
class OrderDetailInfo(models.Model):
    order = models.ForeignKey(OrderInfo)
    goods = models.ForeignKey('df_goods.GoodsInfo')
    price = models.DecimalField(max_digits=5,decimal_places=2)
    count = models.IntegerField()
    def __str__(self):
        return self.order.oid