# -*- coding: utf-8 -*-
#import logging
#logging.basicConfig(filename='/www/log/myapp.log',filemode='w')
import os,time,random, sys, datetime, calendar, traceback
import memcache
import urllib2,json
from Scc4PM import settings
from TaskAndFlow.models import *
from django.db.models import Q
from Scc4PM.settings import CURRENT_PROJECT_ID
from Assist.utility import *
from django.db.models import F
import datetime
import time

def getEventNumber(issuetype):
    bianhao=None
    if issuetype==u'质量问题':
        bianhao = "ZL-"
    elif issuetype==u'安全问题':
        bianhao = "AQ-"
    elif issuetype==u'协调事宜':
        bianhao = "XT-"
    elif issuetype==u'现场签证':
        bianhao = "XCQZ-"
    elif issuetype==u'工程进度款申请':
        bianhao = "JDKSQ-"
    elif issuetype==u'设计变更通知':
        bianhao = "SJBGTZ-"
    elif issuetype==u'变更设计备案':
        bianhao = "BGSJBA-"
    elif issuetype==u'图纸会审':
        bianhao = "TZHS-"
    elif issuetype==u'BIM深化':
        bianhao = "BIMSH-"
    else:
        bianhao = "SJ-"

    bianhao+=datetime.datetime.strftime(datetime.datetime.now(),"%y%m%d%H%M-")

    latestId = 1
    try:
        latestId = projectevent.objects.latest("id").id
    except:
        latestId = 1

    bianhao = bianhao + str(latestId)

    return bianhao

def transIssueType(inIssuetype):
    issuetype = u'质量问题'
    if inIssuetype=="zhiliang":
        issuetype = u'质量问题'
    elif inIssuetype=="anquan":
        issuetype = u'安全问题'
    elif inIssuetype=="xietiao":
        issuetype = u'协调事宜'
    elif inIssuetype=="xianchangqianzheng":
        issuetype = u'现场签证'
    elif inIssuetype=="gcjdksq":
        issuetype = u'工程进度款申请'
    elif inIssuetype=="sjbgtz":
        issuetype = u'设计变更通知'
    elif inIssuetype=="bgsjba":
        issuetype = u'变更设计备案'
    elif inIssuetype=="tzhs":
        issuetype = u'图纸会审'
    elif inIssuetype=="bimsh":
        issuetype = u'BIM深化'
    else:  
        pass
    return issuetype

def getDealNeedFile(each):
    needfile = True
    if FlowTemplateStep.objects.filter(template=each.template,sequence=each.curflowstep.sequence+1):
        needfile = not FlowTemplateStep.objects.filter(template=each.template,sequence=each.curflowstep.sequence+1)[0].isendstep

    if each.template.flowtype.name in ['现场签证','工程进度款申请','设计变更通知','变更设计备案','图纸会审','BIM深化']:
        needfile = False

    return needfile

def isFlowTypeXiaoTiao(flowtype):
    isFlowTypeXiaoTiao = False

    if flowtype in ['现场签证','工程进度款申请','设计变更通知','变更设计备案','图纸会审','BIM深化']:
        isFlowTypeXiaoTiao = True

    return isFlowTypeXiaoTiao

def checkEventRight(user,flowstepid):
    if FlowStepUser.objects.filter(user=user, flowstep_id=flowstepid, isactor=1):  
        return True
    elif FlowStepUser.objects.filter(flowstep_id=flowstepid):
        return False
    else:
        return True


