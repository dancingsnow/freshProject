# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertising',
            name='alink',
            field=models.CharField(default=b'/adv/#/', max_length=100),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gclick',
            field=models.IntegerField(default=0),
        ),
    ]
