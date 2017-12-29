# -*- coding: utf-8 -*-
'''

@author: pgb
'''
import traceback,datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import loader, Context, RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from TaskAndFlow.utility_flowtemplate import *
from UserAndPrj.models import *
from TaskAndFlow.models import *
from TaskAndFlow.forms import *
from dss.Serializer import serializer as objtojson
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
from Scc4PM.settings import CURRENT_PROJECT_ID
from Business.models import *
from TaskAndFlow.utility_filemanager import *
from UserPrjConfig.permissions import *

@csrf_exempt
@login_required(login_url="/login/")
def issue_list2(request):
    if request.method=='GET':
        #FlowTemplateList = getUserFlowTempList(request.user,issuetype)
        issuetypeorg = request.GET.get('issuetype', '')
        title = getTitleFromUrl(request,"/task/issue/list/?issuetype="+issuetypeorg)
        issuetype = transIssueType(issuetypeorg)
        createuserlist = set(each.createuser for each in projectevent.objects.filter(template__flowtype__name=issuetype))

        issuecategory = []
        if isFlowTypeXiaoTiao(issuetype):
            issuecategory = eval(CustomInfo.objects.get(infotype="event_category").custominfo)
       
        majorList = getTemplateMajorList(issuetype)

        if checkMobile(request):
            templateName = 'TaskAndFlow/xietiao/eventlist.html'
        else:
            templateName = 'TaskAndFlow/xietiao/eventlist.html'
        return render_to_response(templateName, RequestContext(request, locals()))
    elif request.method=='POST':
        response_data = {}
        response_data["issuc"] = False
        response_data["total"] = 0
        response_data["issuelist"] = []
        try:
            # 获取页数
            page = int(request.POST.get('page', '1'))
            perPage = int(request.POST.get('perPage', '10'))
            issuetypeorg = request.POST.get('issuetype', '')

            # 查询条件
            filterval = eval(request.POST.get('filterval', '{}'))
            print filterval
 
            issuetype = transIssueType(issuetypeorg)
            issuecategorys=[]

            list_items = projectevent.objects.filter(template__flowtype__name=issuetype).order_by("curdealstep","-createtime")
            if filterval:
                if filterval['stepIds']:
                    list_items = list_items.filter(curflowstep_id__in=filterval['stepIds'])
                if filterval['priority']:
                    list_items = list_items.filter(priority__in=filterval['priority'])
                if filterval['createtime']:
                    startdate, enddate = GetDateRangeArray(filterval['createtime'])
                    list_items = list_items.filter(createtime__range=(startdate, enddate))
                if filterval['deadline']:
                    startdate, enddate = GetDateRangeArray(filterval['deadline'])
                    list_items = list_items.filter(deadline__range=(startdate, enddate))
                if filterval['createuser']:
                    list_items = list_items.filter(createuser_id__in=filterval['createuser'])
                if filterval['fuzefenbao']:
                    list_items = list_items.filter(template__major__id__in=filterval['fuzefenbao'])
                if filterval['issuecategorys']:
                    issuecategorys = filterval['issuecategorys']
                    

            starttime = time.time()
            mapstepactor = {}
            mapstepwatch = {}
            for each in FlowStepUser.objects.all():
                if each.isactor: 
                    if not mapstepactor.has_key(each.flowstep_id):
                        mapstepactor[each.flowstep_id] = set()
                        mapstepactor[each.flowstep_id].add(each.user_id)
                    else:
                        mapstepactor[each.flowstep_id].add(each.user_id)
                else:
                    if not mapstepwatch.has_key(each.flowstep_id):
                        mapstepwatch[each.flowstep_id] = set()
                        mapstepwatch[each.flowstep_id].add(each.user_id)
                    else:
                        mapstepwatch[each.flowstep_id].add(each.user_id)

            mapeventuser = {}
            for each in EventStepOperation.objects.filter(eventstep__flowstep__template__flowtype__name=issuetype):
                if not mapeventuser.has_key(each.eventstep.projectevent_id):
                    mapeventuser[each.eventstep.projectevent_id] = set()
                    mapeventuser[each.eventstep.projectevent_id].add(each.actor_id)
                else:
                    mapeventuser[each.eventstep.projectevent_id].add(each.actor_id)

            mapusername = { each.id:each.truename for each in getPrjUserlist() }

            issuelist=[]
            for each in list_items:
                # 只有保存的用户可以编辑 pgb
                if each.issave and request.user.id != each.saveuser_id:
                    continue

                if each.extend:
                    extenddict = eval(each.extend)
                    if issuecategorys and extenddict.has_key("category") and extenddict["category"] not in issuecategorys:
                        continue

                try:
                    if (not mapstepactor.has_key(each.curflowstep_id) or (mapstepactor.has_key(each.curflowstep_id) and request.user.id not in mapstepactor[each.curflowstep_id])) and  \
                       (not mapstepwatch.has_key(each.curflowstep_id) or (mapstepwatch.has_key(each.curflowstep_id) and request.user.id not in mapstepwatch[each.curflowstep_id])) and\
                       mapeventuser.has_key(each.id) and request.user.id not in mapeventuser[each.id]:
                        continue
                except Exception as e:
                    traceback.print_exc()
                    pass

                issuelist.append(each)

            response_data["total"] = len(issuelist)

            issuelist = issuelist[(page-1)*perPage:page*perPage]



            issuelist_page = []
            for each in issuelist:
                issue = {}
                issue["issueId"] = each.id
                issue["number"] = each.number
                issue["title"] = each.title if each.title else each.describe
                issue["describe"] = each.describe
                issue["faqiren"] = mapusername[each.createuser_id] if mapusername.has_key(each.createuser_id) else "--"
                issue["faqishijian"] = str(each.createtime)
                issue["deadline"] = each.deadline.strftime("%Y-%m-%d")
                issue["unfinished"] = False
                if each.curdealstep!=3 and each.deadline<datetime.datetime.now():
                    issue["unfinished"] = True
                
                issue["dangqianfuzeren"] = ""
                if mapstepactor.has_key(each.curflowstep_id):
                    issue["dangqianfuzeren"] = ','.join([mapusername[stepuser] if mapusername.has_key(stepuser) else "--" for stepuser in mapstepactor[each.curflowstep_id]])

                if each.issave:
                    issue["needdeal"] = True
                else:
                    issue["needdeal"] = checkEventNeedDeal(each, request.user)


                issue["candelete"] = False
                if each.createuser==request.user or request.user.has_perm(""):
                    issue["candelete"] = True

                glyss = ProjecteventElement.objects.filter(event_id=each.id)
                issue["guanlianyuansu"] = []
                issue["guanlianyuansudis"]=""
                for glys in glyss:
                    s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
                    issue["guanlianyuansu"].append(s)
                    issue["guanlianyuansudis"] +=s+","
                issue["guanlianyuansudis"]=issue["guanlianyuansudis"][:-1]
                issue["priority"]=each.priority
                issue["flowstep"]=each.curflowstep.name
                issuelist_page.append(issue)

            response_data["issuc"] = True
            
            response_data["perPage"] = perPage
            response_data["issuelist"] = issuelist_page
        except:
            traceback.print_exc()
        return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required(login_url="/login/")
