from django.conf.urls import patterns, include, url
from Business.views import *

from rest_framework import routers, serializers, viewsets


urlpatterns = patterns('',
    url(r'^spacefeilv/$',spacefeilv),
    url(r'^spacemanager/$',spacemanager),
    url(r'^pacthandle/$',pacthandle),
    url(r'^test/$',test),
    url(r'^getpsrate_or_resource/$',getpsrate_or_resource),

    url(r'^analysis_rencaiji_execl/$',analysis_rencaiji_execl),
    url(r'^businessmanager/$',businessmanager),
    url(r'^initmanagerData/$',initmanagerData),

    url(r'^get_business_tree/$',get_business_tree),
    url(r'^addpact/$',addpact),
    url(r'^getBqitemBycode/$',getBqitemBycode),
    url(r'^updateDinge/$',updateDinge),
    url(r'^updateBqitemQuality/$',updateBqitemQuality),
    url(r'^rencaijiadd/$',rencaijiadd),
    url(r'^resourcehandle/$',resourcehandle),

    url(r'^fenbaopact/$',fenbaopact),
    url(r'^addfenpact/$',addfenpact),
    url(r'^delFenbaoitem/$',delFenbaoitem),
    url(r'^get_fenbaopact_tree/$',get_fenbaopact_tree),
    url(r'^getpactqingdanlist/$',getpactqingdanlist),

    url(r'^shigongyusuan/$',shigongyusuan),
    url(r'^get_budget_tree/$',get_budget_tree),
    url(r'^getbudgetComponentQuantities/$',getbudgetComponentQuantities),
    url(r'^addbudget_requirement/$',addbudget_requirement),
    url(r'^addbudget_construct/$',addbudget_construct),
    url(r'^addbudget_requirerow/$',addbudget_requirerow),
    url(r'^delcalcrelation/$',delcalcrelation),
    url(r'^deleteBudget/$',deleteBudget),

    url(r'^taskmanagerlist/$',taskmanagerlist),
    url(r'^get_task_tree/$',get_task_tree),
    url(r'^gettabletasks/$',gettabletasks),
    url(r'^getTaskorderByid/$',getTaskorderByid),
    url(r'^updateTaskorder/$',updateTaskorder),
    url(r'^delTaskorderByid/$',delTaskorderByid),
    url(r'^addTaskorder/$',addTaskorder),

    url(r'^chanzhilist/$',chanzhilist),
    url(r'^loadAccountList/$',loadAccountList),
    url(r'^getqingdancodeinfo/$',getqingdancodeinfo),
    url(r'^calculateReport/$',calculateReport),
    url(r'^updateReportBqitem/$',updateReportBqitem),
    url(r'^updateReportResitem/$',updateReportResitem),
    url(r'^delReport/$',delReport),
    url(r'^addReportBqitem/$',addReportBqitem),
    url(r'^delReportBqitem/$',delReportBqitem),
    url(r'^lockReport/$',lockReport),
    url(r'^addReportRes/$',addReportRes),
    url(r'^delReportRes/$',delReportRes),
    url(r'^addReportCost/$',addReportCost),
    url(r'^delReportCost/$',delReportCost),
    url(r'^get_report_tree/$',get_report_tree),
    url(r'^get_report_account_tree/$',get_report_account_tree),
    url(r'^getbqtablelist/$',getbqtablelist),
    url(r'^chanzhibaobiao/$',chanzhibaobiao),
    url(r'^chanzhioutandin/$',chanzhioutandin),

    url(r'^getScitemsBycompany/$',getScitemsBycompany),
    url(r'^getLaborpactsBycompany/$',getLaborpactsBycompany),
    url(r'^addSeparateCost/$',addSeparateCost),
    url(r'^getSciteminfo/$',getSciteminfo),
    url(r'^delSeparateCost/$',delSeparateCost),

    url(r'^autobudget/$',autobudget),
    url(r'^updateYusuanRule/$',updateYusuanRule),

    url(r'^ledgeraccount/$',ledgeraccount),
    url(r'^get_account_tree/$',get_account_tree),
    url(r'^get_hazard_tree/$',get_hazard_tree),
    url(r'^manageraccount/$',manageraccount),

    url(r'^otheritem_yusuan/$',otheritem_yusuan),
    url(r'^get_business_otheritem_tree/$',get_business_otheritem_tree),
    url(r'^costManager/$',costManager_vue)
)
