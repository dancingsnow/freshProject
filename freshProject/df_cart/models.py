# coding:utf-8
from django.db import models

# 谁，买了什么东西，买了多少件
class CartInfo(models.Model):
    buy_user = models.ForeignKey('df_user.UserInfo')  # 注意这种关联形式
    buy_goods = models.ForeignKey('df_goods.GoodsInfo')
    buy_num = models.IntegerField(default=1)