def issuelistcount(request):
    response_data = {}
    response_data["issuc"] = False
    response_data["total"] = 0
    response_data["templatetree"] = []
    try:
        issuetypeorg = request.GET.get('issuetype', '')
        issuetype = transIssueType(issuetypeorg)
        list_items = projectevent.objects.filter(template__flowtype__name=issuetype)
       

        mapstepactor = {}
        mapstepwatch = {}
        for each in FlowStepUser.objects.all():
            if each.isactor: 
                if not mapstepactor.has_key(each.flowstep_id):
                    mapstepactor[each.flowstep_id] = set()
                    mapstepactor[each.flowstep_id].add(each.user_id)
                else:
                    mapstepactor[each.flowstep_id].add(each.user_id)
            else:
                if not mapstepwatch.has_key(each.flowstep_id):
                    mapstepwatch[each.flowstep_id] = set()
                    mapstepwatch[each.flowstep_id].add(each.user_id)
                else:
                    mapstepwatch[each.flowstep_id].add(each.user_id)

        mapeventuser = {}
        for each in EventStepOperation.objects.filter(eventstep__flowstep__template__flowtype__name=issuetype):
            if not mapeventuser.has_key(each.eventstep.projectevent_id):
                mapeventuser[each.eventstep.projectevent_id] = set()
                mapeventuser[each.eventstep.projectevent_id].add(each.actor_id)
            else:
                mapeventuser[each.eventstep.projectevent_id].add(each.actor_id)

        mapusername = { each.id:each.truename for each in getPrjUserlist() }

        mapissueCount = {}
        issuelist=[]
        for each in list_items:
            # 只有保存的用户可以编辑 pgb
            if each.issave and request.user.id != each.saveuser_id:
                continue

            try:
                if (not mapstepactor.has_key(each.curflowstep_id) or (mapstepactor.has_key(each.curflowstep_id) and request.user.id not in mapstepactor[each.curflowstep_id])) and  \
                   (not mapstepwatch.has_key(each.curflowstep_id) or (mapstepwatch.has_key(each.curflowstep_id) and request.user.id not in mapstepwatch[each.curflowstep_id])) and\
                   mapeventuser.has_key(each.id) and request.user.id not in mapeventuser[each.id]:
                    continue
            except Exception as e:
                traceback.print_exc()
                pass


            if  mapissueCount.has_key(str(each.curflowstep_id)):
                mapissueCount[str(each.curflowstep_id)] += 1
            else:
                mapissueCount[str(each.curflowstep_id)] = 1

            if mapissueCount.has_key("template_"+str(each.template_id)):
                mapissueCount["template_"+str(each.template_id)] += 1
            else:
                mapissueCount["template_"+str(each.template_id)] = 1

            issuelist.append(each)

        response_data["total"] = len(issuelist)


        #问题统计
        templatelist = getUserFlowTempListAll(request.user, issuetype)
        templatetree = []
        for unit in templatelist:
            child_data = {}
            child_data["id"]="template_"+str(unit.id)
            child_data["text"]=unit.name
            child_data["title"]=unit.name
            child_data["expand"]=False
            child_data["checked"]=False
            child_data["count"]= mapissueCount[child_data["id"]] if mapissueCount.has_key(child_data["id"]) else 0
            
            steplist=FlowTemplateStep.objects.filter(template=unit)
            sub_child_list=[]
            for item in steplist:
                sub_child_data = {}
                sub_child_data["id"]=str(item.id)
                sub_child_data["text"]=item.name
                sub_child_data["title"]=item.name
                sub_child_data["checked"]=False
                sub_child_data["count"]=mapissueCount[sub_child_data["id"]] if mapissueCount.has_key(sub_child_data["id"]) else 0
                sub_child_list.append(sub_child_data)
            child_data["children"]=sub_child_list
            templatetree.append(child_data)

        response_data["templatetree"] = templatetree
        response_data["issuc"] = True
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/")
def shiyicreate(request):
    if request.method=='GET':
        try:
            issuetype = u"协调事宜"

            FlowTemplateList = getUserFlowTempList(request.user,issuetype)

            majorList = getMajorList()
            curMajorId = None
            if FlowTemplateList:
                curMajorId = FlowTemplateList[0].major_id
            biaohao = getEventNumber(issuetype)
        except:
            traceback.print_exc()
        templateName = 'TaskAndFlow/xietiao/eventcreate.html'
        return render_to_response(templateName, RequestContext(request, locals()))
    elif request.method=='POST':
        pass


