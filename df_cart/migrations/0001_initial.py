# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20180622_1830'),
        ('df_user', '0002_auto_20180616_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buy_num', models.IntegerField(default=1)),
                ('buy_goods', models.ForeignKey(to='df_goods.GoodsInfo')),
                ('buy_user', models.ForeignKey(to='df_user.UserInfo')),
            ],
        ),
    ]
