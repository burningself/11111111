# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from UserPrjConfig.views import *
from UserPrjConfig.serializers import *

urlpatterns = patterns('', 
    url(r'^', include(router.urls)),  
    url(r'addroleauths/$', addRoleAuths),
    url(r'delroleauths/$', delRoleAuths), 
    url(r'delprojectusers/$', delProjectUsers), 

    url(r'adduserroles/$', addUserRoles),
)