@login_required(login_url="/login/")
def qianzhengcreate(request):
    try:
        issuetype = u"现场签证"

        FlowTemplateList = getUserFlowTempList(request.user,issuetype)

        majorList = getMajorList()
        curMajorId = None
        if FlowTemplateList:
            curMajorId = FlowTemplateList[0].major_id

        bianhao = getEventNumber(issuetype)
    except:
        traceback.print_exc()
    templateName = 'TaskAndFlow/xietiao/eventcreate.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@login_required(login_url="/login/")
def qianzhenglist(request):
    issuetypeorg = 'xianchangqianzheng'
    issuetype = transIssueType(issuetypeorg)
    title = getTitleFromUrl(request,"/task/issue/qianzhenglist/")
    createuserlist = set(each.createuser for each in projectevent.objects.filter(template__flowtype__name=issuetype))

    issuecategory = []
    if isFlowTypeXiaoTiao(issuetype):
        issuecategory = eval(CustomInfo.objects.get(infotype="event_category").custominfo)

    majorList = getTemplateMajorList(issuetype)
    templateName = 'TaskAndFlow/xietiao/eventlist.html'
    return render_to_response(templateName, RequestContext(request, locals()))




@login_required(login_url="/login/")
def gcjdksqcreate(request):
    try:
        issuetype = u"工程进度款申请"

        FlowTemplateList = getUserFlowTempList(request.user,issuetype)

        majorList = getMajorList()
        curMajorId = None
        if FlowTemplateList:
            curMajorId = FlowTemplateList[0].major_id

        bianhao = getEventNumber(issuetype)
    except:
        traceback.print_exc()
    templateName = 'TaskAndFlow/xietiao/eventcreate.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@login_required(login_url="/login/")