def addNewEventMessage(newEvent,user,curstep,curopr,feedback):
    try:
        if newEvent.issave==False:
            actorlist = FlowStepUser.objects.filter(flowstep_id = newEvent.curflowstep_id,isactor=True)
            watchlist = FlowStepUser.objects.filter(flowstep_id = newEvent.curflowstep_id,isactor=False)
 
            if user.userdivisions.all():
                fromname = user.userdivisions.all()[0].division.name
            else:
                fromname = user.company.name

            if curopr:
                title = ("%s%s%s") % (fromname,curopr.name,newEvent.number)
                newMsg = curopr.name+newEvent.number +"("+( feedback if len(feedback)<20 else feedback[:20]+"...")+")"
            else:
                title = ("%s%s%s") % (fromname,curstep.name,newEvent.number)
                newMsg = curstep.name+newEvent.number+"("+( feedback if len(feedback)<20 else feedback[:20]+"...")+")"
            for each in actorlist:
                PushMessage.objects.create(status=0,title=title, relatetype="事件", relateid=newEvent.id,
                                        agentid= Project.objects.get(id=CURRENT_PROJECT_ID).appid,
                                        fromuser=user, touser=each.user, message=newMsg)
            for each in watchlist:
                PushMessage.objects.create(status=0,title=title, relatetype="事件查看", relateid=newEvent.id,
                                        agentid= Project.objects.get(id=CURRENT_PROJECT_ID).appid,
                                        fromuser=user, touser=each.user, message=newMsg)   
    except:
        traceback.print_exc()
    return


def checkStepTimeOut(stepobj,proobj):
    return False
    
def getEventStep(proeventObj):
    if Eventstep.objects.filter(flowstep=proeventObj.curflowstep, projectevent=proeventObj,endtime=None):
        return Eventstep.objects.get(flowstep=proeventObj.curflowstep, projectevent=proeventObj,endtime=None)
    else:
        newEventStep = Eventstep.objects.create(flowstep=proeventObj.curflowstep, projectevent=proeventObj)
        return newEventStep

def getstepNextState(proeventObj):
    if FlowTemplateStep.objects.filter(template=proeventObj.template,sequence=proeventObj.curflowstep.sequence+1):
        return FlowTemplateStep.objects.get(template=proeventObj.template,sequence=proeventObj.curflowstep.sequence+1)
    else:
        return proeventObj.curflowstep
    
def updateEventStepOper(user, flowstepid, proeventObj, FlowStepOperaObj,feedback):
    eventStep=getEventStep(proeventObj)
    if not EventStepOperation.objects.filter(actor=user, eventstep=eventStep,flowstepoper=FlowStepOperaObj):
        newOpera=EventStepOperation.objects.create(actor=user, eventstep=eventStep, flowstepoper=FlowStepOperaObj , comment=feedback)
    else:
        newOpera=EventStepOperation.objects.filter(actor=user, eventstep=eventStep,flowstepoper=FlowStepOperaObj)[0]
    
    updateEventStatus(proeventObj, newOpera)

    curStep=FlowTemplateStep.objects.get(id=flowstepid)
    addNewEventMessage(proeventObj, user, curStep, FlowStepOperaObj,feedback)

    if proeventObj.curflowstep.isendstep:
        proeventObj.curdealstep = 3
    elif curStep.isstartstep:
        proeventObj.curdealstep = 1
    else:
        proeventObj.curdealstep = 2
    proeventObj.updatetime = datetime.datetime.now()
    proeventObj.save()
    return newOpera


def updateEventStatus(proeventObj, newOpera):
    eventStepNextState = newOpera.eventstep.flowstep
    eventStep=Eventstep.objects.get(flowstep=proeventObj.curflowstep,projectevent=proeventObj,endtime=None )
    #if proeventObj.curflowstep.isautotransfer:
    if proeventObj.curflowstep.istimeouttransfer and checkStepTimeOut(eventStep, proeventObj):
        eventStepNextState = getstepNextState(proeventObj)
    else:
        if newOpera.flowstepoper:
            if newOpera.flowstepoper.actortype.name == "任一":
                eventStepNextState = newOpera.flowstepoper.nextflowstep
                
            elif newOpera.flowstepoper.actortype.name == "超过一半" :
                totalU = FlowStepUser.objects.filter(flowstep=proeventObj.curflowstep, isactor=1).count()
                doneU = EventStepOperation.objects.filter(eventstep=eventStep).values("actor").distinct().count()
                
                if doneU >= totalU or (doneU+0.0)/totalU > 0.5:
                    eventStepNextState = newOpera.flowstepoper.nextflowstep
                
            elif newOpera.flowstepoper.actortype.name == "所有" :
                totalU = FlowStepUser.objects.filter(flowstep=proeventObj.curflowstep, isactor=1).count()
                doneU = EventStepOperation.objects.filter(eventstep=eventStep).values("actor").distinct().count()
                if doneU >= totalU :
                    eventStepNextState = newOpera.flowstepoper.nextflowstep
        else:
            eventStepNextState = getstepNextState(proeventObj)
    
    if eventStepNextState != proeventObj.curflowstep:
        proeventObj.curflowstep = eventStepNextState
        proeventObj.save()
        eventStep.endtime=datetime.datetime.now()  
        eventStep.save()

    return True


