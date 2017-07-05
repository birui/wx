#!/usr/bin/env python
import sys
import os
import django
import time
from datetime import datetime
from datetime import date
from django.db.models import Count
import random


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
        # print('group_name:', on_g_n)
    return on_g_n


def reply_text(wx_own):
    user_msg = Wx_account.objects.filter(wx_name=wx_own).values('Welcome')
    for i in user_msg:
        u_msg_v = i['Welcome']
    print(user_msg)


#
# end_time = Wx_group.objects.filter(group_name='coohua测试').values('end_time')
# print(end_time[0]['end_time'])
# test = range(1, 20)
# print(random.choice(test))
def reply_text(wx_own):
    group_Welcome = Cron_msg.objects.filter(msg_group='coohua测试').values('msg_content')
    id_list = []
    for i in group_Welcome:
        id_list.append(i['msg_content'])
    return(random.choice(id_list))


def group_Welcome(g_name):
    group_Welcome = Cron_msg.objects.filter(msg_group=g_name).values('msg_content')
    id_list = []
    for i in group_Welcome:
        id_list.append(i['msg_content'])
    return(random.choice(id_list))


today = date.today()
# # print(group_Welcome('coohua测试'))
# group_by = Group_user.objects.filter(group_time__year=today.year, group_time__month=today.month, group_time__day=today.day).values('group_own').order_by('id')
# print(group_by)


def wx_img_turn():
    # 可用微信
    Wx = Wx_account.objects.filter(online=1).values('wx_name')
    wx_name = []
    for i in Wx:
        wx_name.append(i['wx_name'])
    # 当天不到210用户的微信
    wx_210 = []
    for j in wx_name:
        count_users = Group_user.objects.filter(group_own=j, group_time__year=today.year, group_time__month=today.month, group_time__day=today.day).values('group_own').count()
        if int(count_users) < 210:
            wx_210.append(j)
    print(count_users, wx_210)


def group_Welcome(g_name):
    id_list = []
    try:
        group_Welcome_msg = Cron_msg.objects.filter(msg_group=g_name).values('msg_content')
    except Exception as e:
        group_Welcome_msg = Cron_msg.objects.filter(msg_group='default').values('msg_content')
    for i in group_Welcome_msg:
        id_list.append(i['msg_content'])
        # print(i)
    return(random.choice(id_list))


# welcome_text = group_Welcome(group_name(wx_user))


def welcome_text():
    welcome_t = group_Welcome(group_name('Enchanting'))
    test = Cron_msg.objects.filter(msg_group='new_user_7').values('msg_content')
    print(test['msg_content'])
    # for i in test:
    #     print(i['msg_content'])


def send_msg():
    # 上次发公告时间,
    end_time = Wx_group.objects.filter(group_name=group_name('Enchanting')).values('end_time')
    print(end_time)


send_msg()
