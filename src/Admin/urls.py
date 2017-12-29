# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


from Admin.views import *
from Admin.usermanger_views import *


urlpatterns = patterns('',
      url(r'pbstatus/$', pbstatus),
      url(r'stylecolor/$', stylecolor),

      url(r'^Navigation_editor/$', Navigation_editor),
      url(r'navigat/menutree/$', menutree),
      url(r'navigat/prjmenujson/$', prjmenujson),
      url(r'navigat/savemenu/$', savemenu),
      url(r'^navigation_editor_mobile/$', navigation_editor_mobile),
      url(r'navigat/menutreemobile/$', menutreemobile),
      url(r'navigat/prjmenujson_mobile/$', prjmenujson_mobile),
      url(r'^navigat/function_editor/$', function_editor),
      url(r'navigat/functiontree/$', functiontree),

      url(r'^adminconfigure/$',adminconfigure),
      url(r'^admincommonindex/$',admincommonindex),
      url(r'^adminmanagerpicture/$',adminmanagerpicture),
      url(r'^adminmanagerbackpic/$',adminmanagerbackpic),
      url(r'^adminmanagerlogopic/$',adminmanagerlogopic),
      url(r'^delimg/$',delimg),
      url(r'^cropimg/$',cropimg),

      url(r'prjconfig/baseinfo/$', baseinfo),

      url(r'^directorynotify/$', directorynotify),
      url(r'^directoryauth/$', directoryauth),

 
      url(r'^noticeconfig/$', noticiConfig),

      url(r'^usermanager_vue/$', usermanager_vue),
      url(r'^usermanager_vue/addusers/$', addusers_vue),
      url(r'^usermanager_vue/guideusers/$', guideusers_vue),
      url(r'^usermanager_vue/editRole/$', editRole_vue),
      url(r'^usermanager_vue/batchUser/$', batchUser_vue),
      url(r'^usermanager_vue/divisionManage/$', divisionManage_vue),
      url(r'^usermanager_vue/companyManage/$', companyManage_vue),
      url(r'^usermanager_vue/majorManage/$', majorManage_vue),
         
      url(r'^usermanager_vue/componentType/$', componentType_vue),
      url(r'^usermanager_vue/typeMeeting/$', typeMeeting_vue),
      url(r'^usermanager_vue/qualityAccept/$', qualityAccept_vue),
      url(r'^usermanager_vue/procedureAccept/$', procedureAccept_vue),

)
