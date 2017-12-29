# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from VehicleManager.views import *
from VehicleManager.serializers import *

urlpatterns = patterns('',
      url(r'^', include(router.urls)),
      url(r'upload_wentong/$', upload_wentong),

      url(r'vehiclemgr_index/$', vehiclemgr_index),
      url(r'carinfocount/$', carinfocount),

)
