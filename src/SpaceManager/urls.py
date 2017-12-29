# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from SpaceManager.views import *
from SpaceManager.serializers import *

urlpatterns = patterns('',
      url(r'^', include(router.urls)),
)