def getEventCreateDesc(event):
    try:
        return event.describe
    except:
        return ""

def getEventCreateUser(event):
    try:
        return event.createuser.truename
    except:
        return ""

def getEventCreateDate(event):
    try:
        return event.createtime.strftime("%Y年%m月%d日")
    except:
        return ""

def getEventCreateUserCmp(event):
    try:
        return event.createuser.company.name
    except:
        return ""

def getEventDealDesc(event):
    try:
        desc = ""
        dealEventstep = Eventstep.objects.filter(projectevent=event,flowstep__sequence=1,flowstep__isendstep=False).order_by('-endtime')[0]
        for opr in EventStepOperation.objects.filter(eventstep=dealEventstep):
            desc = desc + opr.comment + ";"
        if len(desc)>0:
            desc=desc[:-1]
        return desc
    except:
        return ""

def getEventDealUser(event):
    try:
        desc = ""
        dealEventstep = Eventstep.objects.filter(projectevent=event,flowstep__sequence=1,flowstep__isendstep=False).order_by('-endtime')[0]
        for opr in EventStepOperation.objects.filter(eventstep=dealEventstep):
            desc = desc + opr.actor.truename + ","
        if len(desc)>0:
            desc=desc[:-1]
        return desc
    except:
        return ""

def getEventDealDate(event):
    try:
        dealEventstep = Eventstep.objects.filter(projectevent=event,flowstep__sequence=1,flowstep__isendstep=False).order_by('-endtime')[0]
        return dealEventstep.endtime.strftime("%Y年%m月%d日")
    except:
        return ""

def getEventCloseDesc(event):
    try:
        desc = ""
        dealEventstep = Eventstep.objects.filter(projectevent=event,flowstep__sequence=2,flowstep__isendstep=False).order_by('-endtime')[0]
        for opr in EventStepOperation.objects.filter(eventstep=dealEventstep):
            desc = desc + opr.comment + ";"
        if len(desc)>0:
            desc=desc[:-1]
        return desc
    except:
        return ""

def getEventCloseUser(event):
    try:
        desc = ""
        dealEventstep = Eventstep.objects.filter(projectevent=event,flowstep__sequence=2,flowstep__isendstep=False).order_by('-endtime')[0]
        for opr in EventStepOperation.objects.filter(eventstep=dealEventstep):
            desc = desc + opr.actor.truename + ","
        if len(desc)>0:
            desc=desc[:-1]
        return desc
    except:
        return ""

def getEventCloseDate(event):
    try:
        dealEventstep = Eventstep.objects.filter(projectevent=event,flowstep__sequence=2,flowstep__isendstep=False).order_by('-endtime')[0]
        return dealEventstep.endtime.strftime("%Y年%m月%d日")
    except:
        return ""

def getEventDeadLine(event):
    try:
        return event.deadline.strftime("%Y年%m月%d日")
    except:
        return ""

def getEventProperty(event):
    try:
        return event.get_priority_desc(event.priority)
    except:
        return ""

