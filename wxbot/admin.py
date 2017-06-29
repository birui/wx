from django.contrib import admin
from wxbot.models import *

# Register your models here.
class Group_user_show(admin.ModelAdmin):
    #显示字段
    list_display = ('user_name','user_sex','user_province','user_city','group_name', 'group_own','group_time','friend_time','puid')
    #指定列表过滤器,页面右边
    list_filter = ('group_name',)
    # 指定要搜索的字段
    search_fields = ('user_name', 'group_name','group_own',)


class Wx_account_show(admin.ModelAdmin):
    #显示字段
    list_display = ('wx_name','Welcome','use_time', 'friend_count','img_url','online')
    #指定列表过滤器,页面右边
    list_filter = ('wx_name',)
    # 指定要搜索的字段
    search_fields = ('wx_name', 'use_time')


class Wx_group_show(admin.ModelAdmin):
    #显示字段
    list_display = ('group_name','group_count', 'use_time','end_time','group_own','online')
    #指定列表过滤器,页面右边
    list_filter = ('group_name',)
    # 指定要搜索的字段
    search_fields = ('group_name', 'use_time')

class Cron_msg_show(admin.ModelAdmin):
    #显示字段
    list_display = ('msg_group', 'msg_content' , 'msg_type' , 'order_id')
    #指定列表过滤器,页面右边
    list_filter = ('msg_group',)
    # 指定要搜索的字段
    search_fields = ( 'msg_group',)

admin.site.register(Wx_account,Wx_account_show)
admin.site.register(Group_user,Group_user_show)
admin.site.register(Wx_group,Wx_group_show)
admin.site.register(Cron_msg,Cron_msg_show)

