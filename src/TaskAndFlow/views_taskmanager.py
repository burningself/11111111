# -*- coding: utf-8 -*-
'''

@author: pgb
'''
import traceback,datetime,uuid,time,chardet
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from TaskAndFlow.utility import *
from UserAndPrj.models import *
from TaskAndFlow.models import *
# from TaskAndFlow.forms import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
from Scc4PM.settings import CURRENT_PROJECT_ID
from django.db.models import F
from TaskAndFlow.utility_filemanager import *
from TaskAndFlow.utility_taskmanager import *
from TaskAndFlow.utility_flowtemplate import *
from urllib import unquote
from UserPrjConfig.permissions import *

@login_required(login_url="/login/") 
@check_permission
def manager_projecttask(request):
    title = getTitleFromUrl(request, request.get_full_path())
    majorList = UserMajor.objects.all()
    tasktypeList = TaskType.objects.all()
    return render_to_response('TaskAndFlow/taskmanager/taskmanager.html', RequestContext(request,locals()))
    
    

@login_required(login_url="/login/") 
def getprojecttasklist(request):
    jsonprogress = getProjectTaskProgressInfo()
    if jsonprogress:
        return HttpResponse(jsonprogress, content_type="application/json")  
    else:
        MajorId = request.GET.get('MajorId', None)
        jsonprogress=calcProjectTaskProgressInfo(MajorId)
        return HttpResponse(jsonprogress, content_type="application/json")  

@login_required(login_url="/login/") 
def gethisprojecttasklist(request):
    
    response_data = {}
    response_data["projecttasklist"]=[]
    
    try:
        _selVersionId = int(request.GET.get('_selVersionId', ''))
        #todo 由于目前没有多个版本的任务，暂时还是用当前任务表 pangubing
        list_items = ProjectTask.objects.all()
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
            tmpObj["pParent"] =  each.parentid.id if each.parentid else ""
            tmpObj["pOpen"] = 0 if each.parentid else 1
            #tmpObj["pDepend"] = ""
            #tmpObj["pCaption"] = each.description
            #tmpObj["pNotes"] = ""
            #tmpObj["pGantt"] = "g"
    
            response_data["projecttasklist"].append(tmpObj)
        
        response_data["issuc"]="true"
    except Exception, e:
        response_data["issuc"]="false"
        response_data['error'] = '%s' % e
    
    return HttpResponse(json.dumps(response_data), content_type="application/json") 