def archiveEventDoc(proeventObj):
    #归档表单 潘古兵
    event = proeventObj
    curEventsteplist = Eventstep.objects.filter(projectevent=proeventObj,relatedform__isnull=False)
    if curEventsteplist:
        for EventStepObj in curEventsteplist:
            if EventStepObj.relatedform:
                content = EventStepObj.relatedform.content
                for each in Formtempandformtag.objects.filter(formtemplet_id=EventStepObj.relatedform.formtemplet_id):
                    try:
                        content = content.replace("{{"+each.formtag.tagname+"}}",eval(each.formtag.tag))
                    except:
                        traceback.print_exc()
                EventStepObj.relatedform.content = content
                EventStepObj.relatedform.save()
    else:
        flowsteplist = FlowTemplateStep.objects.filter(template=proeventObj.template)
        for stepObj in flowsteplist:
            if stepObj.relatedformtemplate:
                bda = stepObj.relatedformtemplate

                content = bda.content
                for each in Formtempandformtag.objects.filter(formtemplet_id=bda.id):
                    try:
                        content = content.replace("{{"+each.formtag.tagname+"}}",eval(each.formtag.tag))
                    except:
                        traceback.print_exc()
                form = BiaoDan.objects.create(name=bda.name,content=content,creater=proeventObj.createuser,createdate=proeventObj.createtime,
                                major=bda.major,formtype=bda.formtype,formtemplet=bda)
                Eventstep.objects.filter(projectevent=proeventObj,flowstep=stepObj).update(relatedform=form)

    retCode,acdir=Form2FileEvent(proeventObj)

def checkEventNeedDeal(each,user):
    needdeal = False
    if each.curflowstep.isendstep:
        needdeal = False
    else:
        needdeal = False
        if FlowStepUser.objects.filter(Q(flowstep=each.curflowstep) & Q(isactor=True)).count() == 0:
            needdeal = True
        else:
            if FlowStepUser.objects.filter(Q(flowstep=each.curflowstep) & Q(user=user) & Q(isactor=True)).count() > 0:
                if Eventstep.objects.filter(Q(projectevent=each.id) & Q(flowstep=each.curflowstep) & Q(endtime__isnull=True)).count() > 0:
                    curEventstep = Eventstep.objects.filter(Q(projectevent=each.id) & Q(flowstep=each.curflowstep) & Q(endtime__isnull=True))
                    if len(curEventstep)>0:
                        print "111111111111111111111111"
                        curEventstep = curEventstep[0]
                    curEventStepOperation = EventStepOperation.objects.filter( Q(eventstep=curEventstep) & Q(actor=user)).count()
                    needdeal = False if curEventStepOperation > 0 else True
                else:
                    needdeal = True
    return needdeal

def checkEventNeedWatch(each,user):
    needwatch = False
    if each.curflowstep.isendstep:
        needwatch = False
    elif FlowTemplateUser.objects.filter(user=user,template=each.template):
        needwatch = True
    else:
        needwatch = False
        if FlowStepUser.objects.filter(Q(flowstep=each.curflowstep)).count() == 0:
            needwatch = True
        else:
            if FlowStepUser.objects.filter(Q(flowstep=each.curflowstep) & Q(user=user)).count() > 0:
                needwatch = True
            else:
                needwatch = False
    return needwatch

def GetJianDuanFromStep(event):
    jianduan={}
    if event.issave:
        jianduan["jianduan"]=u"待编辑"
        jianduan["color"]="#96A2DA"
    elif event.curdealstep==3:
        jianduan["jianduan"]=u"已结束"
        jianduan["color"]="#008040"
    elif event.curdealstep==1:
        jianduan["jianduan"]=u"未处理"
        jianduan["color"]="#DE0404"
    else:
        jianduan["jianduan"]=u"处理中"
        jianduan["color"]="#fa800a"
    return jianduan

def GetJianDuanFromStep2(event):
    jianduan={}
    if event.issave:
        jianduan["jianduan"]=u"待编辑"
        jianduan["color"]="project-index-bg-blue"
    elif event.curdealstep==3:
        jianduan["jianduan"]=u"已结束"
        jianduan["color"]="project-index-bg-green"
    elif event.curdealstep==1:
        jianduan["jianduan"]=u"未处理"
        jianduan["color"]="project-index-bg-gray "
    else:
        jianduan["jianduan"]=u"处理中"
        jianduan["color"]="project-index-bg-yellow"
    return jianduan 

