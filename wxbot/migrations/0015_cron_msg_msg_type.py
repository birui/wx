# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxbot', '0014_remove_cron_msg_msg_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cron_msg',
            name='msg_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
