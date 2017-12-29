# -*- coding: utf-8 -*-

from TaskAndFlow.models import *
import datetime


def pbtype_timecheck():
    checklist = Pbtypetimedcheck.objects.all()
    for item in checklist:
        if item.task_cycle_type=="每天":
            createdaycheck(item)
        elif item.task_cycle_type=="每周":
            createweekcheck(item)
        elif item.task_cycle_type=="每月":
            createmonthcheck(item)

def createdaycheck(checkObj):
    createcheck(checkObj)

def createweekcheck(checkObj):
    now = datetime.datetime.now()
    nowweekday = now.isoweekday()
    nowweekdaystr = ''
    if nowweekday==1:
        nowweekdaystr = u'星期一'
    elif nowweekday==2:
        nowweekdaystr = u'星期二'
    elif nowweekday==3:
        nowweekdaystr = u'星期三'
    elif nowweekday==4:
        nowweekdaystr = u'星期四'
    elif nowweekday==5:
        nowweekdaystr = u'星期五'
    elif nowweekday==6:
        nowweekdaystr = u'星期六'
    elif nowweekday==7:
        nowweekdaystr = u'星期日'
    if nowweekdaystr in checkObj.task_cycle:
        createcheck(checkObj)

def createmonthcheck(checkObj):
    now = datetime.datetime.now()
    nowday = now.day
    if nowday<10 :
        nowday = '0'+str(nowday)
    if str(nowday) in checkObj.task_cycle:
        createcheck(checkObj)

def createcheck(checkObj):
    curdate = datetime.datetime.now()
    checkObj.status_reset_time = curdate
    checkObj.isneedcheck = True
    checkObj.save()

    if checkObj.pbtype:
        pblist = PrecastBeam.objects.filter(pbtype=checkObj.pbtype).values_list('id',flat=True)
        elelist = Monitoringelement.objects.filter(typetable="构件",relatedid__in=pblist)
    # else:
    #     grplist = Pbgroup.objects.filter(pbtype=checkObj.pbtype).values_list('id',flat=True)
    #     elelist = Monitoringelement.objects.filter(typetable="构件组",relatedid__in=grplist)

    record_list_to_insert = list()
    for ele in elelist:
        record_list_to_insert.append(PbtimedcheckRecord(timedcheck=checkObj, monitoring=ele,status_reset_time=curdate))
    PbtimedcheckRecord.objects.bulk_create(record_list_to_insert)
    
