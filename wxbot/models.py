from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.timezone import now, timedelta
from datetime import datetime



# Create your models here.
#好友表
class Group_user(models.Model):
    user_name = models.CharField(max_length=200)
    group_name = models.CharField(max_length=200)
    group_own = models.CharField(max_length=200)
    group_time = models.DateTimeField(blank=True,null=True)
    friend_time = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return str(self.id)

#微信账户
class Wx_account(models.Model):
    wx_name = models.CharField(max_length=200)
    use_time = models.DateTimeField(auto_now_add = True)
    friend_count = models.IntegerField(blank=True,null=True,default=0)
    img_url = models.CharField(max_length=500)
    Welcome = models.TextField(blank=True, null=True)
    #0下线 1上线
    online = models.IntegerField(blank=True,null=True)
    def __unicode__(self):
        return str(self.id)
#微信群
@python_2_unicode_compatible
class Wx_group(models.Model):
    group_name = models.CharField(max_length=200)
    group_count = models.CharField(max_length=200,blank=True,null=True)
    use_time = models.DateTimeField(auto_now_add = True)
    end_time = models.DateTimeField(blank=True,null=True)
    group_own = models.CharField(max_length=200)
    Welcome = models.TextField(blank=True, null=True)
    online = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return str(self.id)
#定时任务and消息
class Cron_msg(models.Model):
    msg_name = models.CharField(max_length=20)
    msg_group = models.CharField(max_length=200,blank=True,null=True)
    msg_content = models.TextField(blank=True, null=True)
    msg_type = models.CharField(max_length=20,default='txt')
    def __str__(self):
        return str(self.id)
