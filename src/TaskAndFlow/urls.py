# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from TaskAndFlow.views import *
from TaskAndFlow.views_goujian import *
from TaskAndFlow.views_flowtemplate import *
from TaskAndFlow.views_filemanager import *
from TaskAndFlow.views_taskmanager import *
from TaskAndFlow.views_meeting import *
from TaskAndFlow.views_hazard import *
from TaskAndFlow.serializers import *
from TaskAndFlow.views_xietiao import *

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'goujian/$', goujian_list),
                       url(r'goujian/group/$', goujian_group),
                       url(r'goujian/group/create/$', goujian_group_create),
                       url(r'goujian/group/edit/(?P<id>[^/]+)/$',goujian_group_edit),
                       url(r'goujian/group/delete/$', goujian_group_delete),
                       url(r'goujian/group/pbdelete/$', goujian_group_pbdelete),
                       url(r'goujian/pbgrp/$', goujian_pbgrp),
                       url(r'goujian/load/$', goujian_load),
                       url(r'goujian/qrcode/$', goujian_qrcode),
                       url(r'goujian/grpqrcode/$', goujian_grpqrcode),
                       url(r'goujian/trace/$', goujian_trace),
                       url(r'goujian/trace_front/$', goujian_trace_front),
                       url(r'goujian/tree/$', goujian_tree),
                       url(r'goujian/create/$', goujian_create),
                       url(r'goujian/read/$', goujian_read),
                       url(r'goujian/search/$', goujian_search),
                       url(r'goujian/update/$', goujian_update),
                       url(r'goujian/zhijian/$', goujian_zhijian),
                       url(r'goujian/update/zhijian/$',goujian_update_zhijian),
                       url(r'goujian/del/$', goujian_del),
                       url(r'goujian/updatepbstatus/$', updatepbstatus),
                       url(r'goujian/delpbstatus/$', delpbstatus),
                       url(r'goujian/setpbcustominfo/$', setpbcustominfo),
                       url(r'goujian/statusmanager/$', goujian_statusmanager),
                       url(r'goujian/glys/$', goujian_glys),#增加构件关联元素查找构件
                       url(r'goujian/glrw/$', goujian_glrw),#增加构件关联元素查找构件
                       url(r'goujian/glys_mobile/$', goujian_glys_mobile),
                       url(r'goujian/glys_pbtype/$', goujian_glys_pbtype),
                       url(r'goujian/get_glys_qrcode/$', get_glys_qrcode),
                       url(r'goujian/pbcountdesc/$', goujian_pbcountdesc),

                       url(r'getelebyqrcode/$', getelebyqrcode),
                       url(r'getelestatuslist/$', getelestatuslist),
                       url(r'getelestatuslisthis/$', getelestatuslisthis),

                       (r'pbstatusrecord/list/$', list_pbstatusrecord),

                       (r'modelview/$', modelview),
                       (r'modelview/getcounttypelist/$', getcounttypelist),
                       (r'modelview/getpblist/$', getpblist),
                       (r'modelview/getpbstatuslist/$', getpbstatuslist),
                       (r'modelview/getpbstatus/$', getpbstatus),
                       (r'modelview/getstatuslist/$', getstatuslist),
                       (r'modelview/getpbproperty/$', getpbproperty),
                       (r'modelview/getelevationtree/$', getelevationtree),
                       (r'modelview/renwutree/$', renwutree),

                       (r'modelview/getpbmajortree/$', getpbmajortree),
                       (r'modelview/getpbtypetree/$', getpbtypetree),
                       (r'modelview/gethazardtypetree/$', get_hazard_tree),
                       (r'modelview/gethazardeventtree/$', get_hazard_event_tree),
                       (r'modelview/getsheshitypetree/$', get_sheshi_tree),
                       (r'modelview/getjixietypetree/$', get_jixie_tree),
                       (r'modelview/getworktypetree/$', getworktypetree),
                       (r'modelview/filterPblist/$', filterPblist),
                       (r'modelview/getinitialmodel/$', getinitialmodel),
                       (r'modelview/getmodelfile/$', getmodelfile),
                       (r'modelview/setinitialmodel/$', setinitialmodel),
                       (r'modelview/getpblisttimerange/$', getpblisttimerange),
                       (r'modelview/filterPbByCountType/$', filterPbByCountType),
                       (r'modelview/getpblist2/$', getpblist2),
                       (r'modelview/getrelatefilelist/$', getrelatefilelist),

                       (r'flowtemplate/create/$', create_flowtemplate),
                       (r'flowtemplate/list/$', list_flowtemplate),
                       (r'flowtemplate/update/$', update_flowtemplate),
                       (r'flowtemplate/update/info/$',update_flowtemplate_info),
                       (r'flowtemplate/edit/(?P<id>[^/]+)/$',edit_flowtemplate),
                       (r'flowtemplate/view/(?P<id>[^/]+)/$',view_flowtemplate),
                       (r'flowtemplate/delete/$', delete_flowtemplate),

                       (r'flowtemplatestep/create/$', create_flowtemplatestep),
                       (r'flowtemplatestep/changename/$',changename_flowtemplatestep),
                       (r'flowtemplatestep/list/form$', list_flowtemplatestep_form),
                       (r'flowtemplatestep/update/(?P<id>[^/]+)/$',update_flowtemplatestep),
                       (r'flowtemplatestep/edit/(?P<id>[^/]+)/$',edit_flowtemplatestep),
                       (r'flowtemplatestep/get/(?P<id>[^/]+)/$',get_flowtemplatestep),
                       (r'flowtemplatestep/view/(?P<id>[^/]+)/$',view_flowtemplatestep),
                       (r'flowtemplatestep/delete/$', delete_flowtemplatestep),

                       url(r'acceptancetype/formtemplate/$', getacceptancetypeform),
                       url(r'acceptance/createacceptance/$', createacceptance),
                       url(r'acceptance/opt/(?P<id>[^/]+)$', optacceptance),
                       url(r'qualitycenter/$', qualitycenter),
                       url(r'qualitycenter/getpbstatuslist/$', qualitycenter_getpbstatuslist),

                       url(r'zhiliangyanshou/$', zhiliang_yanshou),
                       url(r'gongxuyanshou/$', gxyanshou),
                       url(r'zhiliangyanshou/guanjiandian/(?P<id>[^/]+)/$', guanjiandianyanshou),
                       url(r'zhiliangyanshou/yanshou/(?P<id>[^/]+)/$', newyanshou),
                       url(r'zhiliangyanshou/chakan/(?P<id>[^/]+)/$', chankan),
                       url(r'area_personnel/$', area_personnel),
                       url(r'Tracking_imformation/$', Tracking_imformation),
                       url(r'personnel_details/$', personnel_details),
                    
                       url(r'issue/createh$', issuecreate_html),
                       url(r'issue/createauto/$', issuecreate_auto),

                       url(r'issue/list/$', issue_list2),
                       url(r'issue/list/general/$', issue_list_forgeneral),
                       url(r'issue/createconfig/$', issue_createconfig),
                       url(r'issue/getrelatetype/$', getrelatetype),
                       url(r'issue/getmajortemplate/$', getmajortemplate),
                       url(r'issue/getissuetypetemplate/$',getissuetypetemplate),
                       url(r'issue/createissue/$', createissue),
                       url(r'issue/dealconfig/$', issue_dealconfig),
                       url(r'issue/issuedeal/(?P<id>[^/]+)/$', issuedeal),
                       url(r'issue/dealissue/$', dealissue),
                       url(r'issue/read/(?P<id>[^/]+)/$', issue_read),
                       url(r'issue/readfront/(?P<id>[^/]+)/$', issue_readfront),
                       url(r'issue/update/$',issue_update),
                       url(r'issue/del/$', zhiliang_del),
                       url(r'issue/issuelistcount/$', issuelistcount),
                       url(r'issue/shiyicreate/$', shiyicreate),
                       url(r'issue/issuecount/$', issue_count),
                       url(r'issue/issuetrace/$', issuetrace),
                       url(r'issue/getissuenumber/$', getissuenumber),
                       url(r'issue/qianzhengcreate/$', qianzhengcreate),
                       url(r'issue/qianzhenglist/$', qianzhenglist),

                       url(r'issue/gcjdksqcreate/$', gcjdksqcreate),
                       url(r'issue/gcjdksqlist/$', gcjdksqlist),

                      url(r'issue/sjbgtzcreate/$',sjbgtzcreate),
                       url(r'issue/sjbgtzlist/$', sjbgtzlist),

                      url(r'issue/bgsjbacreate/$', bgsjbacreate),
                       url(r'issue/bgsjbalist/$', bgsjbalist),

                        url(r'issue/tzhscreate/$', tzhscreate),
                       url(r'issue/tzhslist/$', tzhslist),

                        url(r'issue/bimshcreate/$', bimshcreate),
                       url(r'issue/bimshlist/$', bimshlist),


                       url(r'^progress/issue/edit/$', progress_problem_edit),
                       url(r'^progress/problem/$', progress_problem),
                       url(r'^progress/problem/loadTable/$', progress_problem_load_table),
                       url(r'^progress/problem/(?P<id>[^/]+)/$', progress_problem_trace),
                       url(r'^progress/problem/watch/(?P<id>[^/]+)/$', progress_problem_watch),
                       url(r'^progress/problem/(?P<id>[^/]+)/update/$', progress_problem_update),
                       
                       (r'projectevent/create/$', create_projectevent),

                       # url(r'huiyi/$', huiyi),

                       url(r'jishu/fangan/$', jishu_fangan),
                       url(r'jishu/fangan/(?P<id>[^/]+)/$', jishu_fanganopt),
                       url(r'jishu/jichu/$', jishu_jichu),
                       url(r'jishu/chengxu/$', jishu_chengxu),
                       url(r'jishu/jixuwenti/$', jishu_jixuwenti),
                       url(r'jishu/jianceshi/$', jishu_jianceshi),
                       url(r'jishu/guanbiao/$', jishu_guanbiao),

                       url(r'anquan/general/$', anquan_general),

                       url(r'anquan/jiancha/$', anquan_jiancha),
                       url(r'anquan/jianchadetail/$', anquan_jianchadetail),
                       url(r'anquan/jianchajiancha/$', anquan_jianchajiancha),
                       url(r'anquan/jiancha/read$', anquan_jiancharead),
                       url(r'anquan/jianchatrace/$', anquan_jianchatrace),
                       url(r'anquan/jiancha/getpbstatuslist/$', jiancha_getpbstatuslist),

                       url(r'anquan/biaodan/list/$', anquan_biaodan),
                       url(r'anquan/getpbstatuslist/$', anquan_getpbstatuslist),

                       url(r'anquan/jixie/general/$', jixie_general),
                       url(r'anquan/jixie/list/$', jixie_list),

                       url(r'anquan/hazard/general/$', hazard_general),
                       url(r'anquan/hazard/task/$', hazard_task),

                       url(r'anquan/hazard/list/$', hazard_list),

                       url(r'anquan/hazard/attachment/$', hazard_attachment),

                       url(r'anquan/sheshi/general/$', sheshi_general),
                       url(r'anquan/sheshi/list/$', sheshi_list),
                       url(r'anquan/hazard/$', hazardopt),#危险源



                       url(r'ziliao/$', ziliao_list),
                       url(r'ziliao/connector/$', connector_view),
                       url(r'ziliao/connector_upload/$',connector_view_upload),
                       url(r'ziliao/uploadview/$', ziliao_uploadview),
                       url(r'ziliao/cloudfilerelate/$',ziliao_cloudfilerelate),
                       url(r'ziliao/getfiletree/$', ziliao_getfiletree),
                       url(r'ziliao/getdirtree/$', ziliao_getdirtree),
                       url(r'ziliao/anquanjiancha/$', ziliao_anquanjiancha),
                       url(r'ziliao/checkexist/$', ziliao_checkexist),
                       url(r'ziliao/filehisversion/$', ziliao_filehisverison),
                       url(r'ziliao/dirdownload/$', ziliao_dirdownload),
                       url(r'ziliao/filemanager_mobile/$', ziliao_filemanager_mobile),
                       url(r'ziliao/fileproperty/$', ziliao_fileproperty),
                       url(r'ziliao/editproperty/$', ziliao_editproperty),
                       url(r'ziliao/previewfile/$', ziliao_previewfile),
                     


                       (r'projecttask/manager/$', manager_projecttask),
                       (r'projecttask/getprojecttasklist/$',getprojecttasklist),
                       (r'projecttask/getprjversiionlist/$',getprjversiionlist),
                       (r'projecttask/gethisprojecttasklist/$',gethisprojecttasklist),
                       (r'projecttask/qrcode/$', projecttask_qrcode),
                       (r'projecttask/create/$', create_projecttask),
                       (r'projecttask/gettask/$', get_projecttask),
                       (r'projecttask/edit/$', edit_projecttask),
                       (r'projecttask/deltask/$', del_projecttask),
                       (r'projecttask/trace/$', trace_projecttask),
                       (r'projecttask/status/$', status_projecttask),
                       (r'projecttask/getstatus/$', getstatus_projecttask),
                       (r'projecttask/getstatusgoal/$',getstatusgoal_projecttask),
                       (r'projecttask/getunitprojectlist/$', getunitprojectlist),
                       (r'projecttask/list/$', list_projecttask),
                       (r'projecttask/query/$', query_projecttask),
                       (r'projecttask/view/(?P<id>[^/]+)/$', view_projecttask),
                       (r'projecttask/statusbim/$', projecttask_statusbim),
                       (r'projecttask/monthplan/$', projecttask_monthplan),
                       (r'projecttask/savemonthplan/$', monthplan_save),
                       
                       (r'projecttask/builddiary/$', projecttask_builddiary),
                       (r'projecttask/buildweekly/$', projecttask_weekly),
                       (r'projecttask/buildweekly2/$', projecttask_weekly2),
                       (r'projecttask/buildweekly2_list/$', projecttask_weekly2_list),
                       (r'projecttask/buildweekly2_data/$', projecttask_weekly2_data),
                       (r'projecttask/buildweekly2_item/$', projecttask_weekly2_item),
                       (r'projecttask/buildweekly2_read/$', projecttask_weekly2_read),
                       (r'projecttask/buildgoal/$', projecttask_buildgoal),
                        (r'projecttask/buildgoalmgr/$', projecttask_buildgoalmgr),
                       (r'projecttask/savebuildgoal/$', projecttask_savebuildgoal),
                       (r'projecttask/deletebuildgoal/$', projecttask_deletebuildgoal),
                        (r'projecttask/getgoalstatus/$', getgoalstatus_projecttask),
                        (r'projecttask/getgoalproperty/$', getgoalproperty_projecttask),

                       (r'projecttask/updatetaskplan/$', projecttask_updatetaskplan),
                       (r'projecttask/lurujindu/$', projecttask_lurujindu),
                       url(r'^projecttask/count/$', projecttask_count),

                       url(r'cailiao/$', cailiao_list),
                       url(r'cailiao/create/$', cailiao_create),
                       url(r'cailiao/read/$', cailiao_read),
                       url(r'cailiao/update/$', cailiao_update),
                       url(r'cailiao/del/$', cailiao_del),


                       (r'notice/create/$', create_notice),
                       (r'notice/list/$', list_notice),
                       (r'notice/delete/$', delete_notice),
                       (r'notice/edit/$', edit_notice),



                      (r'factoryarea/create/$', create_factoryarea),
                      (r'factoryarea/list/$', list_factoryarea ),
                      (r'factoryarea/edit/(?P<id>[^/]+)/$', edit_factoryarea),
                      (r'factoryarea/view/(?P<id>[^/]+)/$', view_factoryarea),
                      (r'factoryarea/pblist/$', factoryarea_pblist),
                      (r'factoryarea/pblist/search/$', factoryarea_search),

                      (r'typemanager/$', typemanager),
                      
)
