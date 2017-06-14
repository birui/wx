# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('group_name', models.CharField(max_length=200)),
                ('group_own', models.CharField(max_length=200)),
                ('join_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wx_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wx_name', models.CharField(max_length=200)),
                ('use_time', models.CharField(max_length=200)),
                ('friend_count', models.IntegerField(blank=True, default=0, null=True)),
                ('img_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
