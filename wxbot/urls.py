from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^chanell_check/$', views.wxgroup_check),
    url(r'^chanell_get/$', views.wxgroup_get),
    url(r'^wx_img/$', views.wx_img_turn),

]

