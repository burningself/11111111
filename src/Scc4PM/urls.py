# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from UserAndPrj.views import *
from TaskAndFlow.views import *
from TaskAndFlow.viewsimport import *
from Scc4PM import settings
import os

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Scc4PM.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^welcome/$', welcome),
    url(r'^$', RedirectView.as_view(url='/index/')),
    url(r'^index/$', index_view),
    # 新增目录
    url(r'^index_vue/$', index_view_vue),
    url(r'^index_vue/model/$', index_view_vue_model),
    url(r'^index_vue/table/$', index_view_vue_table),
    url(r'^login_vue/$', login_vue),

    url(r'^index/data/$', index_data),
    url(r'^index/table/$', index_table),
    url(r'^introduce/$', introduce),
    url(r'^introduce/addressList/$', addressList_vue),

    url(r'^introducetable/$', introducetable),
    url(r'^feedback/$', feedback),
    url(r'^feedbacks/$', feedbacks),
    url(r'^login/$', login),
    url(r'^changepass/$', changepassword),
    url(r'^logout/$', logout),
    url(r'^error_404/$', error_404),
    url(r'^error_403/$', error_403),
    url(r'^error_500/$', error_500),
    url(r'^wslogin/$', wslogin),
    url(r'^wslogout/$', wslogout),
    url(r'^userinfo/$', userinfo),

    url(r'^progress/schedule/$', progress_schedule),
    url(r'^progress/projecttask/list/$', progress_projecttask),

    url(r'^progress/goujian/$', progress_goujian),
    url(r'^progress/goujian/loadTable/$', progress_goujian_load_table),
    url(r'^progress/goujian/loadCount/$', progress_goujian_load_count),
    url(r'^progress/goujian/loadElevation/$', progress_goujian_load_elevation),
    url(r'^progress/goujian/count_mobile/$', progress_goujian_count),

    url( r'^upload/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.UPLOAD_DIR } ),
    url( r'^doctemplate/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.DOCTEMPLATE_DIR } ),
#    url(r'^upload_script/$',uploadify_script),
#    url(r'^delete_uploadfile/$',profile_delte),

    url(r'^uploadfile_conc/$',uploadfile_conc),
    url(r'^uploadfile_conc2/$',uploadfile_conc2),
    url(r'^uploadfile_blob/$',uploadfile_blob),
    url(r'^uploadfile_ocf/$',uploadfile_ocf),
    url(r'^del_uploadfile/$',del_uploadfile),
    url(r'^importusersfile/$',importusersfile),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += patterns ('',
  url(r'^task/', include('TaskAndFlow.urls')),
)

urlpatterns += patterns ('',
  url(r'^user/', include('UserAndPrj.urls')),
)

urlpatterns += patterns ('',
  url(r'^assist/', include('Assist.urls')),
)

urlpatterns += patterns ('',
  url(r'^xadmin/', include('Admin.urls')),
)

urlpatterns += patterns ('',
  url(r'^business/', include('Business.urls')),
)

urlpatterns += patterns ('',
  url(r'^spacemanager/', include('SpaceManager.urls')),
)

urlpatterns += patterns ('',
  url(r'^vehiclemanager/', include('VehicleManager.urls')),
)

urlpatterns += patterns ('',
  url(r'^config/', include('UserPrjConfig.urls')),
)

urlpatterns += patterns('',
         url(r'dist_vue/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'dist_vue/','show_indexes': True}),
         url(r'rest_framework/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'rest_framework/','show_indexes': True}),
        url(r'admin/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'admin/','show_indexes': True}),
            url(r'js/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'js/','show_indexes': True}),
            url(r'css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT+'css/','show_indexes': True }),
            url(r'images/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'images/','show_indexes': True}),
            url(r'textures/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'textures/','show_indexes': True}),
            url(r'img/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'img/','show_indexes': True}),
            url(r'font/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'font/','show_indexes': True}),
            url(r'model/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT+'model/','show_indexes': True}),
            url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,'show_indexes': True}),
)


handler404 = error_404
handler500 = error_500
