# -*- coding: utf-8 -*-

import os,time,random, sys, datetime, calendar, traceback
import memcache
import urllib2,json
from Scc4PM import settings
from TaskAndFlow.models import *
from django.db.models import Q
from uuid import uuid1
from Scc4PM.settings import DATABASES
from TaskAndFlow.utility import *

def GetTaskCompAndStyle(curtask):
    completion = 0
    style = 'gtaskpink'

    curdate = datetime.datetime.now()
    #if curtask.percentage and curtask.percentage!=0:
    completion = curtask.percentage
    if completion==100:
        style = 'gtaskgreen'
    elif completion==0:
        if ProjectTask.objects.filter(Q(taskpath__contains=str(curtask.id)+"/")&Q(actualstart__isnull=False)).count()>0:
            style = 'gtaskblue'    
        else:
            style = 'gtaskpink'
    else:
        style = 'gtaskblue'    
    if curdate > curtask.planfinish:
        if(completion!=100):
            style = 'gtaskred' if 0 == completion and not curtask.actualstart else 'gtaskyellow' 
    # else:
    #     childtasklist = ProjectTask.objects.filter(Q(taskpath__contains=str(curtask.id)+"/")|Q(id=curtask.id)).values_list('id',flat=True)
    #     totaltaskpblist = PrecastBeam.objects.filter(task_id__in = childtasklist)

    #     totaltaskpb = len(totaltaskpblist)
        
    #     if totaltaskpb > 0:
    #         donetaskpb = totaltaskpblist.filter(curstatus__isnull=False,curstatus__nextstatus__isnull=True).count()
    #         doingtaskpb = totaltaskpblist.filter(curstatus__isnull=False,curstatus__nextstatus__isnull=False).count()
    #         completion = float( '%.2f' % ((donetaskpb*100.0)/totaltaskpb))
    #         if donetaskpb==totaltaskpb:
    #             style = 'gtaskgreen'
    #         elif donetaskpb==0 and doingtaskpb==0:
    #             style = 'gtaskpink'
    #         else:
    #             style = 'gtaskblue'
        
    #         curdate = datetime.datetime.now()
    #         if curdate > curtask.planfinish:
    #             if(donetaskpb!=totaltaskpb):
    #                 style = 'gtaskred' if 0 == donetaskpb and 0==doingtaskpb  else 'gtaskyellow'
    #     else:
    #         completion=0
    #         style = 'gtaskpink'
    #         if curdate > curtask.planfinish:
    #             style = 'gtaskred'
            
    return completion,style

def calcProjectTaskProgressInfo(MajorId=None):
    response_data = {}
    response_data["projecttasklist"]=[]

    list_items = ProjectTask.objects.all()
       
    if MajorId and MajorId!="0":
        list_items = list_items.filter(major_id=int(MajorId))
    
    for each in list_items:
        tmpObj = {}
        tmpObj["pID"] = each.id
        tmpObj["pName"] = each.name
        tmpObj["pStart"] = each.planstart.strftime("%Y-%m-%d")
        tmpObj["pEnd"] = each.planfinish.strftime("%Y-%m-%d")
        #tmpObj["pLink"] = ""
        #tmpObj["pMile"] = each.ismilestone
        #tmpObj["pRes"] = ""
        completion,style = GetTaskCompAndStyle(each)
        tmpObj["pStyle"] = style
        tmpObj["pComp"] = completion
        tmpObj["pGroup"] = 1 if ProjectTask.objects.filter(parentid=each).count()>0 else 0
        tmpObj["pParent"] =  each.parentid_id if each.parentid_id else ""
        tmpObj["pOpen"] = 0 if each.parentid else 1
        #tmpObj["pDepend"] = ""
        #tmpObj["pCaption"] = each.description
        #tmpObj["pNotes"] = ""
        tmpObj["pGantt"] = "g"
    
        response_data["projecttasklist"].append(tmpObj)
    
    response_data["issuc"]="true"

    jsonprogress = json.dumps(response_data)

    mc=memcache.Client(['127.0.0.1:11211'],debug=0)

    keyname = DATABASES['pms']['NAME']+"_pm_projecttask_progress"
    mc.set(keyname,jsonprogress,2000)

    return jsonprogress

def getProjectTaskProgressInfo():
     mc=memcache.Client(['127.0.0.1:11211'],debug=0)
     keyname = DATABASES['pms']['NAME']+"_pm_projecttask_progress"
     jsonprogress=mc.get(keyname)

     return jsonprogress


def getWeeklyDate(weekly=None):
    if weekly:
        weekly_enddate = weekly.weekly_date
        weekly_begindate = weekly.weekly_date+ datetime.timedelta(-6)
    else:
        weekday=0
        try:
             weekday=int(CustomInfo.objects.get(infotype="weekly_index").custominfo)
        except:
            pass
        weekly_enddate = getweekdayofdate(datetime.date.today()+ datetime.timedelta(0-weekday+1),weekday-1)
        weekly_begindate = getweekdayofdate(datetime.date.today()+ datetime.timedelta(0-weekday+1),weekday-7)

    return weekly_begindate,weekly_enddate

def getCurWeekly(user):
    weekly_begindate,weekly_enddate = getWeeklyDate()

    weekly = Weekly.objects.filter(weekly_date=weekly_enddate)
    if weekly:
        weekly = weekly[0]
    else:
        weeklyname = u"工程周汇报("+weekly_begindate.strftime("%Y.%m.%d")+"-"+weekly_enddate.strftime("%Y.%m.%d")+")"
        weekly = Weekly.objects.create(weekly_date=weekly_enddate,update_time=datetime.datetime.now(),
                                        name=weeklyname,user=user,content='{}')

    return weekly

def getWeeklyDir():
    savedir = Directory.objects.get(name="工程周报",islock=True)
    weekly_begindate,weekly_enddate = getWeeklyDate()
    weekdirname = weekly_enddate.strftime("%Y%m%d")
    if Directory.objects.filter(name=weekdirname,islock=True).count()==0:
        weeklydir = Directory.objects.create(name=weekdirname,parent=savedir,creator_id=1,islock=True)
    else:
        weeklydir = Directory.objects.get(name=weekdirname,islock=True)
    return weeklydir