def gcjdksqlist(request):
    issuetypeorg = 'gcjdksq'
    issuetype = transIssueType(issuetypeorg)
    title = getTitleFromUrl(request,"/task/issue/gcjdksqlist/")
    createuserlist = set(each.createuser for each in projectevent.objects.filter(template__flowtype__name=issuetype))

    issuecategory = []
    if isFlowTypeXiaoTiao(issuetype):
        issuecategory = eval(CustomInfo.objects.get(infotype="event_category").custominfo)

    majorList = getTemplateMajorList(issuetype)

    templateName = 'TaskAndFlow/xietiao/eventlist.html'
    return render_to_response(templateName, RequestContext(request, locals()))



@login_required(login_url="/login/")
def sjbgtzcreate(request):
    try:
        issuetype = u"设计变更通知"

        FlowTemplateList = getUserFlowTempList(request.user,issuetype)

        majorList = getMajorList()
        curMajorId = None
        if FlowTemplateList:
            curMajorId = FlowTemplateList[0].major_id

        bianhao = getEventNumber(issuetype)
        categoryList = []
        try:
            categoryList = eval(CustomInfo.objects.get(infotype='event_category').custominfo)
        except:
            pass
    except:
        traceback.print_exc()
    templateName = 'TaskAndFlow/xietiao/eventcreate.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@login_required(login_url="/login/")
def sjbgtzlist(request):
    issuetypeorg = 'sjbgtz'
    issuetype = transIssueType(issuetypeorg)
    title = getTitleFromUrl(request,"/task/issue/sjbgtzlist/")
    createuserlist = set(each.createuser for each in projectevent.objects.filter(template__flowtype__name=issuetype))

    issuecategory = []
    if isFlowTypeXiaoTiao(issuetype):
        issuecategory = eval(CustomInfo.objects.get(infotype="event_category").custominfo)
        print issuecategory

    majorList = getTemplateMajorList(issuetype)

    templateName = 'TaskAndFlow/xietiao/eventlist.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def bgsjbacreate(request):
    try:
        issuetype = u"变更设计备案"

        FlowTemplateList = getUserFlowTempList(request.user,issuetype)

        majorList = getMajorList()
        curMajorId = None
        if FlowTemplateList:
            curMajorId = FlowTemplateList[0].major_id

        bianhao = getEventNumber(issuetype)
        categoryList = []
        try:
            categoryList = eval(CustomInfo.objects.get(infotype='event_category').custominfo)
        except:
            pass
    except:
        traceback.print_exc()
    templateName = 'TaskAndFlow/xietiao/eventcreate.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@login_required(login_url="/login/")
