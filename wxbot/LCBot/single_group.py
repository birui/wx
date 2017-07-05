#!/usr/bin/env python3
# coding: utf-8
import mysql_config as cfg
import pymysql
import sys
import time
import pickle
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import django
import random
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../../')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wx.settings")
django.setup()

from wxbot.models import *
from wxpy import *
import re
from wxpy.utils import start_new_thread

# False
bot = Bot('bot.pkl', console_qr=False)

'''
开启 PUID 用于后续的控制
'''
bot.enable_puid('wxpy_puid.pkl')

# 获取当前用户
wx_user = str(bot)[6:-1]
print(wx_user)

# 获取要使用的群名


def group_name(own):
    # 无结束时间且在线的群（在线=少于100）
    on_g = Wx_group.objects.filter(group_own=own, online=1).values('group_name')
    for i in on_g:
        on_g_n = i['group_name']
        # print('group_name:', on_g_n)
    return on_g_n

#######


# 下方为函数定义

def get_time():
    return str(time.strftime("%Y-%m-%d %H:%M:%S"))


'''
机器人消息提醒设置
'''
# name换成；group_name(wx_user)可以换成一个固定的群或者人
group_receiver = ensure_one(bot.groups().search(group_name(wx_user)))
logger = get_wechat_logger(group_receiver)
logger.error(str("机器人登陆成功！" + get_time()))

'''
重启机器人
'''


def _restart():
    os.execv(sys.executable, [sys.executable] + sys.argv)


'''
定时报告进程状态
'''


def heartbeat():
    while bot.alive:
        time.sleep(3600)
        # noinspection PyBroadException
        try:
            logger.error(get_time() + " 机器人目前在线,共有好友 【" + str(len(bot.friends())) + "】 群 【 " + str(len(bot.groups())) + "】")
        except ResponseError as e:
            if 1100 <= e.err_code <= 1102:
                logger.critical('LCBot offline: {}'.format(e))
                _restart()


start_new_thread(heartbeat)

#######
'''
入群邀请语：
'''


def reply_text(wx_own):
    user_msg = Wx_account.objects.filter(wx_name=wx_own).values('Welcome')
    for i in user_msg:
        u_msg_v = i['Welcome']
    return u_msg_v


# reply_text = reply_text(wx_user)

'''
随机群内欢迎语：
'''


# def group_Welcome(g_name):
#     group_msg = Wx_group.objects.filter(group_name=g_name).values('Welcome')
#     for i in group_msg:
#         msg_gw = i['Welcome']
#     return msg_gw

def group_Welcome(g_name):
    id_list = []
    try:
        group_welcome_msg = Cron_msg.objects.filter(msg_group=g_name).values('msg_content')
    except Exception as e:
        group_welcome_msg = Cron_msg.objects.filter(msg_group='default').values('msg_content')
    for i in group_welcome_msg:
        id_list.append(i['msg_content'])
    return(random.choice(id_list))

# welcome_text = group_Welcome(group_name(wx_user))


def welcome_text():
    welcome_t = group_Welcome(group_name(wx_user))
    return welcome_t


# bot2 = Bot('bot2.pkl', console_qr=False)
print(bot.groups())
# target_group = bot.groups().search(group_name(wx_user))[0]

# 群名


def target_group():
    target_group_1 = bot.groups().search(group_name(wx_user))[0]
    # 如果群成员超过100，将群下线
    if len(target_group_1) >= 100:
        insertdata = Wx_group(online=0)
        insertdata.save()
    # print('target_group_1:', target_group_1)
    return target_group_1


target_group()
# 群成员个数
print(len(target_group()))


'''
邀请消息处理
'''


def get_new_member_name(msg):
    # itchat 1.2.32 版本未格式化群中的 Note 消息
    from itchat.utils import msg_formatter
    msg_formatter(msg.raw, 'Text')

    for rp in rp_new_member_name:
        # match = rp.search(logger)
        match = rp.search(msg.text)
        if match:
            return match.group(1)

# def init_msg():
#     online_group(wx_user)


'''
邀请信息处理
'''
rp_new_member_name = (
    re.compile(r'^"(.+)"通过'),
    re.compile(r'邀请"(.+)"加入'),
)

'''
处理加好友请求信息。
如果验证信息文本是字典的键值之一，则尝试拉群。
'''

# 自动接收好友请求


