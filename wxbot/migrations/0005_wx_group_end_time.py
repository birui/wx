# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-08 15:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxbot', '0004_auto_20170607_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='wx_group',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