def bgsjbalist(request):
    issuetypeorg = 'bgsjba'
    issuetype = transIssueType(issuetypeorg)
    title = getTitleFromUrl(request,"/task/issue/bgsjbalist/")
    createuserlist = set(each.createuser for each in projectevent.objects.filter(template__flowtype__name=issuetype))

    issuecategory = []
    if isFlowTypeXiaoTiao(issuetype):
        issuecategory = eval(CustomInfo.objects.get(infotype="event_category").custominfo)
 
    majorList = getTemplateMajorList(issuetype)

    templateName = 'TaskAndFlow/xietiao/eventlist.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def tzhscreate(request):
    try:
        issuetype = u"图纸会审"

        FlowTemplateList = getUserFlowTempList(request.user,issuetype)

        majorList = getMajorList()
        curMajorId = None
        if FlowTemplateList:
            curMajorId = FlowTemplateList[0].major_id

        bianhao = getEventNumber(issuetype)
        categoryList = []
        try:
            categoryList = eval(CustomInfo.objects.get(infotype='event_category').custominfo)
        except:
            pass
    except:
        traceback.print_exc()
    templateName = 'TaskAndFlow/xietiao/eventcreate.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@login_required(login_url="/login/")
def tzhslist(request):
    issuetypeorg = 'tzhs'
    issuetype = transIssueType(issuetypeorg)
    title = getTitleFromUrl(request,"/task/issue/tzhslist/")
    createuserlist = set(each.createuser for each in projectevent.objects.filter(template__flowtype__name=issuetype))

    issuecategory = []
    if isFlowTypeXiaoTiao(issuetype):
        issuecategory = eval(CustomInfo.objects.get(infotype="event_category").custominfo)
 
    majorList = getTemplateMajorList(issuetype)

    templateName = 'TaskAndFlow/xietiao/eventlist.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def bimshcreate(request):
    try:
        issuetype = u"BIM深化"

        FlowTemplateList = getUserFlowTempList(request.user,issuetype)

        majorList = getMajorList()
        curMajorId = None
        if FlowTemplateList:
            curMajorId = FlowTemplateList[0].major_id

        bianhao = getEventNumber(issuetype)
    except:
        traceback.print_exc()
    templateName = 'TaskAndFlow/xietiao/eventcreate.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@login_required(login_url="/login/")
def bimshlist(request):
    issuetypeorg = 'bimsh'
    issuetype = transIssueType(issuetypeorg)
    title = getTitleFromUrl(request,"/task/issue/bimshlist/")
    createuserlist = set(each.createuser for each in projectevent.objects.filter(template__flowtype__name=issuetype))
 
    issuecategory = []
    if isFlowTypeXiaoTiao(issuetype):
        issuecategory = eval(CustomInfo.objects.get(infotype="event_category").custominfo)

    majorList = getTemplateMajorList(issuetype)

    templateName = 'TaskAndFlow/xietiao/eventlist.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@csrf_exempt
