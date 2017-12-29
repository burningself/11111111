# -*- coding: utf-8 -*-
'''

@author: pgb
'''
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from TaskAndFlow.utility import *
from TaskAndFlow.utility_flowtemplate import *
from UserAndPrj.models import *
from TaskAndFlow.models import *
from TaskAndFlow.forms import *
from django.db.models import Q
from Scc4PM.settings import CURRENT_PROJECT_ID
from UserPrjConfig.permissions import *
# Create your views here.


@login_required(login_url="/login/")  
def index_view_vue(request):
    return render_to_response('version2/index.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def login_vue(request):
    return render_to_response('version2/login_vue.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def index_view_vue_model(request):
    return render_to_response('version2/general_model.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def index_view_vue_table(request):
    return render_to_response('version2/general_table.html', RequestContext(request,locals()))

@check_permission
@login_required(login_url="/login/")  
def addressList_vue(request):
    return render_to_response('AboutUs/addressList.html', RequestContext(request,locals()))


@login_required(login_url="/login/")  
def index_view(request):

    isMobile = checkMobile(request)    
    if isMobile:
        try:
            PersonInfo = eval(CustomInfo.objects.get(infotype="mobile_general_cfg").custominfo)["PersonInfo"]
        except Exception as e:
            PersonInfo = False
        return render_to_response('common/general_mobile.html', RequestContext(request,locals()))
    else:
        nextpage = '/index_vue/model/'
        try:
            nextpage = Projectmenu.objects.get(name="项目概览").url
        except:
            nextpage = Projectmenu.objects.all()[0].url
        
        return HttpResponseRedirect(nextpage)


@csrf_exempt
@login_required(login_url="/login/")  
def index_data(request):
    response_data={}
    try:
        reqType = request.POST.get("reqType") 
        keyword = request.POST.get("keyword")
        duration = int(request.POST.get("duration",6))
        chooseDate = request.POST.get("chooseDate","")
        
        if reqType=='line':
            monthCountList=[]
            weekCountList=[]
            index = 0
            daycur=datetime.date.today()
            day = calendar.monthrange(daycur.year,daycur.month)[1]
            daycur=daycur.replace(day=day)
            while (index < duration):
                mountcount={}
                dateStart=del_months(daycur,duration-index)
                dateEnd=del_months(daycur,duration-1-index)
                mountcount["date"]=dateEnd.strftime("%Y-%m")
                
                dateStart = datetime.datetime.strptime(str(dateStart),'%Y-%m-%d')
                dateEnd = datetime.datetime.strptime(str(dateEnd),'%Y-%m-%d')
                
                projlist = ProjectTask.objects.filter(Q(planstart__lt=dateEnd)&Q(planfinish__gte=dateStart))
                plan_list_items_count=0
                for each in projlist:
                    if (dateStart - each.planstart).days >= 0:
                        daysInRange = (dateEnd - dateStart).days if each.planfinish > dateEnd else (each.planfinish-dateStart).days
                    
                    else:
                        daysInRange = (dateEnd - each.planstart).days if each.planfinish > dateEnd else (each.planfinish-each.planstart).days+1
                    
                    if keyword:
                        pbInCount =  PrecastBeam.objects.filter(task_id=each.id, pbtype=keyword).count() * daysInRange / ((each.planfinish-each.planstart).days+1)
                    else:
                        pbInCount =  PrecastBeam.objects.filter(task_id=each.id).count() * daysInRange / ((each.planfinish-each.planstart).days+1)
                        
                    plan_list_items_count += pbInCount
                    
                anzhuang_list_items = PrecastBeam.objects.filter(curstatus__nextstatus__isnull=True, curstatustime__gt=dateStart, curstatustime__lte=dateEnd)
                
                if keyword:
                    anzhuang_list_items = anzhuang_list_items.filter(precastbeam__pbtype=keyword)

                mountcount["jihua"]= plan_list_items_count
                mountcount["anzhuang"]= anzhuang_list_items.count() 
                
                monthCountList.append(mountcount)
                index=index+1
            
            index=0
            if chooseDate and chooseDate!="":
                daycur=datetime.datetime.strptime(chooseDate,'%Y/%m/%d').date()
            else:
                daycur=datetime.date.today()
            #print daycur
            weekdaycur = daycur.weekday()
            
            # countTypeList = StatusCountType.objects.all()
            # response_data['weekCountTypeList'] = []
            # for counttype in countTypeList:
            #     tmpObj = {}
            #     tmpObj["key"] = counttype.id
            #     tmpObj["name"] = counttype.name
            #     tmpObj["color"] = counttype.rendercolor
            #     response_data['weekCountTypeList'].append(tmpObj)
            
            while (index < 7):   
                mountcount={}
                startTime = datetime.datetime.strptime(str( get_date_of_day(daycur,index-weekdaycur) ) + " 00:00:01",'%Y-%m-%d %H:%M:%S')
                endTime = datetime.datetime.strptime(str( get_date_of_day(daycur,index-weekdaycur) ) + " 23:59:59",'%Y-%m-%d %H:%M:%S')
                mountcount["date"]=endTime.strftime("%m-%d")
                
                mountcount["anzhuang"] = PrecastBeam.objects.filter(curstatus__nextstatus__isnull=True, curstatustime__gt=startTime, 
                                                                    curstatustime__lte=endTime).count()
                    
                weekCountList.append(mountcount)
                index=index+1
            
            response_data['weekCountList']=weekCountList
            response_data['monthCountList']=monthCountList
            response_data['status']='Succeed'
        
        elif reqType=='bar':
            zhiliangCountList=[]
            anquanCountList=[]
            index=0
            daycur=datetime.date.today()
            weekdaycur = daycur.weekday()
            
            while (index < duration):
                zhiliangMountcount={}
                anquanMountcount={}
                mountcount={}
    
                dateStart=datetime.datetime.strptime(str( get_day_of_day(-1-weekdaycur-(duration-index-1)*7) ) + " 00:00:01",'%Y-%m-%d %H:%M:%S')
                dateEnd=datetime.datetime.strptime(str( get_day_of_day(6-weekdaycur-(duration-index-1)*7) ) + " 23:59:59",'%Y-%m-%d %H:%M:%S')
                zhiliangMountcount["date"]=dateEnd.strftime("%m-%d")
                zhiliangMountcount["chulizhong"]=Eventstep.objects.filter(flowstep__isendstep=0, projectevent__template__flowtype__name="质量问题", starttime__gt=dateStart, starttime__lte=dateEnd).values("projectevent").distinct().count() 
                zhiliangMountcount["wancheng"]=Eventstep.objects.filter(flowstep__isendstep=1, projectevent__template__flowtype__name="质量问题",starttime__gt=dateStart, starttime__lte=dateEnd).values("projectevent").distinct().count() 
                
                anquanMountcount["date"]=dateEnd.strftime("%m-%d")
                anquanMountcount["chulizhong"]=Eventstep.objects.filter(flowstep__isendstep=0,projectevent__template__flowtype__name="安全问题", starttime__gt=dateStart, starttime__lte=dateEnd).values("projectevent").distinct().count() 
                anquanMountcount["wancheng"]=Eventstep.objects.filter(flowstep__isendstep=1,projectevent__template__flowtype__name="安全问题", starttime__gt=dateStart, starttime__lte=dateEnd).values("projectevent").distinct().count() 
               
                zhiliangCountList.append(zhiliangMountcount)
                anquanCountList.append(anquanMountcount)
                index=index+1
            
            response_data['zhiliangCountList']=zhiliangCountList
            response_data['anquanCountList']=anquanCountList
            response_data['status']='Succeed'
        
        elif reqType=='eventlist':
            faqi =projectevent.objects.filter(template__flowtype__name="质量问题",curflowstep__isstartstep=1).count()
            chuli=projectevent.objects.filter(template__flowtype__name="质量问题",curflowstep__sequence__gte=1).count()
            
            response_data["zhiliang_faqi"] = str(faqi)+"/"+str(faqi+chuli)
            response_data["zhiliang_chuli"]  = str(chuli)+"/"+str(faqi+chuli)
            response_data["anquan_faqi"]=projectevent.objects.filter(template__flowtype__name="安全问题", curflowstep__isstartstep=1).count()
            response_data["anquan_chuli"]=projectevent.objects.filter(template__flowtype__name="安全问题", curflowstep__sequence__gte=1).count()
            
            response_data['status']='Succeed'
            
        elif reqType=="donut-task":
            categorys=[{'description':'任务状态统计'},{'description':'任务类别统计'}]
            for each in categorys:
                each["data"] = []
                if each["description"] == '任务状态统计':
                    for eachStatus in TaskStatus.objects.all():
                        tmpObj={}
                        tmpObj['label']=eachStatus.statusname+"状态比例"
                        tmpObj['value']=round(ProjectTask.objects.filter(curstatus=eachStatus).count()*100.0/ProjectTask.objects.all().count(), 1)
                        each["data"].append(tmpObj)
                        
                elif each["description"] == '任务类别统计':
                    for eachType in TaskType.objects.all():
                        tmpObj={}
                        tmpObj['label']=eachType.name+"类别比例"
                        tmpObj['value']=round(ProjectTask.objects.filter(type=eachType).count()*100.0/ProjectTask.objects.all().count(), 1)
                        each["data"].append(tmpObj)
            
            response_data['categorys'] = categorys
            response_data['status']='Succeed'
            
        elif reqType=="donut-area":    
            categorys= []
            for each in FactoryArea.objects.all().values():
                qiyong=PrecastBeam.objects.filter(curfactoryposition__in=FactoryPosition.objects.filter(areaowner=each["id"])).count()
                if each['total']==None or each['total']==0 :
                    total=100
                else:
                    total=each['total']
                weiqiyong=total-qiyong
                
                each["data"] = [{'label':'已启用堆场比例', 'value': round(qiyong*100.0/total,1)},
                                {'label':'未启用堆场比例', 'value': round(weiqiyong*100.0/total,1)}]
                categorys.append(each)
            response_data['categorys'] = categorys
            response_data['status']='Succeed'
            
        elif reqType=="donut-pb":    
            categorys=[{'description':'构件进场比例'},{'description':'构件完成比例'}]
            jinchang_count = PrecastBeam.objects.filter(curstatus__roughcounttype_id__gte=3).count()
            weijinchang_count = PrecastBeam.objects.all().exclude(curstatus__roughcounttype_id__gte=3).count()
            
            total= 100 if (jinchang_count+weijinchang_count)==0 else jinchang_count+weijinchang_count
            weijinchang_rate= round(weijinchang_count*1000/total/10.0,1)
            jinchang_rate=round(100-weijinchang_rate,1)
            categorys[0]["data"] = [{'label':'已进场构件比例', 'value': jinchang_rate},
                                {'label':'未进场构件比例', 'value': weijinchang_rate}]
            
            yianzhuang_count=PrecastBeam.objects.filter(curstatus__roughcounttype_id__gte=4).count()
            weianzhuang_count=PrecastBeam.objects.all().exclude(curstatus__roughcounttype_id__gte=4).count()
            total= 100 if (yianzhuang_count+weianzhuang_count)==0 else yianzhuang_count+weianzhuang_count
            weijinchang_rate=round(weianzhuang_count*100.0/total,1)
            yijinchang_rate=round(100-weijinchang_rate,1)
            categorys[1]["data"] = [{'label':'已安装构件比例', 'value': yijinchang_rate},
                                {'label':'未安装构件比例', 'value':weijinchang_rate } ]
            response_data['categorys'] = categorys
            response_data['status']='Succeed'
    except Exception, e: 
        print traceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["status"]="failed"
    return HttpResponse(json.dumps(response_data), content_type="application/json")     

@csrf_exempt
@login_required(login_url="/login/")  
def index_table(request):
    try:
        response_data={}
        list_items=[]
        dataType = int(request.POST.get("type"))
        if dataType == 0:
            '''factoryArea section'''
            if checkMobile(request):
                list_items_head=('场区',"构件数量","空间占用比","堆场数量")
            else:
                list_items_head=('','场区',"构件数量","空间占用比","堆场数量")
            sortKey="场区"
            list_items_set = FactoryArea.objects.all().values()
            for each in list_items_set:
                tmpObj={}
                pslist=FactoryPosition.objects.filter(areaowner_id=each["id"]).values()
                tmpObj["场区"]=each["description"]
                tmpObj["堆场数量"]=pslist.count()
                sumPb=0
                for eachPosition in pslist:
                    eachPosition["count"]=PrecastBeam.objects.filter(curfactoryposition_id=eachPosition["id"]).count()
                    sumPb+=eachPosition["count"]
                
                tmpObj["构件数量"]=sumPb
                if each["total"]:
                    tmpObj["空间占用比"]=str(round(sumPb*100.0/each["total"],1))+" %"
                else:
                    tmpObj["空间占用比"]=str(round(sumPb*100.0/100,1)) + " %"
                list_items.append(tmpObj)
                
        elif dataType ==1 :
            '''Jishu section'''
            list_items_head=('','名称',"负责人","预计完成","当前状态","重大危险源")
            sortKey="当前状态"
            list_items_set = FactoryArea.objects.all().values()
            for each in list_items_set:
                tmpObj={}
                tmpObj["名称"]="技术方案一"
                tmpObj["负责人"]="测试者"
                tmpObj["预计完成"]="MKZ2015"
                tmpObj["当前状态"]="加工中"
                tmpObj["重大危险源"]="MKZ2015"
                
                list_items.append(tmpObj)
        
        elif dataType ==2 :
            '''zhiliang section'''
            list_items_head=('','专业','已关闭','未关闭')
            sortKey="未处理"
            # list_items_set = projectevent.objects.filter(template__flowtype__name="质量问题")[:5]
            allmajor =  UserMajor.objects.all()
            zjy = 0
            zjw = 0
            for mj in allmajor:
                tmpObj={}
                tmpObj["专业"]= mj.name
                tmpObj["已处理"] = 0
                tmpObj["未处理"] = 0
                zymj = projectevent.objects.filter(template__flowtype__name="质量问题",template__major=mj,issave=False)
                for each in zymj:
                    # tmpObj={}
                    # tmpObj["专业"]= each.template.major.name
                    if each.curflowstep.isendstep:
                        tmpObj["已处理"] += 1
                        zjy +=1
                    else:
                        tmpObj["未处理"] += 1
                        zjw +=1
                list_items.append(tmpObj)
            tmpObj={}
            tmpObj["专业"]= "总计"
            tmpObj["已处理"] = zjy
            tmpObj["未处理"] = zjw
            list_items.append(tmpObj)
        elif dataType ==3 :
            '''anquan section'''
            list_items_head=('','专业','已关闭','未关闭')
            sortKey="未处理"
            # list_items_set = projectevent.objects.filter(template__flowtype__name="质量问题")[:5]
            allmajor =  UserMajor.objects.all()
            zjy = 0
            zjw = 0
            for mj in allmajor:
                tmpObj={}
                tmpObj["专业"]= mj.name
                tmpObj["已处理"] = 0
                tmpObj["未处理"] = 0
                zymj = projectevent.objects.filter(template__flowtype__name="安全问题",template__major=mj,issave=False)
                for each in zymj:
                    # tmpObj={}
                    # tmpObj["专业"]= each.template.major.name
                    if each.curflowstep.isendstep:
                        tmpObj["已处理"] += 1
                        zjy +=1
                    else:
                        tmpObj["未处理"] += 1
                        zjw +=1
                list_items.append(tmpObj)
            tmpObj={}
            tmpObj["专业"]= "总计"
            tmpObj["已处理"] = zjy
            tmpObj["未处理"] = zjw
            list_items.append(tmpObj)
        
        
        # list_items = sorted(list_items, key=lambda x : x[sortKey], reverse=True)  
        response_data["list_items"]=list_items
        response_data["list_items_head"]=list_items_head
        response_data['status']='Succeed'
    except:
        traceback.print_exc()
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")     

def progress_schedule(request):
    isMobile = checkMobile(request)
    if isMobile:
        return render_to_response('TaskAndFlow/progress_schedule_mobile.html', RequestContext(request,locals()))
    else:
        return render_to_response('TaskAndFlow/progress_schedule.html', RequestContext(request,locals()))

def progress_projecttask(request):
    isMobile = checkMobile(request)
    if isMobile:
        return render_to_response('TaskAndFlow/progress_projecttask_mobile.html', RequestContext(request,locals()))
    else:
        return render_to_response('TaskAndFlow/progress_projecttask.html', RequestContext(request,locals()))

def progress_cangchu(request):
    isMobile = checkMobile(request)
    if isMobile:
        return render_to_response('TaskAndFlow/progress_cangchu_mobile.html', RequestContext(request,locals()))
    else:
        return render_to_response('TaskAndFlow/progress_cangchu.html', RequestContext(request,locals()))



@login_required(login_url="/login/")    
def progress_goujian(request):
    havesheshi,havejixie,haverenwu = checkMonitorType()
    isMobile = checkMobile(request)
    list_types=['构件']
    if havesheshi:
        list_types.append('安全设施')
    if havejixie:
        list_types.append('施工机械')
    if haverenwu:
        list_types.append('任务')
    
    unitProjectList = UnitProject.objects.all()
    if unitProjectList:
        Elevationlist = Elevation.objects.filter(unitproject_id=unitProjectList[0].id)
    MajorList = getMajorList()

    statusIdlist =set([each.curstatus_id for each in PrecastBeam.objects.filter(curstatus__isnull=False)])
    statuslist = PBStatus.objects.filter(id__in=statusIdlist)
    
    if isMobile:
        return render_to_response('TaskAndFlow/progress_goujian_mobile.html', RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/")  
def progress_goujian_load_table(request):
    try:
        response_data={'status':1}
        filterKey=request.POST.get("filterCode",'')
        unitProject=int(request.POST.get("unitProject",0))
        pbelevation=eval(request.POST.get("pbelevation",'[]'))
        pbmajor=int(request.POST.get("pbmajor",0))
        pbstatus=eval(request.POST.get("pbstatus",'[]'))
        page=int(request.POST.get("page",1))
        
        
        list_items=[]
        list_items_set = []
        list_items_head=[]
        list_items_totalpage=[]
        titles=[]
        index=0
        
        PAGENUM = 30
        startindex = PAGENUM*(page-1)
        totalpage = 1
        
        dataTableList = ['goujian']
        for each in dataTableList:
            list_items.append([])
            list_items_head.append([])
            list_items_totalpage.append([])
            list_items_head[index]=('编号',"类型","状态")
            sortKey="状态"
            
            if filterKey=='构件':
                titles.append("构件验收查看")
                list_items_set = PrecastBeam.objects.filter(curstatus__isnull=False)
                if unitProject !=0:
                    list_items_set = list_items_set.filter(elevation__unitproject_id=unitProject)
                if pbelevation:
                    list_items_set = list_items_set.filter(elevation_id__in=pbelevation)
                if pbmajor!=0:
                    list_items_set = list_items_set.filter(pbtype__major_id=pbmajor)
                if pbstatus:
                    list_items_set = list_items_set.filter(curstatus_id__in=pbstatus)

                list_items_set = filterMonitorType(list_items_set, "构件")
                    
                totalpage = len(list_items_set)/PAGENUM+1
                list_items_totalpage[index] = totalpage
                list_items_set = list_items_set[startindex:startindex+PAGENUM]

                for each in list_items_set:
                    tmpObj={}
                    tmpObj["id"]=each.id
                    tmpObj["编号"]=each.drawnumber
                    tmpObj["类型"]=each.pbtype.name
                    tmpObj["状态"]=each.curstatus.statusname
                    list_items[index].append(tmpObj)
            elif filterKey=='安全设施':
                titles.append("安全设施验收查看")
                majors = UserMajor.objects.filter(name="安全设施")
                if majors:
                    anquanMajor = majors[0]
                    list_items_set = PrecastBeam.objects.filter(curstatus__isnull=False,pbtype__major_id=anquanMajor.id)
                    if unitProject !=0:
                        list_items_set = list_items_set.filter(elevation__unitproject_id=unitProject)
                    if pbelevation:
                        list_items_set = list_items_set.filter(elevation_id__in=pbelevation)
                    if pbmajor!=0:
                        list_items_set = list_items_set.filter(pbtype__major_id=pbmajor)
                    if pbstatus:
                        list_items_set = list_items_set.filter(curstatus_id__in=pbstatus)
     
                        
                    totalpage = list_items_set.count()/PAGENUM+1
                    list_items_totalpage[index] = totalpage
                    list_items_set = list_items_set[startindex:startindex+PAGENUM]

                    for each in list_items_set:
                        tmpObj={}
                        tmpObj["id"]=each.id
                        tmpObj["编号"]=each.drawnumber
                        tmpObj["类型"]=each.pbtype.name
                        tmpObj["状态"]=each.curstatus.statusname
                        list_items[index].append(tmpObj)
            elif filterKey=='施工机械':
                titles.append("施工机械验收查看")
                pass
            elif filterKey=='任务':
                titles.append("任务验收查看")
                pass
            else:
                pass

            
            list_items[index] = sorted(list_items[index], key=lambda x : x[sortKey], reverse=True)      
            index+=1
        
        response_data["titles"]=titles
        response_data["list_items"]=list_items
        response_data["list_items_totalpage"]=list_items_totalpage
        response_data["list_items_head"]=list_items_head
    except:
        traceback.print_exc()    
        response_data['status']=0
        response_data['error']="数据读取出错！"
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@csrf_exempt
@login_required(login_url="/login/")  
def progress_goujian_load_count(request):
    try:
        response_data={'status':1}
        filterKey=request.POST.get("filterCode",'')
        unitProject=int(request.POST.get("unitProject",0))
        pbelevation=eval(request.POST.get("pbelevation",'[]'))
        pbmajor=int(request.POST.get("pbmajor",0))
        pbstatus=eval(request.POST.get("pbstatus",'[]'))

        if filterKey=='构件':
            list_items_set = PrecastBeam.objects.filter(curstatus__isnull=False)
            if unitProject !=0:
                list_items_set = list_items_set.filter(elevation__unitproject_id=unitProject)
            if pbelevation:
                list_items_set = list_items_set.filter(elevation_id__in=pbelevation)
            if pbmajor!=0:
                list_items_set = list_items_set.filter(pbtype__major_id=pbmajor)

            list_items_set = filterMonitorType(list_items_set, "构件")

        elif filterKey=='安全设施':
            majors = UserMajor.objects.filter(name="安全设施")
            if majors:
                anquanMajor = majors[0]
                list_items_set = PrecastBeam.objects.filter(curstatus__isnull=False,pbtype__major_id=anquanMajor.id)
                if unitProject !=0:
                    list_items_set = list_items_set.filter(elevation__unitproject_id=unitProject)
                if pbelevation:
                    list_items_set = list_items_set.filter(elevation_id__in=pbelevation)
                if pbmajor!=0:
                    list_items_set = list_items_set.filter(pbtype__major_id=pbmajor)
              
        elif filterKey=='施工机械':
            titles.append("施工机械验收查看")
            pass
        elif filterKey=='任务':
            titles.append("任务验收查看")
            pass
        else:
            pass

        filterpbIdlist = [each.id for each in list_items_set]

        list_items = PBStatusRecord.objects.filter(precastbeam_id__in=filterpbIdlist)

        if not pbstatus:
            pbstatus = list_items.values('status_id').distinct().values_list('status_id', flat=True)

        countinfolist = []
        prj =  UnitProject.objects.get(id=unitProject)
        if pbelevation:
            for ele in pbelevation:
                elevation = Elevation.objects.get(id=ele)
                pbitems = PrecastBeam.objects.filter(elevation_id__in=pbelevation)
                if pbmajor!=0:
                    pbitems = pbitems.filter(pbtype__major_id=pbmajor)
                totalcount = len(filterMonitorType(pbitems, "构件"))
                countinfobase = prj.name+"  "+elevation.name+"  "
                for sta in pbstatus:
                    tmpinfo = countinfobase
                    status = PBStatus.objects.get(id = sta)
                    stacount = list_items.filter(precastbeam__elevation_id=ele,status_id=sta).count()
                    tmpinfo+="%s_%s:%d/%d" % (status.pbtype.name,status.statusname,stacount,totalcount)
                    countinfolist.append(tmpinfo)

        else:
            pbitems = PrecastBeam.objects.filter(elevation__unitproject_id=unitProject)
            if pbmajor!=0:
                pbitems = pbitems.filter(pbtype__major_id=pbmajor)
            totalcount = len(filterMonitorType(pbitems, "构件"))
            countinfobase = prj.name+"  "
            for sta in pbstatus:
                tmpinfo = countinfobase
                status = PBStatus.objects.get(id = sta)
                stacount = list_items.filter(status_id=sta).count()
                tmpinfo+="%s_%s:%d/%d" % (status.pbtype.name,status.statusname,stacount,totalcount)
                countinfolist.append(tmpinfo)
            
        
        # list_items.query.group_by = ['precastbeam_id']

        # pbidlist = list_items.values_list('precastbeam_id', flat=True)
        # pbidlist = list(pbidlist)
        # mappblvmid = { each.id: each.lvmdbid for each in PrecastBeam.objects.filter(id__in=pbidlist) }
        # mapstatuscolor = { each.id: each.detailcounttype.rendercolor if each.detailcounttype else ""   for each in PBStatus.objects.all() }

        # mapid2obj={}
        # for each in list_items:
        #     tmpObj = {}
        #     tmpObj["lvmdbid"] = mappblvmid[each.precastbeam_id]
        #     tmpObj["color"] = mapstatuscolor[each.status_id]
        #     mapid2obj[each.precastbeam_id]=tmpObj
        response_data["countinfolist"]=countinfolist

    except:
        traceback.print_exc()    
        response_data['status']=0
        response_data['error']="数据读取出错！"
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
@login_required(login_url="/login/")  
def progress_goujian_load_elevation(request):
    try:
        elevationList=[]
        response_data={'status':1}
        unitProject=int(request.POST.get("unitProject",0))
        for each in Elevation.objects.filter(unitproject_id=unitProject):
            tmpObj = {}
            tmpObj["id"] = each.id
            tmpObj["name"] = each.name
            elevationList.append(tmpObj)
        
        response_data['elevationList']=elevationList
    except:
        traceback.print_exc()    
        response_data['status']=0
        response_data['error']="数据读取出错！"
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


@csrf_exempt
@login_required(login_url="/login/")    
def progress_goujian_count(request):
    if request.method=='GET':
        isMobile = checkMobile(request)
        MajorList = getMajorList()

        if isMobile:
            return render_to_response('TaskAndFlow/statistical/progress_count_mobile.html', RequestContext(request,locals()))
    else:
        try:
            response_data={'status':1}
            try:
                unitProject=int(request.POST.get("unitProject",''))
            except:
                unitProject=Modelfile.objects.get(isdefault=True).relatedunitproject_id
            print unitProject
            try:
                pbmajor=int(request.POST.get("filterCode",''))
            except:
                pbmajor = Modelfile.objects.get(isdefault=True).relatedmajor_id
            print pbmajor

            pbelevation=int(request.POST.get("pbelevation",0))

            countlist = ["type"]
            counttypelist = PBStatus.objects.filter(pbtype__major_id=pbmajor,detailcounttype__isnull=False).values('detailcounttype_id').distinct().values_list('detailcounttype_id', flat=True)
            countlist.extend(StatusCountType.objects.filter(id__in=counttypelist).order_by('sequence').values_list('id', flat=True))
            print countlist
            countrowlist = ["title","单位工程","楼层"]
            countrowlist.extend(PBType.objects.filter(major_id=pbmajor))
            print countrowlist
            progresscountlist = []

            setpb =([each.relatedid for each in Monitoringelement.objects.filter(typetable="构件")])
            list_items_total = PrecastBeam.objects.filter(pbtype__major_id=pbmajor,elevation__unitproject_id=unitProject,id__in=list(setpb))
            filterpbIdlist = [each.id for each in list_items_total]


            if pbelevation!=0:
                totalelevation = list_items_total.filter(elevation_id=pbelevation)
                elevationpbIdlist = [each.id for each in totalelevation]
            else:
                totalelevation = list_items_total
                elevationpbIdlist = filterpbIdlist

            for row in countrowlist:
                tmplist = []
                for each in countlist:
                    if each=="type":
                        if row=="title":
                            tmplist.append("进度状态")
                        elif row=="单位工程":
                             tmplist.append("单位工程")
                        elif row=="楼层":
                             tmplist.append("楼层")
                        else:
                            tmplist.append(row.name)
                    else:
                        if row=="title":
                            tmplist.append(StatusCountType.objects.get(id=each).name)
                        elif row=="单位工程":
                            precent = 0
                            if len(filterpbIdlist)!=0:
                                precent = round(PBStatusRecord.objects.filter(precastbeam_id__in=filterpbIdlist,status__detailcounttype_id=each,isactive=True).count()/float(len(filterpbIdlist))*100,2)
                            tmplist.append("%.2f%%" % precent)
                        elif row=="楼层":
                            precent = 0
                            if len(elevationpbIdlist)!=0:
                                precent = round(PBStatusRecord.objects.filter(precastbeam_id__in=elevationpbIdlist,status__detailcounttype_id=each,isactive=True).count()/float(len(elevationpbIdlist))*100,2)
                            tmplist.append("%.2f%%" % precent)
                        else:
                            countmptotal = totalelevation.filter(pbtype_id=row.id).count()
                            countmp = PBStatusRecord.objects.filter(status__detailcounttype_id=each,precastbeam__pbtype_id=row.id,precastbeam_id__in=elevationpbIdlist,isactive=True).count()
                            tmplist.append(("%d/%d") % (countmp,countmptotal))
                progresscountlist.append(tmplist)
                
            response_data["countinfolist"]=progresscountlist
            response_data["unitProject"]=unitProject
            response_data["pbelevation"]=pbelevation

        except:
            traceback.print_exc()    
            response_data['status']=0
            response_data['error']="数据读取出错！"
    
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")  
def jishu_list(request):
    isMobile = checkMobile(request)
    
    if isMobile:
        return render_to_response('TaskAndFlow/jishu_list_mobile.html', RequestContext(request,locals()))
    else:
        return render_to_response('TaskAndFlow/jishu_list.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def jishu_create(request):
    return render_to_response('TaskAndFlow/jishu.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def jishu_read(request):
    return render_to_response('TaskAndFlow/jishu.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def jishu_update(request):
    return render_to_response('TaskAndFlow/jishu.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def jishu_del(request):
    return render_to_response('TaskAndFlow/jishu.html', RequestContext(request,locals()))






@login_required(login_url="/login/") 
def zhiliang_del(request):
    return render_to_response('TaskAndFlow/jishu.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def anquan_read(request):
    return render_to_response('TaskAndFlow/anquan_list.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def anquan_update(request):
    return render_to_response('TaskAndFlow/anquan_list.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def anquan_del(request):
    return render_to_response('TaskAndFlow/anquan_list.html', RequestContext(request,locals()))

# Cailiao
@login_required(login_url="/login/")  
def cailiao_list(request):
    return render_to_response('TaskAndFlow/cailiao_list.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def cailiao_create(request):
    return render_to_response('TaskAndFlow/cailiao_list.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def cailiao_read(request):
    return render_to_response('TaskAndFlow/cailiao_list.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def cailiao_update(request):
    return render_to_response('TaskAndFlow/cailiao_list.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def cailiao_del(request):
    return render_to_response('TaskAndFlow/cailiao_list.html', RequestContext(request,locals()))


# #biaodan
# @login_required(login_url="/login/")  
# def biaodan_manerger(request):
#     return render_to_response('TaskAndFlow/biaodan_manerger.html', RequestContext(request,locals()))
    

def create_factoryarea(request):
    form = FactoryAreaForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = FactoryAreaForm()

    t = get_template('TaskAndFlow/create_factoryarea.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


@login_required(login_url="/login/") 
def list_factoryarea(request):
  
    list_items_area = FactoryArea.objects.all().values()
    for each in list_items_area:
        each["positions"]=FactoryPosition.objects.filter(areaowner_id=each["id"]).values()
        sum=0
        for eachPosition in each["positions"]:
            eachPosition["count"]=PrecastBeam.objects.filter(curfactoryposition_id=eachPosition["id"]).count()
            sum+=eachPosition["count"]
        
        if each["total"]:
            each["used_rate"]=round(sum*100.0/each["total"],1) if round(sum*100.0/each["total"],1)<=100 else 100
        else:
            each["used_rate"]=round(sum*100.0/100,1) if round(sum*100.0/each["total"],1)<=100 else 100
        
    paginator = Paginator(list_items_area ,6)
    
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)
        
    if checkMobile(request):
        t = get_template('TaskAndFlow/list_factoryarea_mobile.html')
    else:
        t = get_template('TaskAndFlow/list_factoryarea.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

def view_factoryarea(request, id):
    factoryarea_instance = FactoryArea.objects.get(id = id)

    t=get_template('TaskAndFlow/view_factoryarea.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

@csrf_exempt
@login_required(login_url="/login/")  
def factoryarea_pblist(request):
    try:
        response_data={}
        pbList=[]
        if checkMobile(request):
            response_data["headerList"] = ["构件编号","类型","积压天数"]
        else:
            response_data["headerList"] = ["构件编号","类型","进场时间","积压天数","占用面积"]
        
        fpid = int(request.POST.get("fpid",0))
        pbSet = PrecastBeam.objects.filter(curfactoryposition_id=fpid)
        for each in pbSet:
            tmpObj={}
            tmpObj["pbid"]=each.id
            tmpObj["构件编号"]=each.sign
            tmpObj["类型"]=each.pbtype.name
            pbRecordList=PBStatusRecord.objects.filter(precastbeam_id=each.id, factoryposition_id=fpid, isactive=1).order_by("time")
            if pbRecordList:
                tmpObj["进场时间"]=pbRecordList[0].time
            else:
                tmpObj["进场时间"]=datetime.datetime.now()
            
            tmpObj["积压天数"]=(datetime.datetime.now()-tmpObj["进场时间"]).days
            tmpObj["进场时间"]=tmpObj["进场时间"].strftime('%Y-%m-%d') 
            tmpObj["占用面积"]=round(each.volume,2)
            pbList.append(tmpObj)
             
        response_data["pbList"] = pbList
    except:
        traceback.print_exc()
        response_data["status"] = "Fail"

    return HttpResponse(json.dumps(response_data), content_type="application/json")    

@csrf_exempt
@login_required(login_url="/login/")  
def factoryarea_search(request):
    try:
        response_data={}
        pbKey = request.POST.get("keyword","")
        positionList = [each[0] for each in PrecastBeam.objects.filter(sign__icontains=pbKey).exclude(curfactoryposition=None).values_list("curfactoryposition_id").distinct()]
             
        response_data["positionList"] = positionList
    except:
        traceback.print_exc()
        response_data["status"] = "Fail"

    return HttpResponse(json.dumps(response_data), content_type="application/json")   

def edit_factoryarea(request, id):

    factoryarea_instance = FactoryArea.objects.get(id=id)

    form = FactoryAreaForm(request.POST or None, instance = factoryarea_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_factoryarea.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_factoryposition(request):
    form = FactoryPositionForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = FactoryPositionForm()

    t = get_template('TaskAndFlow/create_factoryposition.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_factoryposition(request):
  
    list_items = FactoryPosition.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_factoryposition.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_factoryposition(request, id):
    factoryposition_instance = FactoryPosition.objects.get(id = id)

    t=get_template('TaskAndFlow/view_factoryposition.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_factoryposition(request, id):

    factoryposition_instance = FactoryPosition.objects.get(id=id)

    form = FactoryPositionForm(request.POST or None, instance = factoryposition_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_factoryposition.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_unitproject(request):
    form = UnitProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = UnitProjectForm()

    t = get_template('TaskAndFlow/create_unitproject.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_unitproject(request):
  
    list_items = UnitProject.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_unitproject.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_unitproject(request, id):
    unitproject_instance = UnitProject.objects.get(id = id)

    t=get_template('TaskAndFlow/view_unitproject.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_unitproject(request, id):

    unitproject_instance = UnitProject.objects.get(id=id)

    form = UnitProjectForm(request.POST or None, instance = unitproject_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_unitproject.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_elevation(request):
    form = ElevationForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ElevationForm()

    t = get_template('TaskAndFlow/create_elevation.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_elevation(request):
  
    list_items = Elevation.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_elevation.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_elevation(request, id):
    elevation_instance = Elevation.objects.get(id = id)

    t=get_template('TaskAndFlow/view_elevation.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_elevation(request, id):

    elevation_instance = Elevation.objects.get(id=id)

    form = ElevationForm(request.POST or None, instance = elevation_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_elevation.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_pbmaterial(request):
    form = PBMaterialForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PBMaterialForm()

    t = get_template('TaskAndFlow/create_pbmaterial.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_pbmaterial(request):
  
    list_items = PBMaterial.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_pbmaterial.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_pbmaterial(request, id):
    pbmaterial_instance = PBMaterial.objects.get(id = id)

    t=get_template('TaskAndFlow/view_pbmaterial.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_pbmaterial(request, id):

    pbmaterial_instance = PBMaterial.objects.get(id=id)

    form = PBMaterialForm(request.POST or None, instance = pbmaterial_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_pbmaterial.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_pbtype(request):
    form = PBTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PBTypeForm()

    t = get_template('TaskAndFlow/create_pbtype.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_pbtype(request):
  
    list_items = PBType.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_pbtype.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_pbtype(request, id):
    pbtype_instance = PBType.objects.get(id = id)

    t=get_template('TaskAndFlow/view_pbtype.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_pbtype(request, id):

    pbtype_instance = PBType.objects.get(id=id)

    form = PBTypeForm(request.POST or None, instance = pbtype_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_pbtype.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_pbstatus(request):
    form = PBStatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PBStatusForm()

    t = get_template('TaskAndFlow/create_pbstatus.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_pbstatus(request):
  
    list_items = PBStatus.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_pbstatus.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_pbstatus(request, id):
    pbstatus_instance = PBStatus.objects.get(id = id)

    t=get_template('TaskAndFlow/view_pbstatus.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_pbstatus(request, id):

    pbstatus_instance = PBStatus.objects.get(id=id)

    form = PBStatusForm(request.POST or None, instance = pbstatus_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_pbstatus.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_precastbeam(request):
    form = PrecastBeamForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PrecastBeamForm()

    t = get_template('TaskAndFlow/create_precastbeam.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_precastbeam(request):
  
    list_items = PrecastBeam.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_precastbeam.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_precastbeam(request, id):
    precastbeam_instance = PrecastBeam.objects.get(id = id)

    t=get_template('TaskAndFlow/view_precastbeam.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_precastbeam(request, id):

    precastbeam_instance = PrecastBeam.objects.get(id=id)

    form = PrecastBeamForm(request.POST or None, instance = precastbeam_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_precastbeam.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_user2pbstatus(request):
    form = User2PBStatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = User2PBStatusForm()

    t = get_template('TaskAndFlow/create_user2pbstatus.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_user2pbstatus(request):
  
    list_items = User2PBStatus.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_user2pbstatus.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_user2pbstatus(request, id):
    user2pbstatus_instance = User2PBStatus.objects.get(id = id)

    t=get_template('TaskAndFlow/view_user2pbstatus.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_user2pbstatus(request, id):

    user2pbstatus_instance = User2PBStatus.objects.get(id=id)

    form = User2PBStatusForm(request.POST or None, instance = user2pbstatus_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_user2pbstatus.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_pbstatusrecord(request):
    form = PBStatusRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PBStatusRecordForm()

    t = get_template('TaskAndFlow/create_pbstatusrecord.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_pbstatusrecord(request, id):
    pbstatusrecord_instance = PBStatusRecord.objects.get(id = id)

    t=get_template('TaskAndFlow/view_pbstatusrecord.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_pbstatusrecord(request, id):

    pbstatusrecord_instance = PBStatusRecord.objects.get(id=id)

    form = PBStatusRecordForm(request.POST or None, instance = pbstatusrecord_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_pbstatusrecord.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_tasktype(request):
    form = TaskTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = TaskTypeForm()

    t = get_template('TaskAndFlow/create_tasktype.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_tasktype(request):
  
    list_items = TaskType.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_tasktype.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_tasktype(request, id):
    tasktype_instance = TaskType.objects.get(id = id)

    t=get_template('TaskAndFlow/view_tasktype.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_tasktype(request, id):

    tasktype_instance = TaskType.objects.get(id=id)

    form = TaskTypeForm(request.POST or None, instance = tasktype_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_tasktype.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_taskstatus(request):
    form = TaskStatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = TaskStatusForm()

    t = get_template('TaskAndFlow/create_taskstatus.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_taskstatus(request):
  
    list_items = TaskStatus.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_taskstatus.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_taskstatus(request, id):
    taskstatus_instance = TaskStatus.objects.get(id = id)

    t=get_template('TaskAndFlow/view_taskstatus.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_taskstatus(request, id):

    taskstatus_instance = TaskStatus.objects.get(id=id)

    form = TaskStatusForm(request.POST or None, instance = taskstatus_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_taskstatus.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))




def create_user2taskstatus(request):
    form = User2TaskStatusForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = User2TaskStatusForm()

    t = get_template('TaskAndFlow/create_user2taskstatus.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_user2taskstatus(request):
  
    list_items = User2TaskStatus.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_user2taskstatus.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_user2taskstatus(request, id):
    user2taskstatus_instance = User2TaskStatus.objects.get(id = id)

    t=get_template('TaskAndFlow/view_user2taskstatus.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_user2taskstatus(request, id):

    user2taskstatus_instance = User2TaskStatus.objects.get(id=id)

    form = User2TaskStatusForm(request.POST or None, instance = user2taskstatus_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_user2taskstatus.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))


def create_taskstatusrecord(request):
    form = TaskStatusRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = TaskStatusRecordForm()

    t = get_template('TaskAndFlow/create_taskstatusrecord.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def list_taskstatusrecord(request):
  
    list_items = TaskStatusRecord.objects.all()
    paginator = Paginator(list_items ,10)


    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/list_taskstatusrecord.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))



def view_taskstatusrecord(request, id):
    taskstatusrecord_instance = TaskStatusRecord.objects.get(id = id)

    t=get_template('TaskAndFlow/view_taskstatusrecord.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

def edit_taskstatusrecord(request, id):

    taskstatusrecord_instance = TaskStatusRecord.objects.get(id=id)

    form = TaskStatusRecordForm(request.POST or None, instance = taskstatusrecord_instance)

    if form.is_valid():
        form.save()

    t=get_template('TaskAndFlow/edit_taskstatusrecord.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))



@login_required(login_url="/login/") 
@check_permission_ajax
def create_notice(request):
    response_data = {}
    response_data["status"]="Failed"
    try:
        expiredate = request.GET.get('expire', '')
        messagenew = request.GET.get('message', '')
        RelateFileList = eval(request.GET.get('RelateFileList', '[]'))
        print RelateFileList
       
        newNotice = Notice.objects.create(title="公告",message=messagenew,expire=expiredate,sender=request.user)
        
        for FileId in RelateFileList:
            docId = int(FileId)
            Doc2Relate.objects.create(relatetype="公告", relateid=newNotice.id,
                                     creator=request.user, document_id=docId, createtime=datetime.datetime.now())

        notifyuserlist = getPrjUserlist()
        pushmsgList = []
        for each in notifyuserlist:
            pushmsgList.append(PushMessage(status=0, relatetype="公告", relateid=newNotice.id,
                            agentid= Project.objects.get(id=settings.CURRENT_PROJECT_ID).appid,
                            fromuser_id=request.user.id, touser_id=each.id, message=messagenew))

        PushMessage.objects.bulk_create(pushmsgList)

        response_data["status"]="Succeed"
        
    except Exception, e: 
        response_data['error'] = '%s' % e
        print response_data['error']

    return HttpResponse(json.dumps(response_data), content_type="application/json") 


@login_required(login_url="/login/") 
@check_permission
def list_notice(request):
    t = get_template('AboutUs/notices.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

@login_required(login_url="/login/") 
@check_permission_ajax
def delete_notice(request):
    response_data = {}
    response_data["status"]="Failed"
    try:
        noticeId = request.GET.get('id', '')
       
        Notice.objects.filter(id=noticeId).delete()
        
        response_data["status"]="Succeed"
        
    except Exception, e: 
        response_data['error'] = '%s' % e
        print response_data['error']

    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@login_required(login_url="/login/") 
@check_permission_ajax
def edit_notice(request):
    response_data = {}
    response_data["status"]="Failed"
    try:
        noticeId = request.GET.get('id', '')
        expiredate = request.GET.get('expire', '')
        messagenew = request.GET.get('message', '')
        RelateFileList = eval(request.GET.get('RelateFileList', '[]'))
     
        print expiredate
        notice_instance = Notice.objects.get(id=noticeId)
        notice_instance.expire=expiredate
        notice_instance.message=messagenew
        notice_instance.save()

        for FileId in RelateFileList:
            docId = int(FileId)
            Doc2Relate.objects.create(relatetype="公告", relateid=notice_instance.id,
                                     creator=request.user, document_id=docId, createtime=datetime.datetime.now())
        
        response_data["status"]="Succeed"
        
    except Exception, e: 
        response_data['error'] = '%s' % e
        print response_data['error']

    return HttpResponse(json.dumps(response_data), content_type="application/json")
   
@login_required(login_url="/login/") 
def Tracking_imformation(request):
    return render_to_response('TaskAndFlow/area_person_imformation/Tracking_imformation.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
@check_permission
def area_personnel(request):
    return render_to_response('TaskAndFlow/area_person_imformation/area_personnel.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def personnel_details(request):
    return render_to_response('TaskAndFlow/area_person_imformation/personnel_details.html', RequestContext(request,locals()))