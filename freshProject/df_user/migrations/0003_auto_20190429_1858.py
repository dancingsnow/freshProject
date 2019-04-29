# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20180616_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uaddr',
            field=models.CharField(max_length=100, default='null'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ucustomer',
            field=models.CharField(max_length=10, default='null'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uphone',
            field=models.CharField(max_length=11, default='null'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uzipcode',
            field=models.CharField(max_length=6, default='null'),
        ),
    ]