def GetPriorityStyle(event):
    style={}
    if event.priority==1:
        style["text"]="轻微"
        style["class"]="fa-arrow-down text-success"
    elif event.priority==5:
        style["text"]="一般"
        style["class"]="fa-arrow-up text-warning"
    else:
        style["text"]="严重"
        style["class"]="fa-arrow-up text-danger"
    return style      

def relatedDocWithEventOpr(user,docId,OprId,dirName):
    Doc2Relate.objects.create(relatetype='事件步骤操作', relateid=OprId,creator=user, document_id=docId, createtime=datetime.datetime.now())



def getUserIssueList(user,issuetype):
    list_items = projectevent.objects.filter(template__flowtype__name=issuetype,curflowstep__isendstep=False).order_by("deadline")
    issuelist = []
    for each in list_items:
        if each.issave:
                continue

        # 当前用户没有权限 且之前操作步骤指派人没有我
        eventoprlist = EventStepOperation.objects.filter(Q(eventstep__projectevent=each.id)).order_by("-oprtime")
        if not checkEventRight(user, each.curflowstep.id) and \
            eventoprlist.filter(Q(actor=user)).count() == 0:
            if not checkEventNeedWatch(each, user):
                continue

        issue = {}
        issue["issueId"] = each.id
        issue["number"] = each.number
        issue["describe"] = each.describe
        issue["dangqianjieduan"] = GetJianDuanFromStep(each)
        issuelist.append(issue)
    return issuelist



def filterPbListRequest(request):
    list_items = PrecastBeam.objects.filter(lvmdbid__isnull=False)
    selElevations = request.GET.get('_selElevations', '')
    if len(selElevations)>0:
        ElevationIds = []
        for ElevationId in selElevations[:-1].split(","):
            ElevationIds.append(int(ElevationId))
        list_items=list_items.filter(elevation__in=ElevationIds)
    
    selPbtypes = request.GET.get('_selPbtypes', '')
    if len(selPbtypes)>0:
        PbtypesIds = []
        for PbtypesId in selPbtypes[:-1].split(","):
            PbtypesIds.append(int(PbtypesId))
        list_items=list_items.filter(pbtype__in=PbtypesIds)
    
    _selZones = request.GET.get('_selZones', '')
    if len(_selZones)>0:
        selPbZones = []
        for ZoneId in _selZones[:-1].split(","):
            selPbZones.append(int(ZoneId))
        list_items=list_items.filter(zone__in=selPbZones)
    

    curUnitId = request.GET.get('_curUnitId', '')
    list_items=list_items.filter(elevation__unitproject=curUnitId)

    _curMajor = request.GET.get('_curMajor', '')
    list_items=list_items.filter(pbtype__major=_curMajor)

    return list_items

def filterPbGrpListRequest(request):
    zonelist = ZoneElevation.objects.all()
    selElevations = request.GET.get('_selElevations', '')
    if len(selElevations)>0:
        ElevationIds = []
        for ElevationId in selElevations[:-1].split(","):
            ElevationIds.append(int(ElevationId))
        zonelist=zonelist.filter(elevation__in=ElevationIds)

    curUnitId = request.GET.get('_curUnitId', '')
    zonelist=zonelist.filter(elevation__unitproject=curUnitId)

    _curMajor = request.GET.get('_curMajor', '')
    zonelist=zonelist.filter(zone__major=_curMajor)

    _selZones = request.GET.get('_selZones', '')
    if len(_selZones)>0:
        selPbZones = []
        for ZoneId in _selZones[:-1].split(","):
            selPbZones.append(int(ZoneId))
        print selPbZones
        zonelist=zonelist.filter(zone__in=selPbZones)


    zonelist=[each.zone.id for each in zonelist]
    print zonelist

    list_items = Pbgroup.objects.filter(zone_id__in=zonelist)
    selPbtypes = request.GET.get('_selPbtypes', '')
    if len(selPbtypes)>0:
        PbtypesIds = []
        for PbtypesId in selPbtypes[:-1].split(","):
            PbtypesIds.append(int(PbtypesId))
        list_items=list_items.filter(pbtype__in=PbtypesIds)
    

    return list_items

