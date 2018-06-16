# coding:utf-8
from django.db import models

# 这是用户信息相关的模型类
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40) # 密码进行了sha1加密，为40位数字
    uemail = models.CharField(max_length=40)
    isDelete = models.BooleanField(default=False)

    # 以下字段的内容在注册时原则上可以为空。
    # 如果设置null那么修改了数据库的表结构，则必须进行再迁移。但是设置default则为在python层面
    # 设置了一个值而已，会在存储时候设置一个值进去，等于填了一个'null'值进去。
    ucustomer = models.CharField(max_length=10,default='null')
    uaddr = models.CharField(max_length=100,default='null') # 联系地址，收货地址
    uzipcode = models.CharField(max_length=6,default='null') # 邮政编码
    uphone = models.CharField(max_length=11,default='null') # 这里只针对大陆手机号，可添加加密
    def __str__(self):
        return self.uname.encode('utf-8')