@login_required(login_url="/login/") 
def getprjversiionlist(request):
    
    response_data = {}
    response_data["prjversiionlist"]=[]
    
    try:
        list_items = Projectversion.objects.all()
        for each in list_items:
            tmpObj = {}
            tmpObj["id"] = each.id
            tmpObj["version_code"] = each.version_code
            tmpObj["update_time"] = each.update_time.strftime('%Y-%m-%d')  if each.update_time else ''
            tmpObj["description"] = each.description if each.description else ''
            tmpObj["filelist"] = []
            relatefiles = Projectupdatefiles.objects.filter(projectversion=each)
            for eachfile in relatefiles:
                fileobj = {}
                fileobj["id"] = eachfile.id
                fileobj["name"] = eachfile.file.name
                fileobj["shortname"] = eachfile.file.shortname
                fileobj["filepath"] = str(eachfile.file.filepath)
                tmpObj["filelist"].append(fileobj)
            response_data["prjversiionlist"].append(tmpObj)
        
        response_data["issuc"]="true"
    except Exception, e:
        response_data["issuc"]="false"
        response_data['error'] = '%s' % e
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required(login_url="/login/")  
def projecttask_qrcode(request):

    tasklist=ProjectTask.objects.all()
    if 'taskid' in request.GET:
        taskid=int(request.GET.get('taskid',0))
        tasklist=tasklist.filter(id=taskid)
    MajorId = request.GET.get('MajorId', None)
    if MajorId and MajorId!="0":
        tasklist = tasklist.filter(major_id=int(MajorId))
    
    pro=Project.objects.get(id=CURRENT_PROJECT_ID)
        
    templateName='TaskAndFlow/taskmanager/task_qrcode.html'
    return render_to_response(templateName, RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/") 
@check_permission_ajax
def create_projecttask(request):
    response_data = {}
    try:
        taskname = request.POST.get('taskname', '')
        taskparentId = request.POST.get('taskparentId', '')
        dealTemplateMajor = request.POST.get('dealTemplateMajor', '')
        planstart = request.POST.get('planstart', '')
        planfinish = request.POST.get('planfinish', '')
        taskdescribe = request.POST.get('taskdescribe', '')  
        tasktype = request.POST.get('tasktype', '')  
          
        if taskname=="":
            raise Exception(u'任务名称不能为空！')
        if taskparentId=="":
            raise Exception(u'任务父节点不能为空！')
        if planstart=="":
            raise Exception(u'任务计划开始时间不能为空！')
        if planfinish=="":
            raise Exception(u'任务计划结束时间不能为空！')
        
        if ProjectTask.objects.filter(name=taskname).count()>0:
            raise Exception(u'已有同名任务！')
        
        if ProjectTask.objects.filter(id=taskparentId).count()>0:
            parenttask = ProjectTask.objects.filter(id=taskparentId)[0]
        else:
            raise Exception(u'任务父节点不存在！')
        
        planstart=datetime.datetime.strptime(planstart+" 08:00:00",'%Y-%m-%d %H:%M:%S')
        planfinish=datetime.datetime.strptime(planfinish+" 17:00:00",'%Y-%m-%d %H:%M:%S')  
        print planstart
        if planstart > planfinish:
            raise Exception(u'开始时间大于结束时间！')
        
        if planstart < parenttask.planstart:
            raise Exception(u'开始时间应该大于等于父节点的开始时间！')
         
        if planfinish > parenttask.planfinish:
            raise Exception(u'结束时间应该小于等于父节点的结束时间！')
        
        taskuuid = uuid.uuid1()
        newtask = ProjectTask.objects.create(msprojectid=taskuuid,name=taskname,parentid=parenttask,major_id=dealTemplateMajor,
                                    planstart=planstart,planfinish=planfinish,description=taskdescribe,type_id=tasktype)
               
        response_data["issuc"]="true"
        
    except Exception, e: 
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@login_required(login_url="/login/") 
def get_projecttask(request):
    taskid = int(request.GET.get('taskid', '0'))
    response_data = {}
    try:
        each = ProjectTask.objects.get(id=taskid)
        
        issue={}
        issue["taskId"] = each.id
        issue["name"]=each.name
        issue["parentname"]=each.parentid.name if each.parentid else u""
        issue["parentid"]=each.parentid.id if each.parentid else u""
        issue["editmajor"]= each.major.name if each.major else u""
        issue["editplanstart"]=each.planstart.strftime("%Y-%m-%d")
        issue["editplanfinish"]=each.planfinish.strftime("%Y-%m-%d")
        issue["editactualstart"]=each.actualstart.strftime("%Y-%m-%d") if each.actualstart else u""
        issue["editacutalfinish"]=each.acutalfinish.strftime("%Y-%m-%d") if each.acutalfinish else u""
        issue["percentage"]=each.percentage
        issue["description"]=each.description

        response_data["task"]=issue
        response_data["issuc"]="true"
        #print json.dumps(response_data)
    except Exception, e: 
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    
    return HttpResponse(json.dumps(response_data), content_type="application/json") 


def getParentTaskDiGui(each):
    if each.parentid:
        parent=ProjectTask.objects.get(id=each.parentid_id)
        if parent.percentage!=100:
            prelist = ProjectTask.objects.filter(taskpath__contains=str(parent.id)+"/").values("percentage").distinct() 
            print prelist
            if len(prelist)==1 and prelist[0]["percentage"]==100.0:
                parent.percentage = 100
                parent.acutalfinish=ProjectTask.objects.filter(taskpath__contains=str(parent.id)+"/").order_by("-acutalfinish")[0].acutalfinish
                parent.actualstart=ProjectTask.objects.filter(taskpath__contains=str(parent.id)+"/").order_by("actualstart")[0].actualstart
                parent.save()
                getParentTaskDiGui(parent)

    
    return

@csrf_exempt 
@login_required(login_url="/login/") 
@check_permission_ajax
def edit_projecttask(request):
    response_data = {}
    try:
        edittaskId = request.POST.get('edittaskId', '')
        editactualstart = request.POST.get('editactualstart', '')
        editacutalfinish = request.POST.get('editacutalfinish', '')
        editdescription = request.POST.get('editdescription', '')  
        edicompletion = float(request.POST.get('edicompletion', '0')) 
        editplanstart = request.POST.get('editplanstart', '')
        editplanfinish = request.POST.get('editplanfinish', '')

        each = ProjectTask.objects.get(id=edittaskId)
        if editactualstart!="":
            editactualstart=datetime.datetime.strptime(editactualstart+" 08:00:00",'%Y-%m-%d %H:%M:%S')
            each.actualstart=editactualstart
        if editacutalfinish!="":
            editacutalfinish=datetime.datetime.strptime(editacutalfinish+" 17:00:00",'%Y-%m-%d %H:%M:%S')  
            if editactualstart > editacutalfinish:
                raise Exception(u'实际开始时间大于结束时间！')
            each.acutalfinish=editacutalfinish
        
        if editplanstart!="":
            editplanstart=datetime.datetime.strptime(editplanstart+" 08:00:00",'%Y-%m-%d %H:%M:%S')
            each.planstart=editplanstart
        if editplanfinish!="":
            editplanfinish=datetime.datetime.strptime(editplanfinish+" 17:00:00",'%Y-%m-%d %H:%M:%S')  
            if editplanstart > editplanfinish:
                raise Exception(u'计划开始时间大于结束时间！')
            each.planfinish=editplanfinish

        if editdescription!="":
            each.description = editdescription
            
        each.percentage = edicompletion
          
        each.save()

        if each.percentage==100:
             #父任务设置实际完成时间后，如果子任务没有设置实际完成，则与父任务一致；设置完成时间后，父任务、子任务完成百分比变为100；
            ProjectTask.objects.filter(Q(taskpath__contains=str(each.id)+"/")&
                                       Q(acutalfinish__isnull=True)).update(percentage=100,acutalfinish=editacutalfinish)

            #所有子任务设置实际完成时间或完成百分比为100%时，设置父任务的百分比为100%，实际完成时间为子任务中最晚的完成时间；
            getParentTaskDiGui(each)

        calcProjectTaskProgressInfo()    
        
        response_data["issuc"]="true"
        
    except Exception, e: 
        traceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@csrf_exempt 
@login_required(login_url="/login/") 
@check_permission_ajax
def del_projecttask(request):
    response_data = {}
    try:
        taskid = request.GET.get('taskid', '')
        each = ProjectTask.objects.get(id=taskid)
        if(PrecastBeam.objects.filter(task=each).count()>0):
            raise Exception(u'任务已结关联构件不能删除！')
        else:
            each.delete()
        
        response_data["issuc"]="true"
        
    except Exception, e: 
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@login_required(login_url="/login/") 
def trace_projecttask(request):
    taskid = int(request.GET.get('taskid', '0'))
    
    task = ProjectTask.objects.get(id=taskid)
    
    list_items = PrecastBeam.objects.filter(task_id=taskid)
    
    ElevationChoices = Elevation.objects.all()
    PBTypeChoices = PBType.objects.all()
    PBStatusChoices = PBStatus.objects.all()
    
    if request.method == 'GET':
        pbnumber = request.GET.get('number', '')
        pbelevation = request.GET.get('pbelevation', '0')
        pbtype = request.GET.get('pbtype', '0')
        pbstatus = request.GET.get('pbstatus', '0')
        orderby = request.GET.get('orderby', 'sign')
        clickcount = request.GET.get('clickcount', '0')
        if pbnumber:
            list_items=list_items.filter(sign__icontains=pbnumber)
        if pbelevation and (pbelevation!='0'):
            list_items=list_items.filter(elevation=pbelevation)
            if pbelevation.isdigit():
                pbelevation=int(pbelevation)
        if pbtype and (pbtype!='0'):
            list_items=list_items.filter(pbtype=pbtype)
            if pbtype.isdigit():
                pbtype=int(pbtype)
        if pbstatus and (pbstatus!='0'):
            list_items=list_items.filter(curstatus=pbstatus)
            if pbstatus.isdigit():
                pbstatus=int(pbstatus)
        if orderby:
            if clickcount=="0":
                list_items=list_items.order_by(orderby)
            else:
                dscorderby="-"+orderby
                list_items=list_items.order_by(dscorderby)
    
    paginator = Paginator(list_items ,20)
    listcount=len(list_items)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)
    templateName='TaskAndFlow/taskmanager/tasktrace.html'
    return render_to_response(templateName, RequestContext(request,locals()))

