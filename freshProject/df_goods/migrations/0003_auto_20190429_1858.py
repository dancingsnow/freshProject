# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20180622_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertising',
            name='alink',
            field=models.CharField(max_length=100, default='/adv/#/'),
        ),
        migrations.AlterField(
            model_name='advertising',
            name='apic',
            field=models.ImageField(upload_to='df_goods_adv/'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gpic',
            field=models.ImageField(upload_to='df_goods/'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gunit',
            field=models.CharField(max_length=10, default='500g'),
        ),
    ]
