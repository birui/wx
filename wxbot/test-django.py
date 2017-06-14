#!/usr/bin/env python
import sys
import os
import django

# sys.path.append('/Users/admin/python/wxpy/wx')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'wx.settings'

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '/Users/admin/python/wxpy/wx')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wx.settings")

django.setup()

#----------------Use Django Mysql model----------------
from wxbot.models import Wx_group


def get_ip_list():
    ip_list = Wx_group.objects.all()
    return ip_list


aaa = get_ip_list()

print(aaa)