@login_required(login_url="/login/")
@check_permission
def status_projecttask(request):
    try:
        title = getTitleFromUrl(request, request.get_full_path())
        d1 = datetime.date.today()
        d2 = d1 + datetime.timedelta(-210)
        timerange = d2.strftime("%Y/%m/%d")+" - "+d1.strftime("%Y/%m/%d")
        
        unitinfo=Modelfile.objects.get(isdefault=True)
        unitprjlist = Modelfile.objects.all()
        floorList = Elevation.objects.all().order_by('id')
    except Exception, e: 
        print e
    return render_to_response('TaskAndFlow/taskmanager/taskstatus.html', RequestContext(request,locals()))



@login_required(login_url="/login/") 
def getstatus_projecttask(request):
    response_data = {}
    try:
        list_items = PrecastBeam.objects.all()
    
        curUnitId = request.GET.get('curUnitId', '')
        list_items=list_items.filter(elevation__unitproject=curUnitId)

        curMajor = request.GET.get('curMajor', '')
        print curMajor
        list_items=list_items.filter(pbtype__major=curMajor)
        

        # timerange = request.GET.get('timerange', '')
        # if timerange=="":
        #     d1 = datetime.date.today()
        #     d2 = d1 + datetime.timedelta(-30)
        #     timerange = d2.strftime("%Y/%m/%d")+" - "+d1.strftime("%Y/%m/%d")
                    
        # startdate,enddate = GetDateRange(timerange)
        # projlist = ProjectTask.objects.filter(Q(planfinish__gte=startdate)&Q(planfinish__lte=enddate)).values("id")
         
        # list_items=list_items.filter(Q(task__in=projlist))
        list_items=list_items.filter(Q(task__isnull=False))
        
        response_data["pbstatuslist"]=[]
        
        response_data["listcount"]  = list_items.count()
        
        curdate=datetime.datetime.now()
        countTypeList = ["weikaishi","jinxingzhong","wancheng","chaoshiweiwancheng","chaoshiweikaishi"]
        for counttype in countTypeList:
            tmpObj = {}
            tmpObj["name"] = counttype
            tmpObj["pblist"] = []
            response_data[counttype] = {}
            if counttype=="weikaishi":
                pblist = list_items.filter(Q(curstatus__isnull=True)&Q(task__planfinish__gte=curdate))
                #pblist = list_items.filter(Q(Q(curstatus__nextstatus__isnull=True)|Q(curstatus__iscritical=True))&Q(curstatustime__lt=F('task__planfinish') + datetime.timedelta(days=-1)))
            elif counttype=="jinxingzhong":
                #pblist = list_items.filter(Q(Q(curstatus__nextstatus__isnull=True)|Q(curstatus__iscritical=True))&Q(curstatustime__gte=F('task__planfinish')+ datetime.timedelta(days=-1))&Q(curstatustime__lte=F('task__planfinish')))
                pblist = list_items.filter(Q(curstatus__isnull=False)&Q(curstatus__nextstatus__isnull=False)&Q(curstatus__iscritical=False)&Q(task__planfinish__gte=curdate))
            elif counttype=="wancheng":
                pblist = list_items.filter(Q(curstatus__isnull=False)&Q(curstatus__nextstatus__isnull=True)|Q(curstatus__iscritical=True))
            elif counttype=="chaoshiweiwancheng":
                pblist = list_items.filter(Q(curstatus__isnull=False)&Q(curstatus__nextstatus__isnull=False)&Q(curstatus__iscritical=False)&Q(task__planfinish__lt=curdate))
            elif counttype=="chaoshiweikaishi":
                pblist = list_items.filter(Q(curstatus__isnull=True)&Q(task__planfinish__lt=curdate))

            response_data[counttype]["value"] = pblist.count()
            for eachpb in pblist:
                tmpPb = {}
                tmpPb["lvmdbid"] = eachpb.lvmdbid
                tmpObj["pblist"].append(tmpPb)
            response_data["pbstatuslist"].append(tmpObj)
    
        response_data["issuc"]="true"
    except Exception, e: 
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required(login_url="/login/") 
def getstatusgoal_projecttask(request):
    response_data = {}
    try:
        list_items = PrecastBeam.objects.all()
    
        curUnitId = request.GET.get('curUnitId', '')
        list_items=list_items.filter(elevation__unitproject=curUnitId)
        
        response_data["pbstatuslist"]=[]
        
        response_data["listcount"]  = list_items.count()
        
        countTypeList = ["zhiqianwancheng","wancheng","weiwancheng"]
        for counttype in countTypeList:
            tmpObj = {}
            tmpObj["name"] = counttype
            tmpObj["pblist"] = []
            response_data[counttype] = {}
            if counttype=="zhiqianwancheng":
                response_data[counttype]["color"]="#00FF00"
                pblist = list_items.filter(Q(elevation__level__lte=14720))
            elif counttype=="wancheng":
                response_data[counttype]["color"]="#FF9900"
                pblist = list_items.filter(Q(elevation__level__lte=26520)&Q(elevation__level__gt=14720))
            elif counttype=="weiwancheng":
                response_data[counttype]["color"]="#0000FF"
                pblist = list_items.filter(Q(elevation__level__gt=26520))
            
            response_data[counttype]["value"] = pblist.count()
            for eachpb in pblist:
                tmpPb = {}
                tmpPb["lvmdbid"] = eachpb.lvmdbid
                tmpObj["pblist"].append(tmpPb)
            response_data["pbstatuslist"].append(tmpObj)
    
        response_data["issuc"]="true"
    except Exception, e: 
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  



