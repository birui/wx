#!/usr/bin/env python
import sys
import os
import django
import time
from datetime import datetime


# sys.path.append('/Users/admin/python/wxpy/wx')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'wx.settings'

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../../')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wx.settings")

django.setup()

#----------------Use Django Mysql model----------------
from wxbot.models import *

time_tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_ip_list():
    ip_list = Wx_group.objects.all()
    # insertdata = Group_user(user_name='coohuatest2', group_name='test2', group_own='tt')
    # print(insertdata)
    # insertdata.save()
    # q1 = Group_user.objects.filter(join_time__lt=time_tamp).values("join_time")
    name = " 毕锐"
    test = Group_user.objects.filter(user_name='毕锐').update(group_name='test', group_own='bot', group_time=time_tamp)
    return test


def user_Welcome(wx_own):
    msg = Wx_account.objects.filter(wx_name=wx_own).values('Welcome')
    for i in msg:
        msg_v = i['Welcome']
    return msg_v


def group_Welcome(g_name):
    msg = Wx_group.objects.filter(group_name=g_name).values('Welcome')
    for i in msg:
        msg_v = i['Welcome']
    return msg_v


def online_group(own):
    on_g = Wx_group.objects.filter(group_own=own, online=1).values('group_name')

    # for i in on_g:
    # on_g_n = i['group_name']
    return on_g[0]['group_name']


def f1(x, y):
    return (x, y)


def tick_20_18():
    end_time = Wx_group.objects.filter(group_name='test5').values('end_time')
    if end_time:
        end_time_str = str(end_time[0]['end_time'])
        end_timeArray = time.strptime(end_time_str, "%Y-%m-%d %H:%M:%S.%f")
        end_timeStamp = int(time.mktime(end_timeArray))

        local_time_tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        local_timeArray = time.strptime(local_time_tamp, "%Y-%m-%d %H:%M:%S")
        local_timeStamp = int(time.mktime(local_timeArray))

        date_nu = range(0, 18)
        if int(local_timeStamp - end_timeStamp) > 86400:
            nu_dt = int(int(local_timeStamp - end_timeStamp) / 86400) - 1
            if 0 <= nu_dt <= 18:
                end_msg = Cron_msg.objects.filter(msg_name='%dday' % nu_dt, msg_group='18day_msg').values('msg_content')
                print(end_msg[0]['msg_content'])


# aaa = online_group('Enchanting')

def group_name(own):
    # 无结束时间且在线的群（在线=少于100）
    on_g = Wx_group.objects.filter(group_own=own, online=1).values('group_name')
    for i in on_g:
        on_g_n = i['group_name']
        print('group_name:', on_g_n)
    return on_g_n


def reply_text(wx_own):
    user_msg = Wx_account.objects.filter(wx_name=wx_own).values('Welcome')
    for i in user_msg:
        u_msg_v = i['Welcome']
    print(user_msg)


group_name('Enchanting')
# reply_text('Enchanting')

# print(aaa)
