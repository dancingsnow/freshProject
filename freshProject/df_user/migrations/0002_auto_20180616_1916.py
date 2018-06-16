# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uaddr',
            field=models.CharField(default=b'null', max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ucustomer',
            field=models.CharField(default=b'null', max_length=10),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uphone',
            field=models.CharField(default=b'null', max_length=11),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uzipcode',
            field=models.CharField(default=b'null', max_length=6),
        ),
    ]