@login_required(login_url="/login/")
def issue_count(request):
    if request.method=='GET':
        issuetypeorg = request.GET.get('issuetype', '')
        title = getTitleFromUrl(request,"/task/issue/list/?issuetype="+issuetypeorg)
        if issuetypeorg=="zhiliang" and not request.user.has_perm("查看质量问题统计"):
            return HttpResponseRedirect('/error_403/')
        if issuetypeorg=="anquan" and not request.user.has_perm("查看安全问题统计"):
            return HttpResponseRedirect('/error_403/')

        if checkMobile(request):
            templateName = 'TaskAndFlow/statistical/problem_show.html'
        else:
            templateName = 'TaskAndFlow/statistical/problem_show.html'
        return render_to_response(templateName, RequestContext(request, locals()))
    elif request.method=='POST':
        response_data = {}
        response_data["issuc"] = 'false'
        try:
            issuetypeorg = request.POST.get('issuetype', '')
            issuetype = transIssueType(issuetypeorg)

            list_items = projectevent.objects.filter(template__flowtype__name=issuetype)

            createtime = request.POST.get('createtime', None)
            if createtime:
                startdate, enddate = GetDateRange(createtime)
                list_items = list_items.filter(createtime__range=(startdate, enddate))

            issuelistCount = []
            issuelistUnDo = []
            issuelistPriority = []
            issuelistDoneOnTime = []
            timelist = []
            majorlist = getMajorList()
            for each in majorlist:
                majortotal = list_items.filter(template__major=each)
                issuelistUnDo.append(majortotal.exclude(curdealstep=3).count())
                doneonTimeCount = majortotal.filter(curdealstep=3,updatetime__lt=F('deadline')).count()
                print "111111111111111111:"+str(doneonTimeCount)
                doneonTimePercent = round(doneonTimeCount/float(majortotal.count())*100.0 if majortotal.count() else 0.0,2)
                issuelistDoneOnTime.append(doneonTimePercent)
                tmplist = []
                tmplist.append(majortotal.filter(priority=1).count())
                tmplist.append(majortotal.filter(priority=5).count())
                tmplist.append(majortotal.filter(priority=10).count())
                issuelistPriority.append(tmplist)

            
            if list_items.count()>0:
                timebegin = list_items.order_by('createtime')[0].createtime
                print timebegin
                for each in majorlist:
                    tmplist = []
                    index=0
                    while 1:
                        weekly_begindate,weekly_enddate=getWeekDateRange(index)
                        if not issuelistCount:
                            timelist.insert(0,weekly_begindate.strftime("%Y/%m/%d")+"-"+weekly_enddate.strftime("%Y/%m/%d"))
                        majortotal = list_items.filter(template__major=each,createtime__range=(weekly_begindate, weekly_enddate)).count()
                        tmplist.insert(0,majortotal)
                        if weekly_begindate<timebegin:
                            break 
                        index = index-1
                    issuelistCount.append(tmplist)

            response_data["issuelistUnDo"] = issuelistUnDo
            response_data["issuelistPriority"] = issuelistPriority
            response_data["issuelistDoneOnTime"] = issuelistDoneOnTime  
            response_data["timelist"] = timelist  
            response_data["issuelistCount"] = issuelistCount  
            response_data["majorlist"] = list(majorlist.values_list('name', flat=True))
            response_data["issuc"] = 'true'


        except:
            traceback.print_exc()
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def issuetrace(request):
    response_data = {}
    response_data["res"] = 'fail'
    try:
        issueId = request.GET.get('issueId', None)
        projectevent_instance = projectevent.objects.get(id=issueId)
        eventStepsRecord = Eventstep.objects.filter(projectevent=projectevent_instance).values()

        recordlist = []
        for step in eventStepsRecord:
            tmp = objtojson(step)
            tmp["stepName"] = FlowTemplateStep.objects.get(id=step['flowstep_id']).name
            tmp["operationRecord"] = []
            for each in EventStepOperation.objects.filter(eventstep_id=step["id"]).values():
                tmpOpr = objtojson(each)
                tmpOpr["actorName"] = User.objects.get(id=each["actor_id"]).truename
                if each["flowstepoper_id"]:
                    tmpOpr["operaName"] = FlowStepOperation.objects.get(id=each["flowstepoper_id"]).name

                tmpOpr["imglist"] = [objtojson(doc.document) for doc in Doc2Relate.objects.filter(relatetype=u"事件步骤操作", relateid=each["id"],  document__filetype__contains="image")]

                tmpOpr["voiceList"] = [objtojson(doc.document) for doc in Doc2Relate.objects.filter(relatetype=u"事件步骤操作", relateid=each["id"],  document__filetype__contains="audio")]

                tmpOpr["doclist"]  = [objtojson(doc.document) for doc in 
                        Doc2Relate.objects.filter(relatetype=u"事件步骤操作",relateid=each["id"]).exclude(document__filetype__contains="image").exclude(document__filetype__contains="audio")]
    
                tmp["operationRecord"].append(tmpOpr)
            recordlist.append(tmp)

        response_data["eventStepsRecord"]=recordlist
        response_data["res"] = 'sucess'
    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def getissuenumber(request):
    response_data = {}
    response_data["res"] = 'fail'
    try:
        issuetype = request.GET.get('issuetype', None)
        templateId = request.GET.get('templateId', None)
        if not issuetype:
            issuetype=FlowTemplate.objects.get(id=templateId).flowtype.name
        response_data["number"]=getEventNumber(issuetype)
        response_data["res"] = 'sucess'
    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e

    return HttpResponse(json.dumps(response_data), content_type="application/json")


