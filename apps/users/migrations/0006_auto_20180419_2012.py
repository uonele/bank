# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-19 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180419_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradeinfo',
            name='trade_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='\u4ea4\u6613\u6d41\u6c34\u53f7'),
        ),
    ]