def getRijiMsg(rijidate,issuetype):
    msg = ""
    if not rijidate:
        rijidate=str(datetime.date.today())
    startdate=datetime.datetime.strptime(rijidate+" 00:00:00",'%Y-%m-%d %H:%M:%S')
    enddate=datetime.datetime.strptime(rijidate+" 23:59:59",'%Y-%m-%d %H:%M:%S')

    msg = ""

    list_items = projectevent.objects.filter(template__flowtype__name=issuetype,createtime__range=(startdate,enddate))
    if len(list_items)>0:
        msgfaqi="发起了"
        for each in list_items:
            msgfaqi+=each.number+"、"
        msgfaqi=msgfaqi[:-1]+"问题"
        msg+=msgfaqi

    list_items = projectevent.objects.filter(template__flowtype__name=issuetype,updatetime__range=(startdate,enddate),
                                            updatetime__gt=F('createtime') + datetime.timedelta(seconds=3),curflowstep__isendstep=False)
    if len(list_items)>0:
        msgfaqi="处理了"
        for each in list_items:
            msgfaqi+=each.number+"、"
        msgfaqi=msgfaqi[:-1]+"问题"
        if len(msg)>0:
            msg+=","
        msg+=msgfaqi

    list_items = projectevent.objects.filter(template__flowtype__name=issuetype,updatetime__range=(startdate,enddate),curflowstep__isendstep=True)
    if len(list_items)>0:
        msgfaqi="关闭了"
        for each in list_items:
            msgfaqi+=each.number+"、"
        msgfaqi=msgfaqi[:-1]+"问题"
        if len(msg)>0:
            msg+=","
        msg+=msgfaqi

    return msg


def getIssuePblist(issuetype,issueId,response_data,request,list_items_issue,iswholemodel):
    issuelist = []
    issuetype = transIssueType(issuetype)
    issuelist=getUserIssueList(request.user,issuetype)
    if issueId:
        tmplist = []
        for each in issuelist:
            if each["issueId"]==int(issueId):
                tmplist.append(each)
                break
        issuelist=tmplist  

    if len(issuelist)>0:   
        issuelistIds = [ issue["issueId"] for issue in issuelist ]
        
        typelist=['单位工程','楼层','分区','构件','构件组','危险源','安全设施']
        pblistall = []
        response_data["issuepblist"] = []
        for issueId in issuelistIds:
            unitprjIdlist=[]
            elevationIdlist=[]
            zoneIdlist=[]
            PbGrpIdlist=[]
            PbIdlist=[]
            hazardIdlist=[]
            related_items = ProjecteventElement.objects.filter(typetable__in=typelist,event_id=issueId)
            for ele in related_items:
                if ele.typetable=="单位工程":
                    unitprjIdlist.append(ele.relatedid)
                elif ele.typetable=="楼层":
                    elevationIdlist.append(ele.relatedid)
                elif ele.typetable=="分区":
                    zoneIdlist.append(ele.relatedid)
                elif ele.typetable=="构件组":
                    PbGrpIdlist.append(ele.relatedid)
                elif ele.typetable=="构件":
                    PbIdlist.append(ele.relatedid)
                elif ele.typetable=="安全设施":
                    PbIdlist.append(ele.relatedid)
                elif ele.typetable=="危险源":
                    hazardIdlist.append(ele.relatedid)
                else:
                    pass

            if len(hazardIdlist)>0:
                hazardlist = Hazardevent.objects.filter(id__in=hazardIdlist)
                for ele in hazardlist:
                    if ele.relatedspace_type=="单位工程":
                        unitprjIdlist.append(ele.relatedspace_id)
                    elif ele.relatedspace_type=="楼层":
                        elevationIdlist.append(ele.relatedspace_id)
                    elif ele.relatedspace_type=="分区":
                        zoneIdlist.append(ele.relatedspace_id)
                    elif ele.relatedspace_type=="构件":
                        PbIdlist.append(ele.relatedspace_id)
                    else:
                        pass

            # if len(zoneIdlist)>0:
            #     Pbgroups=Pbgroup.objects.filter(zone_id__in=zoneIdlist)
            #     pbgrppblist = Pbgrouprelation.objects.filter(pbgroup__in=Pbgroups).values_list('pb_id', flat=True)
            #     PbIdlist.extend(pbgrppblist)

            if len(PbGrpIdlist)>0:
                pbgrppblist = Pbgrouprelation.objects.filter(pbgroup__in=PbGrpIdlist).values_list('pb_id', flat=True)
                PbIdlist.extend(pbgrppblist)


            list_issue_pbs=list_items_issue.filter(Q(elevation__unitproject_id__in=unitprjIdlist)|
                                     Q(elevation_id__in=elevationIdlist)|Q(zone_id__in=zoneIdlist)|
                                     Q(id__in=PbIdlist)).exclude(lvmdbid__isnull=True).values_list('lvmdbid', flat=True)

            tmpObj = {}
            tmpObj["issueId"] = issueId
            tmpObj["pblist"] = map(int,map(str,list_issue_pbs))
            response_data["issuepblist"].append(tmpObj)

            pblistall.extend(list_issue_pbs)

        tmpObj = {}
        tmpObj["type"]="needtick"
        color = "#e1b274"
        if issuetype=="质量问题":
            color= "#e1b274"
        else:
            color="#ED002F" 
        if iswholemodel=="true":
            tmpObj["color"] =color
        else:
            tmpObj["color"] = color
        tmpObj["pblist"] = []
        for eachpb in set(pblistall):
            tmpPb = {}
            tmpPb["lvmdbid"] = eachpb
            tmpObj["pblist"].append(tmpPb)
        response_data["pbstatuslist"].append(tmpObj)

