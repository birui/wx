from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.template import loader
from .models import *
from django.core import serializers
import json
from datetime import date
from django.db.models import Count
from django.core import serializers
from django.conf import settings





def index(request):
    monitordomain_v = Wx_group.objects.all()
    jsondata = serializers.serialize("json", monitordomain_v)
    last_ten = json.loads(jsondata)
    result = []
    for i in last_ten:
        result.append(i['fields'])

    return render(
        request,
        'wxbot/chanell.html',
        {'last_ten': result}
    )

def wxgroup_get(request):
    wxgroup_db = Wx_group.objects.all()
    sid = str(Wx_group.objects.last())
    # print(sid)
    jsondata = serializers.serialize("json", wxgroup_db.filter(id=sid))
    return HttpResponse(jsondata)


def wxgroup_check(request):

    if request.method == 'POST':
        a = request.POST.get('a')
        d = request.POST.get('d')
        # print a,b,c,d
        data_v = Wx_group(group_name=a,group_own=d)
        data_v.save()
    return HttpResponse('OK')

#二维码轮换http://127.0.0.1:8000/wxbot/wx_img/
def wx_img_turn(request):

    today = date.today()
    #今天的加群的用户总数
    count_users = Group_user.objects.filter(group_time__year= today.year,group_time__month=today.month,group_time__day=today.day).values('group_own').count()
    #SELECT group_own, COUNT(user_name) AS dcount FROM Group_user GROUP BY group_own
    group_by = Group_user.objects.filter(group_time__year= today.year,group_time__month=today.month,group_time__day=today.day).values('group_own').annotate(dcount=Count('user_name'))
    limit_210 = []
    for i in group_by:
        if i['dcount'] < 20:
            limit_210.append(i['group_own'])
        elif not i['dcount']:
            limit_210.append(i['group_own'])


    if limit_210:
        img_d = Wx_account.objects.filter(wx_name=limit_210[0]).values('img_url')
        # img_url = serializers.serialize("json",  Wx_account.objects.all())
        for i in img_d:
            img_d = i['img_url']
        document_root = settings.BASE_DIR
        print(document_root)
        image_data = open("%s/wxbot/static/weixin/img/%s" %(document_root,img_d), "rb").read()
        return HttpResponse(image_data, content_type="image/png")
    else:
        return HttpResponse('没有可用微信了!!')