@login_required(login_url="/login/") 
def getunitprojectlist(request):
    response_data = {}
    try:
        response_data["unitprojectlist"]=[]
        
        unitprojectlist = UnitProject.objects.all()
        for each in unitprojectlist:
            tmpObj = {}
            tmpObj["id"] = each.id
            tmpObj["name"] = each.name
            tmpObj["modelfile"] = unicode(each.modelfile)
            response_data["unitprojectlist"].append(tmpObj)
        response_data["issuc"]="true"
        print json.dumps(response_data)
    except Exception, e: 
        print e
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@csrf_exempt
@login_required(login_url="/login/") 
def list_projecttask(request):
    if checkMobile(request):
        list_obj_weekly={}
        weekstartdate = datetime.date.today()+datetime.timedelta(0-datetime.date.today().weekday())
        weekstartend = weekstartdate + datetime.timedelta(7)
        
        grplist = Pbgroup.objects.filter(curstatustime__gt=weekstartdate,curstatustime__lt=weekstartend)
        for each in grplist:
            if list_obj_weekly.has_key(each.pbtype.major.name):
                if list_obj_weekly[each.pbtype.major.name].has_key(each.curstatus.statusname):
                    if len(list_obj_weekly[each.pbtype.major.name][each.curstatus.statusname])<5:
                        list_obj_weekly[each.pbtype.major.name][each.curstatus.statusname].append(each.number)
                else:
                    list_obj_weekly[each.pbtype.major.name][each.curstatus.statusname]=[each.number]
            else:
                list_obj_weekly[each.pbtype.major.name] = {each.curstatus.statusname:[each.number]}
        pblist = PrecastBeam.objects.filter(curstatustime__gt=weekstartdate,curstatustime__lt=weekstartend,pbtype__isprebuilt=True)
        for each in pblist:
            if list_obj_weekly.has_key(each.pbtype.major.name):
                if list_obj_weekly[each.pbtype.major.name].has_key(each.curstatus.statusname):
                    if len(list_obj_weekly[each.pbtype.major.name][each.curstatus.statusname])<5:
                        list_obj_weekly[each.pbtype.major.name][each.curstatus.statusname].append(each.number)
                else:
                    list_obj_weekly[each.pbtype.major.name][each.curstatus.statusname]=[each.number]
            else:
                list_obj_weekly[each.pbtype.major.name]={each.curstatus.statusname:[each.number]}

        list_obj_monthly={}
        curdate = datetime.date.today()
        monthstartdate = curdate +datetime.timedelta(1-curdate.day)
        monthstartend =  datetime.datetime.now()
        monthstartenddate = curdate+datetime.timedelta(0-curdate.day+calendar.monthrange(curdate.year, curdate.month)[1])
        
        grplist = Pbgroup.objects.filter(curstatustime__gte=monthstartdate,curstatustime__lte=monthstartend)
        for each in grplist:
            if list_obj_monthly.has_key(each.pbtype.major.name):
                if list_obj_monthly[each.pbtype.major.name].has_key(each.curstatus.statusname):
                    if len(list_obj_monthly[each.pbtype.major.name][each.curstatus.statusname])<5:
                        list_obj_monthly[each.pbtype.major.name][each.curstatus.statusname].append(each.number)
                else:
                    list_obj_monthly[each.pbtype.major.name][each.curstatus.statusname]=[each.number]
            else:
                list_obj_monthly[each.pbtype.major.name] = {each.curstatus.statusname:[each.number]}
        pblist = PrecastBeam.objects.filter(curstatustime__gte=monthstartdate,curstatustime__lt=monthstartend,pbtype__isprebuilt=True)
        for each in pblist:
            if list_obj_monthly.has_key(each.pbtype.major.name):
                if list_obj_monthly[each.pbtype.major.name].has_key(each.curstatus.statusname):
                    if len(list_obj_monthly[each.pbtype.major.name][each.curstatus.statusname])<5:
                        list_obj_monthly[each.pbtype.major.name][each.curstatus.statusname].append(each.number)
                else:
                    list_obj_monthly[each.pbtype.major.name][each.curstatus.statusname]=[each.number]
            else:
                list_obj_monthly[each.pbtype.major.name] = {each.curstatus.statusname:[each.number]}

        t = get_template('TaskAndFlow/list_projecttask_mobile.html')
    else:
        t = get_template('TaskAndFlow/list_projecttask.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

@csrf_exempt
@login_required(login_url="/login/") 
def query_projecttask(request):
    response_data = {}

    pid=int(request.POST.get("proid",0))
    projecttask_instance = ProjectTask.objects.get(id = pid)
    total = []
    total.append(PrecastBeam.objects.filter(task_id=pid).count())
    total.append(PrecastBeam.objects.filter(task_id=pid, curstatus__counttype_id=4).count())
    total.append(PrecastBeam.objects.filter(task_id=pid, curstatus__counttype_id__in=[1,2,3]).count())
    total.append(PrecastBeam.objects.filter(task_id=pid, curstatus__counttype=None).count())
    
    response_data["rate"] = 100 if total[0]==0 else round((total[1]*100.0)/total[0],2)
    response_data["total"]=total
    response_data["status"]=1
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")    

def view_projecttask(request, id):
    projecttask_instance = ProjectTask.objects.get(id = id)

    t=get_template('TaskAndFlow/view_projecttask.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

@login_required(login_url="/login/") 
def projecttask_statusbim(request):
    PBStatusChoices = PBStatus.objects.filter(id__gt=1)
    countTypeList = StatusCountType.objects.all()
    return render_to_response('TaskAndFlow/taskmanager/taskstatusbim.html', RequestContext(request,locals()))


@login_required(login_url="/login/") 
@check_permission
def projecttask_monthplan(request):
    title = getTitleFromUrl(request, request.get_full_path())

    canEdit = request.user.has_perm("编辑月度计划")

    list_items = MonthPlan.objects.all()

    paginator = Paginator(list_items ,20)
    listcount=len(list_items)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)
    return render_to_response('TaskAndFlow/taskmanager/monthplan.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
@check_permission
def projecttask_builddiary(request):
    title = u"施工日记"
    list_items = Constructiondiary.objects.all().order_by("-diary_date")

    timerange = request.GET.get("timerange",None)
    if not  timerange:
        d1 = datetime.date.today()
        d2 = d1 + datetime.timedelta(-30)
        timerange = d2.strftime("%Y/%m/%d")+" - "+d1.strftime("%Y/%m/%d")

    startdate, enddate = GetDateRange(timerange)
    list_items = list_items.filter(Q(diary_date__gte=startdate)&Q(diary_date__lte=enddate))
    
    paginator = Paginator(list_items ,20)
    listcount=len(list_items)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    templateName='TaskAndFlow/taskmanager/builddiary.html'
    return render_to_response(templateName, RequestContext(request,locals()))

@login_required(login_url="/login/") 
def projecttask_weekly(request):
    title="工程周报"
    weeklydir = getWeeklyDir()
    startPathHash = str(weeklydir.id)+"_dir"
    return render_to_response('TaskAndFlow/filemanager/filemanager.html', RequestContext(request,locals()))

def getWeeklyGoal(weekly_enddate):
    curWorkGoal = None
    workgoallist = Workgoal.objects.all()
    if len(workgoallist)>0:
        daycur=weekly_enddate+ datetime.timedelta(4)
        if Workgoal.objects.filter(begin_date__lt=daycur,end_date__gt=daycur).count()>0:
            curWorkGoal = Workgoal.objects.filter(begin_date__lt=daycur,end_date__gt=daycur)[0]
        else:
            curWorkGoal = workgoallist[0]
    return curWorkGoal

@csrf_exempt 
@login_required(login_url="/login/") 
def projecttask_weekly2(request):
    if request.method=='GET':
        unitprjlist = Modelfile.objects.all()
        floorList = Elevation.objects.all().order_by('id')
        weeklyid = request.GET.get("weeklyid",'')
        weekly = None
        if weeklyid:
            weekly = Weekly.objects.get(id=weeklyid)
        weekly_begindate,weekly_enddate = getWeeklyDate(weekly)

        workgoallist = Workgoal.objects.all()

        curWorkGoal = getWeeklyGoal(weekly_enddate)

        return render_to_response('TaskAndFlow/taskmanager/bulidweekly.html', RequestContext(request,locals()))
    elif request.method=='POST':
        response_data = {}
        response_data["issuc"] = 'false'
        try:
            name = request.POST.get('name', None)
            value = request.POST.get('value', '')
           
            weekly = getCurWeekly(request.user)
            
            newcontent = {}
            if weekly.content:
                newcontent = eval(weekly.content)
            newcontent[name]= value
            weekly.content=str(newcontent)
            weekly.save()
            response_data["issuc"] = 'true'
        except:
            traceback.print_exc()
        return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required(login_url="/login/") 
def projecttask_weekly2_read(request):
    weeklyid = request.GET.get("weeklyid",None)
    weekly = Weekly.objects.get(id=weeklyid)
    return render_to_response('TaskAndFlow/taskmanager/readweekly.html', RequestContext(request,locals()))

@csrf_exempt 
@login_required(login_url="/login/") 
def projecttask_weekly2_list(request):
    if request.method=='GET':
        list_items = Weekly.objects.all().order_by("-weekly_date")
        timerange = request.GET.get("timerange",'')
        if timerange:
            startdate, enddate = GetDateRange(timerange)
            list_items = list_items.filter(Q(weekly_date__gte=startdate)&Q(weekly_date__lte=enddate))
        
        paginator = Paginator(list_items ,20)
        listcount=len(list_items)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        
        try:
            list_items = paginator.page(page)
        except :
            list_items = paginator.page(paginator.num_pages)
        return render_to_response('TaskAndFlow/taskmanager/buildweeklylist.html', RequestContext(request,locals()))
    elif request.method=='POST':
        try:
            response_data["issuc"] = 'true'
        except:
            traceback.print_exc()
        return HttpResponse(json.dumps(response_data), content_type="application/json")  


@csrf_exempt 
@login_required(login_url="/login/") 
def projecttask_weekly2_data(request):
    response_data = {}
    response_data["issuc"] = 'false'
    response_data["content"] = {}
    response_data["zongbao"] = 'false'
    response_data["jianli"] = 'false'
    try:
        weeklyid = request.GET.get("weeklyid",None)
        print weeklyid
        weekly = None
        if weeklyid:
            print "11111111111111111"
            weekly = Weekly.objects.get(id=weeklyid)
            weekly_begindate,weekly_enddate = getWeeklyDate(weekly)
        else:
            weekly_begindate,weekly_enddate = getWeeklyDate()
            weekly = getCurWeekly(request.user)

        content={}        
        content = eval(weekly.content)

        if not content.has_key('xietiaoshiyiDesc'):
            weekly_begindate=datetime.datetime.strptime(weekly_begindate.strftime("%Y/%m/%d")+" 00:00:00",'%Y/%m/%d %H:%M:%S')
            weekly_enddate=datetime.datetime.strptime(weekly_enddate.strftime("%Y/%m/%d")+" 23:59:59",'%Y/%m/%d %H:%M:%S')  

            # yezhulist = [ each.id for each in  User.objects.filter(major_id=18) ]
            # zongbaolist = [ each.id for each in  User.objects.filter(major_id=11) ]

            # setjianlitmp =set([each.flowstep.template_id for each in FlowStepUser.objects.filter(user_id__in=yezhulist)])
            # setjianlitmp = list(setjianlitmp)
            
            weekly_items = projectevent.objects.filter((~Q(curdealstep=3)|(Q(curdealstep=3)&Q(updatetime__range=(weekly_begindate,weekly_enddate)))))

            issuetype = '协调事宜'
            list_items = weekly_items.filter(Q(template__flowtype__name=issuetype))
            
            xietiao=''                          
            for each in list_items:
               xietiao += each.describe+";"

            content["xietiaoshiyiDesc"]=xietiao

        if not weekly.file:
            curweekly = getCurWeekly(request.user)
            if request.user.major_id==11:
                response_data["zongbao"] = "true" if UserRoles.objects.filter(user=request.user,role_id__in=[3,4,5,15,10]).count()>0 else "false"
            if request.user.major_id==19:
                response_data["jianli"] = "true" if UserRoles.objects.filter(user=request.user,role_id__in=[3,4,5,15,10]).count()>0 else "false"
            if response_data["zongbao"]=="true" or response_data["jianli"] == "true":
                response_data["needfile"] = "true"
            if weekly.id!=curweekly.id:
                response_data["zongbao"] = "false"
                response_data["jianli"] = "false"

        response_data["issuc"] = 'true'
        response_data["content"] = content
    except:
            traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@csrf_exempt 
@login_required(login_url="/login/") 
def projecttask_weekly2_item(request):
    response_data = {}
    response_data["issuc"] = 'false'
    try:
        opr = request.POST.get('opr','')
        if opr=="getall":
            response_data["anquan"] = []
            response_data["zhiliang"] = []
            response_data["anquan_jianli"] = []
            response_data["zhiliang_jianli"] = []

            weeklyid = request.POST.get("weeklyid",None)
            weekly = None
            if weeklyid:
                weekly = Weekly.objects.get(id=weeklyid)
                weekly_begindate,weekly_enddate = getWeeklyDate(weekly)
            else:
                weekly_begindate,weekly_enddate = getWeeklyDate()
                weekly = getCurWeekly(request.user)

            content = {}
            if weekly.content:
                content = eval(weekly.content)
            deleteissue = []
            if weekly.deleteissue:
                deleteissue = eval(weekly.deleteissue)

            weekly_begindate=datetime.datetime.strptime(weekly_begindate.strftime("%Y/%m/%d")+" 00:00:00",'%Y/%m/%d %H:%M:%S')
            weekly_enddate=datetime.datetime.strptime(weekly_enddate.strftime("%Y/%m/%d")+" 23:59:59",'%Y/%m/%d %H:%M:%S')  

            yezhulist = [ each.id for each in  User.objects.filter(major_id=18) ]
            jianlilist = [ each.id for each in  User.objects.filter(major_id=19) ]
            zongbaolist = [ each.id for each in  User.objects.filter(major_id=11) ]

            setjianlitmp =set([each.flowstep.template_id for each in FlowStepUser.objects.filter(user_id__in=yezhulist)])
            setjianlitmp = list(setjianlitmp)
            
           
            print "2222222222222222222222222"
            print weekly_begindate,weekly_enddate
            weekly_items = projectevent.objects.filter(~Q(id__in=deleteissue)&Q(template_id__in=setjianlitmp)&Q(updatetime__range=(weekly_begindate,weekly_enddate)))

            issuetype = '安全问题'
            list_items = weekly_items.filter(Q(createuser_id__in=zongbaolist)&Q(template__flowtype__name=issuetype))
                                       
            for each in list_items:
                tmp = {}
                tmp["id"]=each.id
                tmp["desc"]=each.describe
                tmp["status"]=GetJianDuanFromStep(each)["jianduan"]
                tmp["readurl"]='/task/issue/readfront/'+str(each.id)+'/'
                response_data["anquan"].append(tmp)

            if content.has_key('anquan'):
                response_data["anquan"].extend(content["anquan"])

            issuetype = '质量问题'
            list_items = weekly_items.filter(Q(createuser_id__in=zongbaolist)&Q(template__flowtype__name=issuetype))
            for each in list_items:
                tmp = {}
                tmp["id"]=each.id
                tmp["desc"]=each.describe
                tmp["status"]=GetJianDuanFromStep(each)["jianduan"]
                tmp["readurl"]='/task/issue/readfront/'+str(each.id)+'/'
                response_data["zhiliang"].append(tmp)

            if content.has_key('zhiliang'):
                response_data["zhiliang"].extend(content["zhiliang"])

         
            issuetype = '安全问题'
            list_items = weekly_items.filter(Q(createuser_id__in=jianlilist)&Q(template__flowtype__name=issuetype))
            for each in list_items:
                tmp = {}
                tmp["id"]=each.id
                tmp["desc"]=each.describe
                tmp["status"]=GetJianDuanFromStep(each)["jianduan"]
                tmp["readurl"]='/task/issue/readfront/'+str(each.id)+'/'
                response_data["anquan_jianli"].append(tmp)

            if content.has_key('anquan_jianli'):
                response_data["anquan_jianli"].extend(content["anquan_jianli"])

            issuetype = '质量问题'
            list_items = weekly_items.filter(Q(createuser_id__in=jianlilist)&Q(template__flowtype__name=issuetype))
            for each in list_items:
                tmp = {}
                tmp["id"]=each.id
                tmp["desc"]=each.describe
                tmp["status"]=GetJianDuanFromStep(each)["jianduan"]
                tmp["readurl"]='/task/issue/readfront/'+str(each.id)+'/'
                response_data["zhiliang_jianli"].append(tmp)

            if content.has_key('zhiliang_jianli'):
                response_data["zhiliang_jianli"].extend(content["zhiliang_jianli"])

        elif opr=="addone":
            curtype = request.POST.get('curtype','')
            item = eval(request.POST.get('item',{}))
            weekly = getCurWeekly(request.user)
            content = eval(weekly.content)
            if content.has_key(curtype):
                content[curtype].append(item)
            else:
                content[curtype] = [item]

            weekly.content=str(content)
            weekly.save()

        elif opr=="deleteone":
            curtype = request.POST.get('curtype','')
            id = request.POST.get('id','')
            weekly = getCurWeekly(request.user)
            if "custom" in id:
                content = eval(weekly.content)
                if content.has_key(curtype):
                    for each in  content[curtype]:
                        if each["id"]==id:
                            content[curtype].remove(each)
                            break
                weekly.content=str(content)
                weekly.save()
            else:
                deleteissue = []
                if weekly.deleteissue:
                    deleteissue = eval(weekly.deleteissue)
                deleteissue.append(id)
                weekly.deleteissue=str(deleteissue)
                weekly.save()
        else:
            pass


        response_data["issuc"] = 'true'
       
    except:
            traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

def getCurGoal():
    curWorkGoal = None
    workgoallist = Workgoal.objects.all()
    if len(workgoallist)>0:
        daycur=datetime.date.today()
        if Workgoal.objects.filter(begin_date__lt=daycur,end_date__gt=daycur).count()>0:
            curWorkGoal = Workgoal.objects.filter(begin_date__lt=daycur,end_date__gt=daycur)[0]
        else:
            curWorkGoal = workgoallist[0]
    return curWorkGoal

@login_required(login_url="/login/") 
@check_permission
def projecttask_buildgoal(request):
    title = getTitleFromUrl(request, request.get_full_path())
    unitinfo=Modelfile.objects.get(isdefault=True)
    unitprjlist = Modelfile.objects.all()

    curMajorIdUser = getUserMajor(request.user)
    workgoallist = Workgoal.objects.all()

    curWorkGoal = getCurGoal()
    floorList = Elevation.objects.all().order_by('id')
    return render_to_response('TaskAndFlow/taskmanager/buildgoal.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
@check_permission
def projecttask_buildgoalmgr(request):

    majorList = UserMajor.objects.all()

    curMajorIdUser = getUserMajor(request.user)
    list_items = Workgoal.objects.all()
    listcount = len(list_items)

    curWorkGoal = getCurGoal()

    return render_to_response('TaskAndFlow/taskmanager/buildgoalmgr.html', RequestContext(request,locals()))

def getPreTask(each,pretaskidslist,typelist):
    pretaskids=Projecttaskrelation.objects.filter(suctask=each,projecttaskrelationtype__in=typelist).values_list('pretask_id',flat=True)
    pretaskidslist.extend(pretaskids)
    if (len(pretaskids)>0):
        for tmp in pretaskids:
            getPreTask(tmp,pretaskidslist,typelist)
    
    return

@csrf_exempt 
@login_required(login_url="/login/") 
@check_permission_ajax
def projecttask_savebuildgoal(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        goalname = request.POST.get('goalname', None)
        timerange = request.POST.get('timerange', None)
        goaldescribe = request.POST.get('goaldescribe', None)
        selTasks = eval(request.POST.get('selTasks', '[]'))
        
        if goalname and timerange and goaldescribe:
            startdate,enddate=GetDateRange2(timerange)
            if  Workgoal.objects.filter(begin_date=startdate,end_date=enddate).count()==0:

                goal = Workgoal.objects.create(label =goalname ,begin_date=startdate,end_date=enddate,user=request.user,description=goaldescribe)
                
                relatetaskIds=[]
                for taskid in selTasks:
                    curtaskid = taskid.split("_")[1]
                    if curtaskid not in relatetaskIds:
                        childtasklist = ProjectTask.objects.filter(Q(taskpath__contains=str(curtaskid)+"/")|Q(id=curtaskid)).values_list('id',flat=True)
                        print childtasklist
                        relatetaskIds.extend(childtasklist)
                        print relatetaskIds

                #获取前置任务
                typelist = Projecttaskrelationtype.objects.filter(name__in=["FS","FF"])
                pretasklist = []
                for each in relatetaskIds:
                    getPreTask(each,pretasklist,typelist)
                relatetaskIds.extend(pretasklist)

                #去重
                relatetaskIds = list(set(relatetaskIds))

                querysetlist=[]
                for each in relatetaskIds:
                    querysetlist.append(Finishedtasksingoal(workgoal=goal,task_id=each))        
                Finishedtasksingoal.objects.bulk_create(querysetlist)
                
                response_data["issuc"]="true"  
            else:
                response_data['error'] = u"目标重复创建！"
        else:
            response_data['error'] = u"信息不完整"

    except Exception, e: 
        print e
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@csrf_exempt 
@login_required(login_url="/login/") 
@check_permission_ajax
def projecttask_deletebuildgoal(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        goalId = request.POST.get('goalId', None)
        
        if goalId:
            Finishedtasksingoal.objects.filter(workgoal_id=int(goalId)).delete()
            goal = Workgoal.objects.get(id =int(goalId)).delete()
            response_data["issuc"]="true"  
        else:
            response_data['error'] = u"确少参数"

    except Exception, e: 
        print e
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json") 


@login_required(login_url="/login/") 
def getgoalstatus_projecttask(request):
    response_data = {}
    try:
        list_items = PrecastBeam.objects.all()
    
        curUnitId = request.GET.get('curUnitId', '')
        list_items=list_items.filter(elevation__unitproject=curUnitId)

        curMajor = request.GET.get('curMajor', '')
        print curMajor
        list_items=list_items.filter(pbtype__major=curMajor)
        

        goal = request.GET.get('goal', None)
        goal= Workgoal.objects.get(id=int(goal))
        
        projShigonglist=Finishedtasksingoal.objects.filter(workgoal=goal,task__type=1).values_list('task_id',flat=True)
        projGongxulist=Finishedtasksingoal.objects.filter(workgoal=goal,task__type=2).values_list('task_id',flat=True)
        gongxuparentlist = ProjectTask.objects.filter(id__in=projGongxulist).values_list('parentid_id',flat=True)
        projlist=[]
        projlist.extend(projShigonglist)
        projlist.extend(gongxuparentlist)

        task_list_items=list_items.filter(Q(task__in=projlist))
        
        response_data["pbstatuslist"]=[]
        
        response_data["listcount"]  = task_list_items.count()
        
        wanchenglist = []
        weiwanchenglist = []
        for each  in task_list_items:
            if each.task_id  in projShigonglist:
                if each.curstatus and (not each.curstatus.nextstatus or each.curstatus.iscritical):
                    #完成
                    wanchenglist.append(each.lvmdbid)
                else:
                    #未完成
                    weiwanchenglist.append(each.lvmdbid)
            else:#如果不在施工段任务中，说明是工序任务的父任务
                tmplist = ProjectTask.objects.filter(parentid_id=each.task_id,type=2,relatestatus__isnull=False,id__in=projGongxulist).order_by("-relatestatus_id")
                if tmplist:
                    projGX = tmplist[0]
                    if each.curstatus and (not each.curstatus.nextstatus or each.curstatus.iscritical):
                        #完成
                        wanchenglist.append(each.lvmdbid)
                    elif each.curstatus and (each.curstatus_id==projGX.relatestatus_id or each.curstatuspercent==100):
                        #完成
                        wanchenglist.append(each.lvmdbid)
                    elif each.curstatus and each.curstatus.sequence>projGX.relatestatus.sequence :
                        #完成
                        wanchenglist.append(each.lvmdbid)
                    else:
                        #未完成
                        weiwanchenglist.append(each.lvmdbid)



        countTypeList = ["wancheng","weiwancheng"]
        for counttype in countTypeList:
            tmpObj = {}
            tmpObj["name"] = counttype
            tmpObj["pblist"] = []
            response_data[counttype] = {}
            if counttype=="wancheng":
                response_data[counttype]["value"] = len(wanchenglist)
                tmpObj["pblist"]=wanchenglist
            elif counttype=="weiwancheng":
                response_data[counttype]["value"] = len(weiwanchenglist)
                tmpObj["pblist"]=weiwanchenglist

            response_data["pbstatuslist"].append(tmpObj)
    
        response_data["issuc"]="true"
    except Exception, e: 
        traceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required(login_url="/login/") 
def getgoalproperty_projecttask(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        goalId = request.GET.get('goal', None)
        
        if goalId:
            goal = Workgoal.objects.get(id =int(goalId))
            response_data["name"]=goal.label
            response_data["timerange"]=goal.begin_date.strftime("%Y/%m/%d")+"-"+goal.end_date.strftime("%Y/%m/%d")
            response_data["description"]=goal.description
            response_data["issuc"]="true"  
        else:
            response_data['error'] = u"确少参数"

    except Exception, e: 
        print e
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@csrf_exempt
@login_required(login_url="/login/") 
def projecttask_updatetaskplan(request):
    response_data={}
    response_data["issuc"]="false"
    try:
        version=request.POST.get('version', '')
        updatetag=request.POST.get('updatetag', 1)
        describe=request.POST.get('describe', 1)
        docs = eval(request.POST.get('docs', '[]'))
        qianzhengdocs = eval(request.POST.get('qianzhengdocs', '[]'))  # 关联元素

        savedir=None
        try:
            savedir = Directory.objects.get(name="施工计划",islock=True)
        except:
            savedir=None

        prjversion = Projectversion.objects.create(version_code=version,label=updatetag,update_user=request.user,description=describe)
        Projectupdatefiles_list_to_insert = []
        for FileId in docs:
            docId = int(FileId)
            Projectupdatefiles_list_to_insert.append(Projectupdatefiles(projectversion=prjversion, file_id=docId))

            doc = Document.objects.get(id=docId)
            if savedir:
                doc.docdirectory.add(savedir)
                movefiletoDir(doc,savedir)

        for FileId in qianzhengdocs:
            docId = int(FileId)
            Projectupdatefiles_list_to_insert.append(Projectupdatefiles(projectversion=prjversion, file_id=docId))

            doc = Document.objects.get(id=docId)
            if savedir:
                doc.docdirectory.add(savedir)
                movefiletoDir(doc,savedir)

        Projectupdatefiles.objects.bulk_create(Projectupdatefiles_list_to_insert)

        response_data["issuc"]="true"

    except:
        traceback.print_exc()
        response_data["error"] = "保存失败！"
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt 
@login_required(login_url="/login/")
@check_permission_ajax
def monthplan_save(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        monthplan_desc = request.POST.get('monthplan_desc', None)
        create_date = request.POST.get('create_date', None)
        docs = eval(request.POST.get('docs', None))
        create_date = create_date+"-01"

        builddiary = MonthPlan.objects.create(month_date =create_date ,desc=monthplan_desc,user=request.user,file_id=int(docs[0]))
        response_data["issuc"]="true"

    except: 
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json") 


@login_required(login_url="/login/")
def projecttask_lurujindu(request):
    title = getTitleFromUrl(request, "/task/projecttask/lurujindu/")
    majorList = UserMajor.objects.all()
    curMajorId = getUserMajor(request.user)

    havesheshi,havejixie,haverenwu = checkMonitorType()

    canChangeTime = request.user.has_perm("自定义扫码时间")

    acc = None
    if request.GET.get("gxid",None):
        acc = Acceptance.objects.get(id=request.GET.get("gxid",None))
        accdesc = GetRelateTypeInfo(acc.monitoring.typetable, acc.monitoring.relatedid)

    return render_to_response('TaskAndFlow/taskmanager/lurujindu.html', RequestContext(request,locals()))



@login_required(login_url="/login/") 
def projecttask_count(request):
    MajorList = getMajorList()
    major = Modelfile.objects.get(isdefault=True).relatedmajor_id
    return render_to_response('TaskAndFlow/statistical/progress_count.html', RequestContext(request,locals()))