def getUserFlowTempList(user,flowtype="",MajorId=None):
    if flowtype:
        userflowsteplist = FlowStepUser.objects.filter(flowstep__template__flowtype__name=flowtype,flowstep__isstartstep=True,user=user,isactor=True).values_list('flowstep_id', flat=True)
    else:
        userflowsteplist = FlowStepUser.objects.filter(flowstep__isstartstep=True,user=user,isactor=True).values_list('flowstep_id', flat=True)
    
    if MajorId==None:
        userflowtemplist = [ r.template for r in FlowTemplateStep.objects.filter(isstartstep=True,id__in=userflowsteplist)]
    else:
        if MajorId not in [1,2,4,9]:
            MajorId = 1
        userflowtemplist = [ r.template for r in FlowTemplateStep.objects.filter(isstartstep=True,id__in=userflowsteplist,template__major_id=MajorId)]

    return userflowtemplist


def getUserFlowTempListAll(user,flowtype):
    userflowsteplist = FlowStepUser.objects.filter(user=user,flowstep__template__flowtype__name=flowtype).values_list('flowstep_id', flat=True)

    userflowtemplist = set([ r.template for r in FlowTemplateStep.objects.filter(id__in=userflowsteplist)])

    return userflowtemplist

def getTemplateMajorList(flowtype=""):
    majorlist = FlowTemplate.objects.filter(flowtype__name=flowtype).values('major_id').distinct().values_list('major_id', flat=True)
    return UserMajor.objects.filter(id__in=list(majorlist))

def updateRelateType(proeventObj):
    elelist = ProjecteventElement.objects.filter(event=proeventObj)
    for each in elelist:
        if each.typetable=="危险源":
            try:
                hz=Hazardevent.objects.get(id=each.relatedid)
                status = HazardStatus.objects.get(statusname = "受控")
                Hazardevent.objects.filter(hazard_code=hz.hazard_code,relatedspace_type=hz.relatedspace_type,
                    relatedspace_id=hz.relatedspace_id,his_date=datetime.date.today()).update(curstatus=status)
            except:
                pass
            
        else:
            pass


def getEventRelateDesc(event):
    desc=""
    glyss = ProjecteventElement.objects.filter(event_id=event.id)
    for glys in glyss:
        s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
        desc +=s+","
    if desc:
        desc=desc[:-1]
    return desc