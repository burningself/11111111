# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from UserAndPrj.views import *
from UserAndPrj.serializers import *

urlpatterns = patterns('', 
    url(r'^', include(router.urls)),  
    url(r'^userview/$', user_view),
    url(r'^userproject/$', user_project),
    url(r'^curproject/$', curproject),
    url(r'costomPage/$', costomPage),
    url(r'prjusertree/$', prjusertree),
    url(r'companytree/$', companytree),
    url(r'adduser/$', createUser),

    url(r'^resetpwd/$', resetPassword),
      
)