@bot.register(msg_types=FRIENDS)  # 注册好友请求消息
def new_friends(msg):
    group_owner = bot
    user = msg.card.accept()  # 接受好友 (msg.card 为该请求的用户对象)
    target_group().add_members(user, use_invitation=True)  # user是要加入的用户，use_invitation – 使用发送邀请的方式
    user_data = str(user)[9:-1].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
    user_sex = user.sex
    user_province = user.province
    user_city = user.city
    # user_puid = bot.friends().search(user_data)[0].puid
    user_puid = user.puid
    # print(user_puid)
    insertdata = Group_user(user_name=user_data, user_sex=user_sex, user_province=user_province, user_city=user_city, puid=user_puid)  # 入库
    insertdata.save()
    user.send(reply_text(wx_user))

# 加群


@bot.register(target_group(), NOTE)
def send_msg():
    # 上次发公告时间,
    time_tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if os.path.exists('last_time.pkl'):
        pkl_file = open('last_time.pkl', 'rb')
        last_time_dic = pickle.load(pkl_file)
        last_time = last_time_dic['last_time']
        count_users = Group_user.objects.filter(group_time__gt=last_time).count()
        # 上次发公告以来如果有7个新人进群就再发一次公告
        # if int(count_users) >= 7 and len(target_group()) >= 30:#test
        print(count_users, last_time)
        if int(count_users) >= 2 and len(target_group()) >= 10:
            # print('send msg!!!!===>{0}' .format(last_time))
            # notice_msg = Cron_msg.objects.filter(msg_group='new_user_7').values('msg_content')
            # target_group().send('公告：{0}' .format(group_msg))
            # 发送公告信息到群
            notice_msg = Cron_msg.objects.filter(msg_group='new_user_7').values('msg_content', 'msg_type').order_by('order_id')
            for i in notice_msg:
                if i['msg_type'] == 'img':
                    target_group().send_image(i['msg_content'])
                elif i['msg_type'] == 'txt':
                    target_group().send(i['msg_content'])
            # 发完公告改时间
            last_time['last_time'] = time_tamp
            pickle.dump(last_time, pkl_file)

    else:
        last_time = {'last_time': time_tamp}
        pkl_file = open('last_time.pkl', 'wb')
        pickle.dump(last_time, pkl_file)

    pkl_file.close()

# 欢迎进群


@bot.register(target_group(), NOTE)
def welcome(msg):
    name = get_new_member_name(msg)
    my_friend = bot.friends().search(name)[0]
    puid_nu = my_friend.puid
    time_tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(name, puid_nu)
    if name:
        # 将刚刚入群的用户添加到数据库
        group_owner = str(bot)[6:-1]
        # group_name = group_name(wx_user)
        Group_user.objects.filter(puid=puid_nu).update(group_name=group_name(wx_user), group_own=group_owner, group_time=time_tamp)

        # 1.如果达到60人一个群则自动建群
        # 2.如果新人达到7个就发一次公告
        try:
            # 发送公告信息
            send_msg()
        except Exception as e:
            print('new_user_7 出错!! %s' % e)
        # 发送公告信息
        return welcome_text().format(name)

# 定时任务

# 定时1： 18点人群大于50发送话术1，19点发送话术2 #如果不到50人？


def tick_18():
    print('tick_18')
    end_time = Wx_group.objects.filter(group_name=group_name(wx_user)).values('end_time')
    # 注意群是未结束状态
    if end_time[0]['end_time'] is None:
        # if len(target_group()) >= 50:
        if len(target_group()) >= 10:  # test
            notice_msg = Cron_msg.objects.filter(msg_group='tick_18').values('msg_content', 'msg_type').order_by('order_id')
            # target_group().send('1.==>Tick! The time is: %s' % datetime.now())
            # target_group().send(notice_msg)
            # print(notice_msg)
            for i in notice_msg:
                if i['msg_type'] == 'img':
                    target_group().send_image(i['msg_content'])
                    # print(i['msg_content'])
                elif i['msg_type'] == 'txt':
                    target_group().send(i['msg_content'])
                    # print(i['msg_content'])


scheduler_18 = BackgroundScheduler()
scheduler_18.add_job(tick_18, 'cron', day_of_week='0-6', hour='18', minute='00')
# scheduler_18.add_job(tick_18, 'cron', day_of_week='0-6', minute='*/5')  # test
scheduler_18.start()
# 19点发送话术2


def tick_19():
    end_time = Wx_group.objects.filter(group_name=group_name(wx_user)).values('end_time')
    if end_time[0]['end_time'] is None:
        #notice_msg = Cron_msg.objects.filter(msg_name='tick_19', msg_group='cron').values('msg_content')
        notice_msg = Cron_msg.objects.filter(msg_group='tick_19').values('msg_content', 'msg_type').order_by('order_id')
        # target_group().send(notice_msg)
        for i in notice_msg:
            if i['msg_type'] == 'img':
                target_group().send_image(i['msg_content'])
                # print(i['msg_content'])
            elif i['msg_type'] == 'txt':
                target_group().send(i['msg_content'])


