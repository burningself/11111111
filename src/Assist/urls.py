# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from Assist.views_biaodan import *
from Assist.views import *
from Assist.views_meeting import *
from Assist.serializers import *
from Assist.views_weather import *


urlpatterns = patterns('',
      url(r'^', include(router.urls)),

      url(r'^viewpdf/$', viewpdf),
      url(r'^shigongriji/$', shigongriji),
      
      url(r'biaodanmanerger/$', biaodan_manerger),
      url(r'biaodanedit/$', biaodan_edit),
      url(r'biaodan/$', biaodan_biaodan),
      url(r'biaodanmuban/$', biaodan_muban),
      url(r'biaodanmuban/getrelatestep/$', biaodan_getrelatestep),
      url(r'projecttask/builddiarycreate/$',builddiaryform),
      url(r'projecttask/createbuilddiary/$',builddiary_create),
      url(r'projecttask/savebuilddiary/$',builddiary_save),
      url(r'projecttask/editbuilddiary/$',builddiary_edit),
      url(r'projecttask/builddiaryprint/$',builddiary_print),

      url(r'todolist/$', todolist),
      url(r'^baidumap/$', baidumap),
      url(r'^huiyi/$', huiyi),
      url(r'^edithuiyi/$',edithuiyi),
      url(r'^createhuiyi/$', createhuiyi),
      url(r'^loadMeetingDatas/$',loadMeetingDatas),
      url(r'^getMeetingMember/$',getMeetingMember),
      url(r'^getMeetingFile/$',getMeetingFile),
      url(r'^deleteMeeting/$',deleteMeeting),
      url(r'^loadHuiyiInfo/$',loadHuiyiInfo),
      url(r'^uploadJiyao/$',uploadJiyao),
      url(r'^zhouqihuiyi/$',zhouqihuiyi),
      url(r'^createzhouqihuiyi/$',createzhouqihuiyi),
      url(r'^deleteMeetingZhouqi/$',deleteMeetingZhouqi),
      url(r'^loadHuiyiZhouqiInfo/$',loadHuiyiZhouqiInfo),
      url(r'^getMeetingZhouqiMember/$',getMeetingZhouqiMember),
      url(r'^editzhouqihuiyi/$',editzhouqihuiyi),
      url(r'^zhilianglihui/$', zhilianglihui),

      url(r'^shortcut/getcategorylist/$',shortcut_getcategorylist),
      url(r'^shortcut/getcategoryfunction/$',shortcut_getcategoryfunction),
      url(r'^shortcut/getusershortcutlist/$',shortcut_getusershortcutlist),
      url(r'^shortcut/setusershortcut/$',shortcut_setusershortcut),
      url(r'^shortcut/saveshortcutseq/$',shortcut_saveshortcutseq),

      url(r'^meetnotice/$',meetnotice),
      url(r'^managerattend/$',managerattend),
      url(r'^loadweather/$',loadweather),
)
