# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertising',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aname', models.CharField(max_length=20)),
                ('apic', models.ImageField(upload_to=b'df_goods_adv/')),
                ('alink', models.CharField(default=b'/adv/#', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gtitle', models.CharField(max_length=20)),
                ('gpic', models.ImageField(upload_to=b'df_goods/')),
                ('gprice', models.DecimalField(max_digits=5, decimal_places=2)),
                ('gunit', models.CharField(max_length=10)),
                ('isDelete', models.BooleanField(default=False)),
                ('gclick', models.IntegerField()),
                ('gdesc', models.CharField(max_length=200)),
                ('gdetail', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ttitle', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(to='df_goods.TypeInfo'),
        ),
    ]