scheduler_19 = BackgroundScheduler()
# scheduler_19.add_job(tick_19, 'cron', day_of_week='0-6', hour='19', minute='00')
scheduler_19.add_job(tick_19, 'cron', day_of_week='0-6', minute='*/5')
scheduler_19.start()


# 定时2： 到19：40若群有80人则记录群结束，并记录“结束时间”，并发送话术1，若不足80发送话术2不设置结束。
def tick_19_40():
    end_time = Wx_group.objects.filter(group_name=group_name(wx_user)).values('end_time')
    if end_time[0]['end_time'] is None:
        time_tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if len(target_group()) >= 80:
            notice_msg = Cron_msg.objects.filter(msg_group='tick_19_40_1').values('msg_content', 'msg_type').order_by('order_id')
            for i in notice_msg:
                if i['msg_type'] == 'img':
                    target_group().send_image(i['msg_content'])
                elif i['msg_type'] == 'txt':
                    target_group().send(i['msg_content'])
            Wx_group.objects.filter(group_name=group_name(wx_user)).update(end_time=time_tamp)
        else:
            notice_msg = Cron_msg.objects.filter(msg_group='tick_19_40_2').values('msg_content', 'msg_type').order_by('order_id')
            for i in notice_msg:
                if i['msg_type'] == 'img':
                    target_group().send_image(i['msg_content'])
                    # print(i['msg_content'])
                elif i['msg_type'] == 'txt':
                    target_group().send(i['msg_content'])


scheduler_19_40 = BackgroundScheduler()
# scheduler_19_40.add_job(tick_19_40, 'cron', day_of_week='0-6', hour='19', minute='40')
scheduler_19_40.add_job(tick_19_40, 'cron', day_of_week='0-6', minute='*/6')
scheduler_19_40.start()

# 定时3：群结束后，每天8点发推送连续18天


def tick_20_18():
    try:
        end_time = Wx_group.objects.filter(group_name=group_name(wx_user)).values('end_time')
        if end_time is not None:
            end_time_str = str(end_time[0]['end_time'])
            end_timeArray = time.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
            end_timeStamp = int(time.mktime(end_timeArray))

            local_time_tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            local_timeArray = time.strptime(local_time_tamp, "%Y-%m-%d %H:%M:%S")
            local_timeStamp = int(time.mktime(local_timeArray))

            if int(local_timeStamp - end_timeStamp) >= 86400:
                nu_dt = int(int(local_timeStamp - end_timeStamp) / 86400) - 1
                if 0 <= nu_dt <= 18:
                    end_msg = Cron_msg.objects.filter(msg_group='%dday' % nu_dt).values('msg_content', 'msg_type').order_by('order_id')
                    # print(end_msg[0]['msg_content'])
                    for i in end_msg:
                        if i['msg_type'] == 'img':
                            target_group().send_image(i['msg_content'])
                            # print(i['msg_content'])
                        elif i['msg_type'] == 'txt':
                            target_group().send(i['msg_content'])
                    # target_group().send(end_msg[0]['msg_content'])
    except Exception as e:
        print('出错了!! %s' % e)


scheduler_20_18 = BackgroundScheduler()
# scheduler_20_18.add_job(tick_20_18, 'cron', day_of_week='0-6', hour='20', minute='00')
scheduler_20_18.add_job(tick_20_18, 'cron', day_of_week='0-6', minute='*/7')
scheduler_20_18.start()


my_friend = ensure_one(bot.search(group_name(wx_user)))
tuling = Tuling(api_key='1996a93aebba489baed8346239c6111f')

# 使用图灵机器人自动与指定好友聊天


@bot.register(my_friend, TEXT)
def auto_reply(msg):
    # 如果是群聊，但没有被 @，则不回复
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    else:
        # 回复消息内容和类型
        # return '收到消息: {} ({})'.format(logger, msg.type)
        tuling.do_reply(msg)

# target_group.send('Hello, WeChat!') 发送信息到群

#======多开=====

#
# @bot2.register(msg_types=FRIENDS)  # 注册好友请求消息
# def new_friends(msg):
#     user = msg.card.accept()  # 接受好友 (msg.card 为该请求的用户对象)
#     target_group.add_members(user, use_invitation=True)  # user是要加入的用户，use_invitation – 使用发送邀请的方式
#     user.send(reply_text)
#
#
# @bot2.register(target_group, NOTE)
# def welcome(msg):
#     name = get_new_member_name(msg)
#     if name:
#         return welcome_text.format(name)


embed()
