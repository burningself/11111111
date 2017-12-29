# -*- coding: utf-8 -*-
'''

@author: pgb
'''
import traceback, datetime, re
import django.db
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
from TaskAndFlow.forms import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from Scc4PM.settings import CURRENT_PROJECT_ID
import cgi
from django.shortcuts import redirect
from TaskAndFlow.utility_flowtemplate import *
from TaskAndFlow.utility_filemanager import *
from UserPrjConfig.permissions import *
# Create your views here.

#Goujian
@login_required(login_url="/login/")  
def goujian_list(request):
    if checkMobile(request):
        config={}
        ticket, appid, _ = fetch_ticket()
        
        sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.path)
        
        config = sign.sign()
        config["appid"] = appid
        
        templateName='TaskAndFlow/goujian_list_mobile.html'
    else:
        templateName='TaskAndFlow/goujian_list.html'
    return render_to_response(templateName, RequestContext(request,locals()))


@login_required(login_url="/login/")  
def goujian_group(request):
    if checkMobile(request):
        config={}
        ticket, appid, _ = fetch_ticket()
        
        sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.path)
        
        config = sign.sign()
        config["appid"] = appid
        
        templateName='TaskAndFlow/goujian_list_mobile.html'
    else:
        list_items = CompGroup.objects.all()
        progressList = ["<50","<90","=100"]
        typeList = CompGroupType.objects.all()
        pbstatusList = PBStatus.objects.all()

        if request.method == 'GET':
            groupid = request.GET.get('number', '')
            progress = int(request.GET.get('progress', '0'))
            gtype = int(request.GET.get('gtype', '0'))
            pbstatus = int(request.GET.get('pbstatus', '0'))
            orderby = request.GET.get('orderby', 'id')
            clickcount = request.GET.get('clickcount', '0')
            
            if groupid.isdigit():
                list_items=list_items.filter(id=groupid)
                groupid=groupid
                
            if progress and (progress!='0'):
                list_items=list_items.filter(rate__lte=int(progressList[progress-1][1:]))
                progress=int(progress)

            if pbstatus and (pbstatus!='0'):
                list_items=list_items.filter(pbstatus_id=pbstatus)
                pbstatus=int(pbstatus)
                    
            if gtype and (gtype!='0'):
                list_items=list_items.filter(type_id=gtype)
                gtype=int(gtype)
                
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
        templateName='TaskAndFlow/goujian_group_list.html'
         
    return render_to_response(templateName, RequestContext(request,locals()))

@login_required(login_url="/login/")  
def goujian_pbgrp(request):
    list_items = Pbgroup.objects.all()
    typeList = PBType.objects.all()

    if request.method == 'GET':
        grpnumber = request.GET.get('grpnumber', '')
        grpname = request.GET.get('grpname', '')
        gtype = int(request.GET.get('gtype', '0'))
        orderby = request.GET.get('orderby', 'id')
        clickcount = request.GET.get('clickcount', '0')
        
        if grpnumber:
            list_items=list_items.filter(number__icontains=grpnumber)

        if grpname:
            list_items=list_items.filter(name__icontains=grpname)

        if gtype and (gtype!='0'):
            list_items=list_items.filter(pbtype_id=gtype)
            gtype=int(gtype)
            
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
    templateName='TaskAndFlow/goujian/goujian_pbgrp_list.html'
         
    return render_to_response(templateName, RequestContext(request,locals()))


@csrf_exempt
@login_required(login_url="/login/")  
def goujian_group_create(request):
    try:
        response_data = {"status":1}
        
        name = request.POST.get('name', '')
        descrition = request.POST.get('descrition', '')
        total_count = int(request.POST.get('total_count', 0))
        rate = int(request.POST.get('rate', 100))
        pbstatus = int(request.POST.get('pbstatus', 0))

        type = int(request.POST.get('type', 0)) if int(request.POST.get('type', 0)) else None
        CompGroup.objects.create(name=name, descrition=descrition, total_count=total_count, rate=rate, pbstatus_id=pbstatus, type_id=type)
    except:
        traceback.print_exc()
        response_data["status"]=0
        response_data["error"]="提交失败！"
        
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@login_required(login_url="/login/")  
def goujian_group_edit(request, id):
    group_instance = CompGroup.objects.get(id=id)
    relate_group_instance = CompGroup.objects.filter(type=group_instance.type).exclude(id=group_instance.id)[0]
    
    if CompGroup.objects.filter(type_id=group_instance.type_id).exclude(id=id):
        relateGroup = CompGroup.objects.filter(type_id=group_instance.type_id).exclude(id=id)[0]
    
    if request.method == 'POST':
        if request.POST.get('PbSelected', ''):
            selpbs=request.POST.get('PbSelected', '')
            selPbList=selpbs.split(",")
            for pb in selPbList:
                group_instance.precastbeam.add(PrecastBeam.objects.get(sign=pb))
    
    list_items_total = group_instance.precastbeam.all().count()
    list_items = group_instance.precastbeam.all().order_by("-curstatus")

    t=get_template('TaskAndFlow/edit_pbgroup.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))

@csrf_exempt
@login_required(login_url="/login/") 
def goujian_group_delete(request):   
    try:
        flag=1
        response_data = {"status":1}
        groupid  = int(request.POST.get('groupid', 0))
        
        if PBStatusRecord.objects.filter(compgroup_id=groupid):
            response_data["status"]=0
            response_data["error"]="已有关联记录，不允许删除！"
        else:
            CompGroup.objects.get(id=groupid).precastbeam.remove()
            CompGroup.objects.get(id=groupid).delete()
            
    except:
        traceback.print_exc()
        response_data["status"]=0
        response_data["error"]="提交失败！"
    
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@csrf_exempt
@login_required(login_url="/login/") 
def goujian_group_pbdelete(request):   
    try:
        flag=1
        response_data = {"status":1}
        gid  = int(request.POST.get('gid', 0))
        pid  = int(request.POST.get('pid', 0))

        if CompGroup.objects.filter(id=gid):
            if CompGroup.objects.get(id=gid).precastbeam.filter(id=pid):
                CompGroup.objects.get(id=gid).precastbeam.remove(PrecastBeam.objects.get(id=pid))
                
        PBStatusRecord.objects.filter(precastbeam_id=pid, compgroup_id=gid).update(compgroup=None)    
        
    except:
        traceback.print_exc()
        response_data["status"]=0
        response_data["error"]="提交失败！"
    
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

def goujian_load(request):
    if checkMobile(request):
        config={}
        ticket, appid, _ = fetch_ticket()
        
        sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.path)
        
        config = sign.sign()
        config["appid"] = appid
        
        templateName='TaskAndFlow/goujian_load_mobile.html'
    else:
        templateName='TaskAndFlow/goujian_load.html'
    
    return render_to_response(templateName, RequestContext(request,locals()))


@login_required(login_url="/login/")  
@check_permission
def goujian_qrcode(request):
    pbid=0
    pblist=PrecastBeam.objects.all().order_by('sign')
    pbgrp = request.GET.get('pbgrp', None)
    if pbgrp and pbgrp!='None':
        pbidlist = Pbgrouprelation.objects.filter(pbgroup_id=pbgrp).values_list('pb_id', flat=True)
        pblist=pblist.filter(id__in=pbidlist)

    if 'pbid' in request.GET:
        pbid=int(request.GET.get('pbid',0))
        pblist=pblist.filter(id=pbid)
    elif 'selPbtypes' in request.GET and 'selElevations' in request.GET:
        selPbtypes = request.GET.get('selPbtypes', '')
        selElevations = request.GET.get('selElevations','')
       
        if len(selElevations)>0:
            ElevationIds = []
            for ElevationId in selElevations[:-1].split(","):
                ElevationIds.append(int(ElevationId))
            pblist=pblist.filter(elevation__in=ElevationIds)
    
        if len(selPbtypes)>0:
            PbtypesIds = []
            for PbtypesId in selPbtypes[:-1].split(","):
                PbtypesIds.append(int(PbtypesId))
            pblist=pblist.filter(pbtype__in=PbtypesIds)
    else:
        pbnumber = request.GET.get('number', '')
        unitproject = request.GET.get('unitproject', '')
        pbelevation = request.GET.get('pbelevation', '')
        major = request.GET.get('major', '')
        pbtype = request.GET.get('pbtype', '')
        pbstatus = request.GET.get('pbstatus', '')
        if 'taskid' in request.GET:
            taskid=int(request.GET.get('taskid',0))
            pblist=pblist.filter(task_id=taskid)
        
        print pbnumber
        if pbnumber:
            pblist=pblist.filter(sign__contains=pbnumber)
        if unitproject:
            pblist=pblist.filter(elevation__unitproject=unitproject)
        if pbelevation:
            pblist=pblist.filter(elevation=pbelevation)
        if major:
            pblist=pblist.filter(pbtype__major=major)
        if pbtype:
            pblist=pblist.filter(pbtype=pbtype)
        if pbstatus:
            pblist=pblist.filter(curstatus=pbstatus)
    

    idlist = [each.id for each in pblist]
    GrpIdlist = [each.relatedid for each in Monitoringelement.objects.filter(typetable="构件",relatedid__in=idlist)]
    pblist=pblist.filter(id__in=GrpIdlist)
    for each in pblist:
        mlist = Monitoringelement.objects.filter(typetable="构件",relatedid=each.id)
        if mlist:
            each.qrcode = mlist[0].qrcode

    #限制下条数 pgb
    pblist = pblist[:5000]
    pro=Project.objects.get(id=CURRENT_PROJECT_ID)

    qrcodetype =  ""
    try:
        qrcodetype = CustomInfo.objects.get(infotype="qrcode_type").custominfo
    except:
        pass
    if qrcodetype !="":
        templateName='TaskAndFlow/goujian/goujian_qrcode_' + qrcodetype +'.html'
    else:
        templateName='TaskAndFlow/goujian_qrcode.html'
    return render_to_response(templateName, RequestContext(request,locals()))

@login_required(login_url="/login/")  
def goujian_grpqrcode(request):
    pblist = Pbgroup.objects.all()

    grpnumber = request.GET.get('grpnumber', '')
    grpname = request.GET.get('grpname', '')
    gtype = int(request.GET.get('gtype', '0'))
    
    if grpnumber:
        pblist=pblist.filter(number__icontains=grpnumber)

    if grpname:
        pblist=pblist.filter(name__icontains=grpname)

    if gtype and (gtype!='0'):
        pblist=pblist.filter(pbtype_id=gtype)

    idlist = [each.id for each in pblist]
    GrpIdlist = [each.relatedid for each in Monitoringelement.objects.filter(typetable="构件组",relatedid__in=idlist)]
    pblist=pblist.filter(id__in=GrpIdlist)
    for each in pblist:
        each.sign = each.number
        mlist = Monitoringelement.objects.filter(typetable="构件组",relatedid=each.id)
        if mlist:
            each.qrcode = mlist[0].qrcode
    pro=Project.objects.get(id=CURRENT_PROJECT_ID)
       
    templateName='TaskAndFlow/goujian_qrcode.html'
         
    return render_to_response(templateName, RequestContext(request,locals()))

@login_required(login_url="/login/")
@check_permission
def goujian_trace(request):
    pbid=int(request.GET.get('pbid',0))
    try:
        pbinfo = PrecastBeam.objects.get(id = pbid)
    except:
        pbinfo = None
    
    if pbinfo == None:
        pbsign=request.GET.get('sign','')
        try:
            pbinfo = PrecastBeam.objects.get(sign = pbsign)
        except:
            pbinfo = None
    
    if pbinfo:
        pbsign=pbinfo.sign
    refreshPbstatus(pbinfo)

    statuslist = PBStatus.objects.filter(pbtype=pbinfo.pbtype).order_by('sequence').values()
    for status in statuslist:
        if PBStatusRecord.objects.filter(precastbeam=pbid,status_id=status['id'],isactive=1).count()>0:
            sumPercentage = PBStatusRecord.objects.filter(status_id=status['id'],precastbeam=pbid,isactive=True,
                                          percentage__isnull=False).aggregate(Sum('percentage'))["percentage__sum"]
            status["sumPercentage"]=sumPercentage
            pbrecordTgt=PBStatusRecord.objects.filter(precastbeam=pbid,status_id=status['id'],isactive=1)
            status["status_record"]=pbrecordTgt
            for substatus in pbrecordTgt:
                substatus.docList = None
                if Doc2Relate.objects.filter(relatetype=u"构件状态修改记录", relateid=substatus.id).count()>0:
                    substatus.docList=Doc2Relate.objects.filter(relatetype=u"构件状态修改记录", relateid=substatus.id)
        else:
            status["status_record"]=None
       
        
    statuslistHis=PBStatusRecord.objects.filter(precastbeam=pbid).order_by("-time")
    for each in statuslistHis:
        each.docList = Doc2Relate.objects.filter(relatetype=u"构件状态修改记录", relateid=each.id)
    
    if checkMobile(request):
        config={}
        ticket, appid, _ = fetch_ticket()
        if request.GET.get('sign',''):
            url="http://" + request.META["HTTP_HOST"] + request.path + "?sign=" + pbsign
        else:
            url="http://" + request.META["HTTP_HOST"] + request.path + "?pbid=" + str(pbid)
        
        sign = Sign(ticket,  url)
        
        config = sign.sign()
        config["appid"] = appid 
        
        templateName='TaskAndFlow/goujian/goujian_trace_mobile.html'
    else:
        templateName='TaskAndFlow/goujian_trace.html'
    return render_to_response(templateName, RequestContext(request,locals()))


@login_required(login_url="/login/")  
def goujian_trace_front(request):
    pbid=int(request.GET.get('pbid',0))
    try:
        pbinfo = PrecastBeam.objects.get(id = pbid)
    except:
        pbinfo = None
    
    if pbinfo == None:
        pbsign=request.GET.get('sign','')
        try:
            pbinfo = PrecastBeam.objects.get(sign = pbsign)
        except:
            pbinfo = None
    
    if pbinfo:
        pbsign=pbinfo.sign
    #refreshPbstatus(pbinfo)

    statuslist = PBStatus.objects.filter(pbtype=pbinfo.pbtype).order_by('sequence').values()
    for status in statuslist:
        if PBStatusRecord.objects.filter(precastbeam=pbid,status_id=status['id'],isactive=1).count()>0:
            sumPercentage = PBStatusRecord.objects.filter(status_id=status['id'],precastbeam=pbid,isactive=True,
                                          percentage__isnull=False).aggregate(Sum('percentage'))["percentage__sum"]
            status["sumPercentage"]=sumPercentage
            pbrecordTgt=PBStatusRecord.objects.filter(precastbeam=pbid,status_id=status['id'],isactive=1)
            status["status_record"]=pbrecordTgt
            for substatus in pbrecordTgt:
                substatus.docList = None
                if Doc2Relate.objects.filter(relatetype=u"构件状态修改记录", relateid=substatus.id).count()>0:
                    substatus.docList=Doc2Relate.objects.filter(relatetype=u"构件状态修改记录", relateid=substatus.id)
        else:
            status["status_record"]=None
       
        
    statuslistHis=PBStatusRecord.objects.filter(precastbeam=pbid).order_by("-time")
    for each in statuslistHis:
        each.docList = Doc2Relate.objects.filter(relatetype=u"构件状态修改记录", relateid=each.id)
    
   
        
    templateName='TaskAndFlow/goujian/goujian_trace_front.html'

    return render_to_response(templateName, RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/")  
def goujian_search(request):
    try:
        response_data={}
        response_data["status"] = "Fail"
        qrStr = request.POST.get("keyword")
        #注释掉，不知道干啥的呀？ todo
        #pbsign= re.search(CustomInfo.objects.get(infotype="qrformat").custominfo,qrStr).group(0) 

        MoteleObj = Monitoringelement.objects.get(qrcode=qrStr)
        if MoteleObj.typetable == u"构件" or MoteleObj.typetable == u"安全设施":
            goujianObj = PrecastBeam.objects.get(id=MoteleObj.relatedid)
            response_data["status"] = "Succeed"
            response_data["rePath"] = "/task/goujian/trace/?pbid=" +str(goujianObj.id)
        elif MoteleObj.typetable == u"构件组":
            pblist = [each.pb for each in Pbgrouprelation.objects.filter(pbgroup_id=MoteleObj.relatedid)]
            if len(pblist)>0:
                goujianObj = pblist[0]
                response_data["status"] = "Succeed"
                response_data["rePath"] = "/task/goujian/trace/?pbid=" +str(goujianObj.id)
    except:
        response_data["status"] = "Fail"
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")    

@login_required(login_url="/login/") 
def goujian_create(request):
    return render_to_response('TaskAndFlow/jishu_.html', RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/") 
def goujian_read(request):
    try: 
        response_data={}
        statusSet=[] 
        statusSet_zhijian=[] 
        qrStr = request.POST.get("keyword") 
        #pbsign= re.search(CustomInfo.objects.get(infotype="qrformat").custominfo,qrStr).group(0)  
        
        if request.POST.get("chooseStatus") == "" or request.POST.get("chooseStatus") == None:
            chooseStatus = 0 
        else:
            chooseStatus = int(request.POST.get("chooseStatus"))
        
        nextState = request.POST.get("nextState",1) 
        

        qrcodetmp = qrStr.split(',')[0]
        goujianObj = Monitoringelement.objects.get(qrcode=qrcodetmp)

        
        if goujianObj:
            #todo 注释掉强制刷新逻辑 pgb
            #refreshPbstatus(goujianObj)
            response_data["status"] = "Succeed"
            
            statuslist = fetchStatusList(goujianObj, request.user)
                
            statuslist_zhijian = fetchZhiJianStatusList(goujianObj)

            curstatus = getCurStatus(goujianObj)

            if statuslist:
                for each in statuslist:
                    tmpObj={}
                    tmpObj["id"]=each.id
                    tmpObj["statusname"]=each.statusname
                    statusSet.append(tmpObj)
            
            if statuslist_zhijian:
                for each in statuslist_zhijian:
                    tmpObj={}
                    tmpObj["id"]=each
                    tmpObj["statusname"]=PBStatus.objects.get(id=each).statusname
                    statusSet_zhijian.append(tmpObj)
            
            response_data["statusName"] = 0
            #print curstatus.id
            if nextState==1 and curstatus and curstatus.nextstatus in statuslist:
                response_data["statusName"] = curstatus.nextstatus_id
            elif curstatus in statuslist:
                response_data["statusName"] = curstatus.id
            else:
                response_data["statusName"] = 0
            
            
            if response_data["statusName"] < chooseStatus:
                response_data["statusName"] = chooseStatus
            
            response_data["statusSet_zhijian"] = statusSet_zhijian
            response_data["statusSet"] = statusSet
            response_data["pbid"] = goujianObj.id
            response_data["pbnumber"] = qrStr
            response_data["pbcategory"] = "构件"
            response_data["pbtype"] = goujianObj.typetable
            # if goujianObj.curfactoryposition:
            #     response_data["duichang"] = goujianObj.curfactoryposition.id
            
        else:
            response_data["status"] = "Fail"
            response_data["error"] = "没有对应扫码元素！"
        
    except Exception, e: 
        traceback.print_exc()
        response_data["status"] = "Fail"
        response_data['error'] = '%s' % e
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")    

@csrf_exempt
@login_required(login_url="/login/") 
def goujian_update(request):
    if request.method=="POST":
        response_data={}
        response_data["isqualify"] = 'false'
        try:
            if request.POST.get("goujian") not in ["",None] and request.POST.get("status") not in ["",None]:
                goujians = request.POST.get("goujian")
                duichang= request.POST.get('duichang')
                status=int(request.POST.get('status'))
                beizhu=request.POST.get('beizhu')
                imgInfo = request.POST.get('zhijian')
                latitude = 0 if request.POST.get("latitude") in ["",None] else request.POST.get("latitude")
                longitude = 0 if request.POST.get("longitude") in ["",None] else request.POST.get("longitude")
                speed = 0 if request.POST.get("speed") in ["",None] else request.POST.get("speed")
                accuracy = 0 if request.POST.get("accuracy") in ["",None] else request.POST.get("accuracy")
                relatefiles = eval(request.POST.get("relatefiles","[]"))
                lururq = request.POST.get('lururq',None)
                percent = request.POST.get('percent','100')
                if lururq:
                    lururq=datetime.datetime.strptime(lururq,'%Y-%m-%d %H:%M')

                goujians = eval(goujians)
                for goujian in goujians:
                    try: 
                        MoteleObj = Monitoringelement.objects.get(typetable=goujian["typetable"],relatedid=goujian["relatedid"])

                        statuslist = fetchStatusList(MoteleObj, request.user)
                        
                    except:
                        MoteleObj = None

                    #todo 堆场与状态的联动 pgb（选择状态的时候，筛选对应的堆场，上面）
                    try: 
                        duichangObj = FactoryPosition.objects.get(id=int(duichang))
                    except:
                        duichangObj = None
                        
                        
                    try:
                        statusObj,isqualify = getStatusObj(MoteleObj,status)
                    except:
                        traceback.print_exc()
                        statusObj = None
           
                    if MoteleObj ==None:
                        color_code="red"
                        result_string = "没有扫码元素！"
                    elif  statusObj == None:
                        color_code="red"
                        result_string = "请选择上传状态！"
                    else:
                        try:
                           
                            color_code,result_string,pbrecordid = updateMoteleObjStatus(MoteleObj,statusObj,request.user,duichangObj,beizhu,percent,latitude,longitude,lururq)

                            if color_code!="red":
                                 #扫码不合格发起流程  
                                if statusObj.isqualify:
                                    if statusObj.relatedflowtemplate:
                                        response_data["goujian"] = goujian
                                        response_data["isqualify"] = "true" if isqualify else "false"
                                        response_data["describe"] = beizhu
                                        response_data["relatedflowtemplate"]=statusObj.relatedflowtemplate_id
                                    else:
                                        result_string="验收成功，验收不合格未关联整改流程"

                                #upload img
                                #todo 根据不同类型 放到不同目录下pgb
                                if imgInfo and ':' in imgInfo: 
                                    imgList=imgInfo.split(':')[1].split(';')
                                    name= MoteleObj.qrcode
                                    if uploadfile_weixinstatus(imgList,name,'quality', '构件状态修改记录', request.user, pbrecordid,MoteleObj):
                                        result_string="状态提交,质检失败！"  
                                        color_code="blue"
                                if len(relatefiles)>0:
                                    dir = MoteleObjDirectory(MoteleObj)
                                    for docId in relatefiles:
                                        doc = Document.objects.get(id=int(docId))
                                        MoteleObjDoc2Relate('构件状态修改记录', pbrecordid, request.user, doc, MoteleObj)
                                        if dir:
                                            doc.docdirectory.add(dir)
                                            movefiletoDir(doc,dir)
                           
                        except django.db.IntegrityError as e:
                            traceback.print_exc()
                            color_code="red"
                            result_string="状态重复提交，已更新！"
                        except Exception as e :
                            traceback.print_exc()
                            color_code="red"
                            result_string="数据错误，上传失败！"

                    if color_code=="red":
                        result_string=result_string
                        break

            else:
                color_code="red"
                result_string="信息不全，提交失败！"
          
            response_data["color_code"] = color_code
            response_data["result_string"] = result_string
        except:
            traceback.print_exc()
            response_data["color_code"] = color_code
            response_data["result_string"] = "验收失败"



        return  HttpResponse(json.dumps(response_data), content_type="application/json")    
    else:
        statuslist=[]    
        duichanglist=FactoryPosition.objects.all().values()
        majorList = UserMajor.objects.all()
        curMajorId = getUserMajor(request.user)

        title = getTitleFromUrl(request, request.get_full_path())
        havesheshi,havejixie,haverenwu = checkMonitorType()

        config={}
        ticket, appid, _ = fetch_ticket()
        
        sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.path)
        
        config = sign.sign()
        config["appid"] = appid
        templateName='TaskAndFlow/goujian_update_mobile.html'

        
        return render_to_response(templateName, RequestContext(request,locals()))


@csrf_exempt
@login_required(login_url="/login/")
def gxyanshou(request):
    gongxu = []
    gxdeadlineTimerange = request.GET.get('gxdeadlineTimerange', '')
    if gxdeadlineTimerange:
        startdate, enddate = GetDateRange(gxdeadlineTimerange)
        gongxu = Acceptance.objects.filter(
            is_finished=False, deadline__range=(startdate, enddate))
    else:
        gongxu = Acceptance.objects.filter(is_finished=False)

    gxpaginator = Paginator(gongxu, 10)
    gxlistcount = len(gongxu)
    try:
        gxpage = int(request.GET.get('pagegx'))
        typeye = 2
    except:
        gxpage = 1
    try:
        gongxu = gxpaginator.page(gxpage)
    except:
        gongxu = gxpaginator.page(gxpaginator.num_pages)
    templateName = 'TaskAndFlow/flowtemplate/gongxuyanshou.html'
    return render_to_response(templateName, RequestContext(request, locals()))

def goujian_zhijian(request):
    pbid=int(request.GET.get('pbid',0))
    docList=[]
    tmp={}

    if checkMobile(request):
        config={}
        ticket, appid, _ = fetch_ticket()
        
        sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.path)
        
        config = sign.sign()
        config["appid"] = appid
        
        pbrecordList=[each(0) for each in PBStatusRecord.objects.filter(precastbeam_id=pbid).values_list("id")]
        
        docList = Doc2Relate.objects.filter(relatetype="构件状态修改记录", relateid__in=pbrecordList)
        
        
        
        templateName='TaskAndFlow/goujian_zhijian_mobile.html'
    else:
        templateName='TaskAndFlow/goujian_zhijian.html'
    
    return render_to_response(templateName, RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/") 
def goujian_update_zhijian(request):
    if request.method=="POST":
        try:
            ret={}
            ret["status"] = "Succeed"
            msg = "验收信息补充成功！"
            mediaStr= request.POST.get('zhijianList', [])
            imgList=mediaStr.split(';')
            pbid = request.POST.get('pbid', " ")
            status = request.POST.get('pbstatus', " ")
            beizhu = request.POST.get('beizhu', " ")

            MoteleObj = Monitoringelement.objects.get(qrcode=pbid)

            retstatus,msg,pbrecordid=updateMoteleObjStatusAppend(MoteleObj,status,beizhu)
                
            if uploadfile_weixinstatus(imgList,pbid,'quality', '构件状态修改记录', request.user, pbrecordid,MoteleObj):
                msg="状态提交,质检失败！"  
                retstatus="Fail"

            statusSet_zhijian=[]
            statuslist_zhijian = fetchZhiJianStatusList(MoteleObj)
            
            for each in statuslist_zhijian:
                tmpObj={}
                tmpObj["id"]=each
                tmpObj["statusname"]=PBStatus.objects.get(id=each).statusname
                statusSet_zhijian.append(tmpObj)
            
            ret["statusSet_zhijian"]=statusSet_zhijian
            #ret["rePath"] = "/task/goujian/trace/?pbid=" +str(goujianObj.id)
            ret["status"] = retstatus
            ret["msg"] = msg   

        except Monitoringelement.DoesNotExist:
            traceback.print_exc()
            ret["status"] = "Fail"
            ret["msg"] = "构件信息不存在！"
        
        except Exception as e :
            traceback.print_exc()
            ret["status"] = "Fail"
            ret["msg"] = "服务器错误！"
        
    return HttpResponse(json.dumps(ret,ensure_ascii = False))

@login_required(login_url="/login/") 
def goujian_del(request):
    return render_to_response('TaskAndFlow/jishu.html', RequestContext(request,locals()))

@login_required(login_url="/login/") 
def modelview(request):
    if checkMobile(request):
        config = {}
        ticket, appid, _ = fetch_ticket()

        sign = Sign(ticket, "http://" +request.META["HTTP_HOST"] + request.path)

        config = sign.sign()
        config["appid"] = appid
        templateName='TaskAndFlow/flowtemplate_mobile/model_mobile.html'
    else:
        title = getTitleFromUrl(request, request.get_full_path())
        unitinfo=Modelfile.objects.get(isdefault=True)
        PBStatusChoices = PBStatus.objects.filter(pbtype__major=unitinfo.relatedmajor)
        templateName='common/modelview.html'
    return render_to_response(templateName, RequestContext(request,locals()))

@login_required(login_url="/login/") 
def getcounttypelist(request):
    response_data = {}
    response_data["counttypelist"]=[]
    try:
        _curUnitId = request.GET.get('_curUnitId', '')
        _curMajor = request.GET.get('_curMajor', '')
        iswholemodel = request.GET.get('_isWholeModel', '')

        liststatusIds = PrecastBeam.objects.filter(elevation__unitproject=_curUnitId,pbtype__major=_curMajor,
                                        curstatus__isnull=False).distinct().values("curstatus_id")

        if iswholemodel=="true":
            statuslist = PBStatus.objects.filter(id__in=liststatusIds).order_by('roughcounttype__sequence')
        else:
            statuslist = PBStatus.objects.filter(id__in=liststatusIds).order_by('detailcounttype__sequence')
        for eachStatus in statuslist:
            tmpObj = {}
            try:
                if iswholemodel=="true":
                    if eachStatus.roughcounttype:
                        tmpObj["id"] = eachStatus.roughcounttype.id
                        tmpObj["name"] = eachStatus.roughcounttype.name
                        tmpObj["color"] = eachStatus.roughcounttype.rendercolor
                        if tmpObj not in response_data["counttypelist"]:
                            response_data["counttypelist"].append(tmpObj)
                else:
                    if eachStatus.detailcounttype:
                        tmpObj["id"] = eachStatus.detailcounttype.id
                        tmpObj["name"] = eachStatus.detailcounttype.name
                        tmpObj["color"] = eachStatus.detailcounttype.rendercolor
                        if tmpObj not in response_data["counttypelist"]:
                            response_data["counttypelist"].append(tmpObj)
            except:
                continue

        response_data["issuc"]="true"

    except Exception, e: 
        print e
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"

    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def getinitialmodel(request):
    response_data = {}
    try:
        loadtype = request.GET.get('type',None)
        unitinfo = None
        if loadtype:
            if loadtype=="安全总览":
                major = UserMajor.objects.get(name="安全设施")
                unitinfo=Modelfile.objects.get(relatedmajor=major)
            else:
                pass
        else:
            unitinfo=Modelfile.objects.get(isdefault=True)
        if unitinfo:
            response_data["unitid"]=str(unitinfo.relatedunitproject_id)
            response_data["majorid"]=str(unitinfo.relatedmajor_id)
            response_data["modelfile"]=str(unitinfo.modelfile)
            response_data["iswhole"]=(unitinfo.iswhole)
            response_data["selectionmode"]=(unitinfo.selectionmode)
            response_data["homeview"]=eval(unitinfo.homeview) if unitinfo.homeview else []
            response_data["extdata"]=eval(unitinfo.extdata) if unitinfo.extdata else {}
            response_data["issuc"]="true"
    except:
        traceback.print_exc()
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required(login_url="/login/") 
def getmodelfile(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        _modelfile = request.GET.get('_modelfile', None)
        _curUnitId = request.GET.get('_curUnitId', None)
        _curMajor = request.GET.get('_curMajor', None)
        if _modelfile:
            modelfilelist = Modelfile.objects.filter(id=_modelfile)
        else:
            modelfilelist = Modelfile.objects.filter(relatedunitproject_id=_curUnitId,relatedmajor_id=_curMajor)
        if len(modelfilelist)>0:
            response_data["issuc"]="true"
            response_data["modelfile"]=modelfilelist[0].modelfile
            response_data["unitid"]=modelfilelist[0].relatedunitproject_id
            response_data["majorid"]=modelfilelist[0].relatedmajor_id
            response_data["iswhole"]=modelfilelist[0].iswhole
            response_data["selectionmode"]=(modelfilelist[0].selectionmode)
            response_data["homeview"]=eval(modelfilelist[0].homeview) if modelfilelist[0].homeview else []
            response_data["extdata"]=eval(modelfilelist[0].extdata) if modelfilelist[0].extdata else {}

    except Exception, e: 
        print e
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def setinitialmodel(request):
    response_data = {}
    try:
        defaultunitId = request.GET.get('defaultunitId', '')
        
        lastdefaultunitprj = Modelfile.objects.filter(isdefault=True)[0]
        lastdefaultunitprj.isdefault= False
        lastdefaultunitprj.save()
        
        newdefaultunitprj = Modelfile.objects.get(id = defaultunitId )
        newdefaultunitprj.isdefault = True;
        newdefaultunitprj.save()

        response_data["issuc"]="true"
    except Exception, e: 
        pritraceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  
   
@login_required(login_url="/login/") 
def getpbstatuslist(request):
    list_items = filterPbListRequest(request)
    
    response_data = {}
    response_data["pbstatuslist"]=[]

    iswholemodel = request.GET.get('_isWholeModel', '')

    listpbtypes = list_items.distinct().values("pbtype")
    statuslist = PBStatus.objects.filter(pbtype__in=listpbtypes)

    for eachStatus in statuslist:
        #statuslist = PBStatus.objects.filter(Q(detailcounttype =counttype.id)).values("id")
        pblist = list_items.filter(curstatus=eachStatus)
        try:
            tmpObj = {}
            #完成状态不赋予颜色 pgb
            tmpObj["color"] = ''
            if iswholemodel=="true":
                if eachStatus.roughcounttype:
                    tmpObj["color"] = eachStatus.roughcounttype.rendercolor
            else:
                if eachStatus.detailcounttype:
                    tmpObj["color"] = eachStatus.detailcounttype.rendercolor
            tmpObj["pblist"] = []
            for eachpb in pblist:
                tmpPb = {}
                tmpPb["lvmdbid"] = eachpb.lvmdbid
                tmpObj["pblist"].append(tmpPb)
            response_data["pbstatuslist"].append(tmpObj)
        except:
            traceback.print_exc()
            continue

    response_data["issuc"]="true"
    
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def getpbstatus(request):
    list_items = PrecastBeam.objects.all()
    curUnitId = request.GET.get('curUnitId', '')
    list_items=list_items.filter(elevation__unitproject=curUnitId)
    
    lastSelectDbid = request.GET.get('lastSelectDbid', 0)
    list_items=list_items.filter(lvmdbid=lastSelectDbid)
    
    response_data = {}
    response_data["pbstatuslist"]=[]
    
    countTypeList = StatusCountType.objects.all()
    for counttype in countTypeList:
        statuslist = PBStatus.objects.filter(Q(counttype =counttype.id)).values("id")
        pblist = list_items.filter(Q(curstatus__in=statuslist))
        tmpObj = {}
        tmpObj["name"] = counttype.name
        tmpObj["pblist"] = []
        for eachpb in pblist:
            tmpPb = {}
            tmpPb["lvmdbid"] = eachpb.lvmdbid
            tmpObj["pblist"].append(tmpPb)
        response_data["pbstatuslist"].append(tmpObj)

    response_data["issuc"]="true"
    
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def getstatuslist(request):

    curMajor = int(request.GET.get('_curMajor', '0'))
    list_items = PBStatus.objects.all()
    if curMajor!=0:
        list_items = list_items.filter(pbtype__major_id=curMajor)
    
    selPbtypes = request.GET.get('_selPbtypes', '')
    if len(selPbtypes)>0:
        PbtypesIds = []
        for PbtypesId in selPbtypes[:-1].split(","):
            PbtypesIds.append(int(PbtypesId))
        list_items=list_items.filter(pbtype__in=PbtypesIds)
    
    response_data = {}
    response_data["statuslist"]=[]
    
    for each in list_items:
        tmpObj = {}
        tmpObj["id"] = each.id
        tmpObj["name"] = each.pbtype.name+"_"+each.statusname
        response_data["statuslist"].append(tmpObj)

    response_data["issuc"]="true"
    
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json") 


@login_required(login_url="/login/") 
def getpblist(request):
    setpbgrp =([each.relatedid for each in Monitoringelement.objects.filter(typetable="构件")])
    list_items = filterPbListRequest(request)
    listtmp=[]
    for each in list_items:
        if each.id in setpbgrp:
            listtmp.append(each)

    list_items = listtmp
    result=""
    pageinfo=""
    response_data = {}
    
    paginator = Paginator(list_items ,10)
    listcount=len(list_items)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    for item in list_items:
        result+="<tr>"
        # result+="<td><input type='radio' onchange='changefunction()' name='pbcheck' value='%s'></td>" % (item.lvmdbid)
        result+="<td>%s</td>" % (item.drawnumber)
        result+="<td>%s</td>" % (item.curstatus.statusname if  item.curstatus else "未开始")
        result+="</tr>"
    
    try:
        if listcount>0:
            pageinfo+="<li><a onclick='changepage2Page(1)'>首页</a></li>"
            if list_items.number>1:
                pageinfo+="<li><a onclick='changepage2Page(%s)'><i class='fa fa-chevron-left'></i></a></li>" % (list_items.previous_page_number(),) 
            pageinfo+="<li><a>第 %s 页，共 %s页</a></li>" % (list_items.number,paginator.num_pages)
            if list_items.has_next:
                pageinfo+="<li><a onclick='changepage2Page(%s)'><i class='fa fa-chevron-right'></i></a></li>" % (list_items.next_page_number(),)
            pageinfo+="<li><a onclick='changepage2Page(%s)'>尾页</a></li>" % (paginator.num_pages,)
    except Exception, e:
        print e
    
    response_data["pageinfo"]=pageinfo
    response_data["pblist"] = result
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")    

@login_required(login_url="/login/") 
def getpbproperty(request):
    response_data = {}
    try:
        qrCode =request.GET.get('qrCode', None)
        pbinfo = None
        prjinfo = Project.objects.get(id=settings.CURRENT_PROJECT_ID)
        if qrCode:
            ele = Monitoringelement.objects.get(qrcode=qrCode,typetable="构件")
            pbinfo=PrecastBeam.objects.get(id = ele.relatedid)
        else:
            pbdbid = int(request.GET.get('dbId', '0'))
            curUnitId = int(request.GET.get('_curUnitId', '0'))
            _curMajor = int(request.GET.get('_curMajor', '0'))
            if len(PrecastBeam.objects.filter(Q(lvmdbid=pbdbid)&Q(elevation__unitproject=curUnitId)&Q(pbtype__major=_curMajor)))>0:
                pbinfo=PrecastBeam.objects.filter(Q(lvmdbid=pbdbid)&Q(elevation__unitproject=curUnitId)&Q(pbtype__major=_curMajor))[0]

        response_data["pbid"]=pbinfo.id
        response_data["task"]=pbinfo.task.name if pbinfo.task else "无"
        response_data["plantime"]=str(pbinfo.task.planfinish) if pbinfo.task else ""
        response_data["realtime"]=str(pbinfo.curstatustime) if pbinfo.curstatus and (pbinfo.curstatus.nextstatus==None or pbinfo.curstatus.iscritical) else ""
        response_data["pbnumber"]=pbinfo.drawnumber
        response_data["pbtype"]=pbinfo.pbtype.name if pbinfo.pbtype else "未知"
        response_data["pbelevation"]=pbinfo.elevation.name if pbinfo.elevation else "未知"
        response_data["pbstatus"]=pbinfo.curstatus.statusname if pbinfo.curstatus else "未开始"
        response_data["curstatuspercent"]=pbinfo.curstatuspercent if pbinfo.curstatuspercent else "0"
        response_data["statusdesc"]=pbinfo.curstatusdesc if pbinfo.curstatusdesc else ""
        
        response_data["dbid"]=pbinfo.lvmdbid
        try:
            response_data["extern"]=eval(pbinfo.description)
        except:
            response_data["extern"] = []
        response_data["constrator"]=prjinfo.constrator.name
        response_data["builder"]=prjinfo.builder.name
        response_data["manager"]=prjinfo.manager.truename
        response_data["issuc"]="true"
            #print json.dumps(response_data)
    except Exception, e:
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def getelevationtree(request):
    id=request.GET.get('id', '')
    major=request.GET.get('major',None)
    liuchengid = request.GET.get('liuchengid',None);
    if liuchengid:
        major = FlowTemplate.objects.get(id=int(liuchengid)).major_id
    if not major:
        major = getUserMajor(request.user)

    response_data = {}
    child_list=[]
    
    prj = Project.objects.get(id=settings.CURRENT_PROJECT_ID)
    if id=='#':
        response_data["id"]="rootelevationtree"
        response_data["text"]=prj.name
        response_data["icon"]="/img/buildings2.png"
        response_data["state"]= {'opened':True }

        
        unit_items=UnitProject.objects.all()
        for unit in unit_items:
            child_data = {}
            child_data["id"]="unitprj_"+str(unit.id)
            child_data["text"]=unit.name
            child_data["icon"]="/img/building2.png"
            
            tmpObj = {}
            tmpObj["unitid"] = str(unit.id)
            child_data["data"]=tmpObj

            list_items=Elevation.objects.filter(unitproject=unit).order_by('level')
            sub_child_list=[]
            if len(list_items)>0:
                zoneElevationall = ZoneElevation.objects.all()
                for item in list_items:
                    sub_child_data = {}
                    sub_child_data["id"]="floor_"+str(item.id)
                    sub_child_data["text"]=item.name
                    sub_child_data["icon"]=False
                    sub_child_list.append(sub_child_data)
                    list_zones=zoneElevationall.filter(elevation=item)
                    sub_child_list2=[]
                    for zoneitem in list_zones:
                        zone = zoneitem.zone
                        if major and zone.major_id!=int(major):
                            continue
                        sub_child_data2 = {}
                        sub_child_data2["id"]=str(item.id)+"zone_"+str(zone.id)
                        sub_child_data2["text"]=zone.name
                        sub_child_data2["icon"]=False
                        sub_child_list2.append(sub_child_data2)
                    sub_child_data["children"]=sub_child_list2
            child_data["children"]=sub_child_list
            child_list.append(child_data)
        response_data["children"]=child_list

    #print json.dumps(response_data)

    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def renwutree(request):
    # id 格式 renwu_1_1  renwu_深度_id
    try:
        id=request.GET.get('id', '')
        major=request.GET.get('major',None)
        liuchengid = request.GET.get('liuchengid',None);
        if liuchengid:
            major = FlowTemplate.objects.get(id=int(liuchengid)).major_id
        # if not major:
        #     major = getUserMajor(request.user)
        if id=='#':
            response_data = {}
            child_list=[]

            root = ProjectTask.objects.filter(parentid__isnull=True)
            if major:
                root=root.filter(major_id=int(major))

            if not root:
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                root=root[0]
            response_data["id"]="renwu_" + str(root.id)
            response_data["text"]=root.name
            response_data["state"]= {'opened':True }
            response_data["icon"]="/img/task.png"

            renwu1 = ProjectTask.objects.filter(parentid_id=root.id)
            if major:
                renwu1=renwu1.filter(major_id=int(major))
            for rw in renwu1:
                child_data = {}
                child_data["id"]="renwu_"+str(rw.id)
                child_data["text"]=rw.name
                child_data["children"]=True
                child_data["icon"]="/img/task.png"
                
                child_list.append(child_data)

            response_data["children"]=child_list
        else:
            child_list=[]
            nodeid = id.split('_')[1]

            renwux = ProjectTask.objects.filter(parentid_id=int(nodeid))
            if major:
                renwux=renwux.filter(major_id=int(major))
            for rw in renwux:
                child_data = {}
                child_data["id"]="renwu_"+str(rw.id)
                child_data["text"]=rw.name
                child_data["children"]=True
                child_data["icon"]="/img/task.png"
                child_list.append(child_data)
            response_data=child_list

        #print json.dumps(response_data)

        return HttpResponse(json.dumps(response_data), content_type="application/json")  
    except:
        traceback.print_exc()

@login_required(login_url="/login/") 
def getpbtypetree(request):
    id=request.GET.get('id', '')
    curmajor=request.GET.get('major',None)
    response_data = {}
    child_list=[]
        
    if id=='#':
        response_data["id"]="pbtypetree"
        response_data["text"]="构件类型"
        response_data["icon"]="/img/Catalog.png"
        response_data["state"]= {'opened':True }
        major_items=getMajorList()
        if curmajor:
            major_items = major_items.filter(id=int(curmajor))
        for major in major_items:
            child_data = {}
            child_data["id"]="major_"+str(major.id)
            child_data["text"]=major.name
            child_data["icon"]="/img/majortype2.png"
            
            tmpObj = {}
            tmpObj["majorid"] = str(major.id)
            child_data["data"]=tmpObj
    
            list_items=PBType.objects.filter(major=major)
            sub_child_list=[]
            if len(list_items)>0:
                for item in list_items:
                    sub_child_data = {}
                    sub_child_data["id"]="type_"+str(item.id)
                    sub_child_data["text"]=item.name
                    sub_child_data["icon"]=False
                    sub_child_list.append(sub_child_data)
            child_data["children"]=sub_child_list
            child_list.append(child_data)
        response_data["children"]=child_list
    
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def getworktypetree(request):
    id=request.GET.get('id', '')
    response_data = {}
    child_list=[]
        
    if id=='#':
        response_data["id"]="pbtype"
        response_data["text"]="类别"
        response_data["icon"]="/img/Catalog.png"
        response_data["state"]= {'opened':True }

        child_data = {}
        child_data["id"]="重大危险源"
        child_data["text"]="重大危险源"
        child_data["icon"]="/img/majortype2.png"
        child_data["children"]=[{"id":"1-1","text":"1-1"},{"id":"1-2","text":"1-2"},{"id":"1-3","text":"1-3"}]
        child_list.append(child_data)
        
        child_data = {}
        child_data["id"]="机械设备"
        child_data["text"]="机械设备"
        child_data["icon"]="/img/majortype2.png"
        child_data["children"]=[{"id":"1-1","text":"1-1"},{"id":"1-2","text":"1-2"},{"id":"1-3","text":"1-3"}]
        child_list.append(child_data)
        
        child_data = {}
        child_data["id"]="安全设施"
        child_data["text"]="安全设施"
        child_data["icon"]="/img/majortype2.png"
        child_data["children"]=[{"id":"1-1","text":"1-1"},{"id":"1-2","text":"1-2"},{"id":"1-3","text":"1-3"}]
        child_list.append(child_data)
        
        response_data["children"]=child_list
    
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def getpbmajortree(request):
    id=request.GET.get('id', '')
    response_data = {}
    child_list=[]
        
    if id=='#':
        response_data["id"]="pbtype"
        response_data["text"]="专业"
        response_data["icon"]="/img/Catalog.png"
        response_data["state"]= {'opened':True }
        major_items=UserMajor.objects.all()
        for major in major_items:
            child_data = {}
            child_data["id"]=major.name
            child_data["text"]=major.name
            child_data["icon"]=False
            child_data["state"]= {'opened':True }
            
            tmpObj = {}
            tmpObj["majorid"] = str(major.id)
            child_data["data"]=tmpObj
    
               
            child_list.append(child_data)
        response_data["children"]=child_list
    
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

def goujian_tree(request):
    try:
        id=request.GET.get('id', '')       
        gid=request.GET.get('gid', '')
        forbidList = [each[0] for each in CompGroup.objects.get(id=gid).precastbeam.all().values_list("id")]
        
        if id=='#':
            resultStr= "<ul><li data-jstree='{&quot;icon&quot;:&quot;/images/pbroot1.png&quot;}' id='_' class='jstree-open'>所有构件" + "<ul>"
            for each in UnitProject.objects.all():
                resultStr += "<li data-jstree='{&quot;icon&quot;:&quot;/img/buildings2.png&quot;}' id='unit_" + str(each.id) + \
                "' class='jstree-closed'>" + each.name +"</li>"
                
            resultStr += "</ul></li></ul>"
                
            result=resultStr
        
        elif id.startswith("unit_"):
            result = "<ul>"
            for each in Elevation.objects.filter(unitproject_id= int(id.replace("unit_","")) ):
                result+="<li data-jstree='{&quot;icon&quot;:&quot;/img/building2.png&quot;}' id='floor_"+ str(each.id)+"' ' class='jstree-closed'>"+ each.name +"</li>"
            
            result+="</ul>"
        
        else:
            list_items = PrecastBeam.objects.filter(elevation_id=int( id.replace("floor_","") )).exclude(id__in=forbidList)
            result = "<ul>"
            for item in list_items:
                result+="<li data-jstree='{&quot;icon&quot;:&quot;/img/floor.png&quot;}' id='"+item.drawnumber+"'>"+item.sign+"_"+item.elevation.name+"</li>"
            
            result+="</ul>"

    except:
        traceback.print_exc()
    
    return HttpResponse(result)

@login_required(login_url="/login/") 
def filterPblist(request):
    list_items = filterPbListRequest(request)
    

    response_data = {}
    response_data["pblist"]=[]
    for each in list_items:
        tmpObj = {}
        tmpObj["lvmdbid"] = each.lvmdbid
        response_data["pblist"].append(tmpObj)
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required(login_url="/login/") 
@check_permission_ajax
def updatepbstatus(request):
    response_data = {}
    pbstatusId = request.GET.get('pbstatusId', '')
    pbstatusNewTime = request.GET.get('pbstatusNewTime', '')
    #print pbstatusId
    #print pbstatusNewTime
    if PBStatusRecord.objects.get(id=pbstatusId):
        tgtPB = PBStatusRecord.objects.get(id=pbstatusId)
        tgtPB.time= pbstatusNewTime
        tgtPB.save()
        response_data["issuc"]="true"
        response_data["newtime"]=pbstatusNewTime
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@login_required(login_url="/login/") 
@check_permission_ajax
def delpbstatus(request):
    response_data = {}
    pbstatusId = request.GET.get('pbstatusId', '')
    pbId = request.GET.get('pbId', '')
    #print pbstatusId
    response_data["issuc"]="false"
    PBStatusRecord.objects.filter(precastbeam_id=pbId,status_id=pbstatusId).update(isactive=0)

    pb = PrecastBeam.objects.get(id=pbId)
    if pb.curstatus.id == int(pbstatusId):
        if PBStatusRecord.objects.filter(precastbeam_id=pbId,isactive=1).count()>0:
            laststat=PBStatusRecord.objects.filter(precastbeam_id=pbId,isactive=1).order_by("time")[0]
            pb.curstatus=laststat.status
            pb.curstatustime=laststat.time
            sumPercentage = PBStatusRecord.objects.filter(status= laststat.status,precastbeam=pb,isactive=True,
                                              percentage__isnull=False).aggregate(Sum('percentage'))["percentage__sum"]
            pb.curstatuspercent=sumPercentage
            pb.save()
        else:
            pb.curstatus=None
            pb.curstatustime=None
            pb.curstatuspercent=0
            pb.save()
    response_data["issuc"]="true"
    
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@login_required(login_url="/login/") 
def setpbcustominfo(request):
    response_data = {}
    custominfo = request.GET.get('custominfo', '')
#    print custominfo
    
    if CustomInfo.objects.filter(infotype='pblist').count()>0:
            customset=CustomInfo.objects.filter(infotype='pblist')[0]
            customset.custominfo=custominfo[:-1]
            customset.save()
    else:
        CustomInfo.objects.create(infotype= 'pblist',custominfo=custominfo)
        
    response_data["issuc"]="true"

    return HttpResponse(json.dumps(response_data), content_type="application/json") 

@login_required(login_url="/login/") 
def list_pbstatusrecord(request):
    list_items = PBStatusRecord.objects.filter(isactive=True)
    ElevationChoices = Elevation.objects.all()
    PBTypeChoices = PBType.objects.all()
    PBStatusChoices = PBStatus.objects.all()
    UnitProjectChoices = UnitProject.objects.all()
    pbelevationlist = []
    if request.method == 'GET':
        pbnumber = request.GET.get('number', '')
        pbelevationlist = request.GET.getlist('pbelevation', [])
        pbtype = request.GET.get('pbtype', '0')
        unitprj = request.GET.get('unitprj', '0')
        pbstatus = request.GET.get('pbstatus', '0')
        timerange = request.GET.get('timerange', '')
        if timerange:
            startdate=datetime.datetime.strptime(timerange.split('-')[0].strip()+" 00:00:00",'%Y/%m/%d %H:%M:%S')
            enddate=datetime.datetime.strptime(timerange.split('-')[1].strip()+" 23:59:59",'%Y/%m/%d %H:%M:%S')
            print startdate,enddate
            list_items=list_items.filter(time__gte=startdate,time__lte=enddate)
        if pbnumber:
            list_items=list_items.filter(precastbeam__sign__icontains=pbnumber)
            
        print pbelevationlist
        if pbelevationlist and len(pbelevationlist)>0:
            list_items=list_items.filter(precastbeam__elevation__in=pbelevationlist)

        if pbtype and (pbtype!='0'):
            list_items=list_items.filter(precastbeam__pbtype=pbtype)
            if pbtype.isdigit():
                pbtype=int(pbtype)
        if unitprj and (unitprj!='0'):
            list_items=list_items.filter(precastbeam__elevation__unitproject=unitprj)
            if unitprj.isdigit():
                unitprj=int(unitprj)
        if pbstatus and (pbstatus!='0'):
            list_items=list_items.filter(status=pbstatus)
            if pbstatus.isdigit():
                pbstatus=int(pbstatus)
                
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
    templateName='TaskAndFlow/list_pbstatusrecord.html'
    
    return render_to_response(templateName, RequestContext(request,locals()))

@login_required(login_url="/login/") 
def getpblisttimerange(request):
    response_data = {}
    response_data["pblist"]=[]
    pbstatus = request.GET.get('pbstatus', '')
    timerange = request.GET.get('timerange', '')
    
    #print selPbtypes
    try:
        filterpblist = filterPbListRequest(request)
        filterpbIdlist = [each.id for each in filterpblist]

        list_items = PBStatusRecord.objects.filter(precastbeam_id__in=filterpbIdlist,isactive=True)
        if timerange:
                startdate=datetime.datetime.strptime(timerange.split('-')[0].strip()+" 00:00:00",'%Y/%m/%d %H:%M:%S')
                enddate=datetime.datetime.strptime(timerange.split('-')[1].strip()+" 23:59:59",'%Y/%m/%d %H:%M:%S')
                #print startdate,enddate
                list_items=list_items.filter(time__gte=startdate,time__lte=enddate)
        if pbstatus and pbstatus!="":
            status = PBStatus.objects.get(id = pbstatus)
            if status.sequence ==0 :
                list_items=list_items.filter(status=pbstatus)
            else:
                list_items=list_items.filter(Q(status=pbstatus)&Q(isactive=True))
        else:
            pass
        
        list_items.query.group_by = ['precastbeam_id']

        pbidlist = list_items.values_list('precastbeam_id', flat=True)
        pbidlist = list(pbidlist)
        mappblvmid = { each.id: each.lvmdbid for each in PrecastBeam.objects.filter(id__in=pbidlist) }
        mapstatuscolor = { each.id: each.detailcounttype.rendercolor if each.detailcounttype else ""   for each in PBStatus.objects.all() }

        mapid2obj={}
        for each in list_items:
            tmpObj = {}
            tmpObj["lvmdbid"] = mappblvmid[each.precastbeam_id]
            tmpObj["color"] = mapstatuscolor[each.status_id]
            mapid2obj[each.precastbeam_id]=tmpObj
        response_data["pblist"]=mapid2obj.values()
    except Exception, e:
        traceback.print_exc()
        print e
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


@login_required(login_url="/login/") 
def filterPbByCountType(request):
    response_data = {}
    response_data["pblist"]=[]
    counttype = request.GET.get('counttype', '')
    iswholemodel = request.GET.get('_isWholeModel', '')
    
    #print selPbtypes
    try:
        filterpblist = filterPbListRequest(request)
        filterpbIdlist = [each.id for each in filterpblist]

        list_items = PBStatusRecord.objects.filter(precastbeam_id__in=filterpbIdlist,isactive=True)
        statuslist = []
        if counttype and counttype!="":
            if iswholemodel=="true":
                statuslist = PBStatus.objects.filter(roughcounttype_id=counttype).values_list('id', flat=True)
            else:
                statuslist = PBStatus.objects.filter(detailcounttype_id=counttype).values_list('id', flat=True)

        print statuslist
        list_items=list_items.filter(status_id__in=statuslist)
        
        list_items.query.group_by = ['precastbeam_id']

        pbidlist = list_items.values_list('precastbeam_id', flat=True)
        pbidlist = list(pbidlist)
        mappblvmid = { each.id: each.lvmdbid for each in PrecastBeam.objects.filter(id__in=pbidlist) }
        mapstatuscolor = { each.id: each.detailcounttype.rendercolor if each.detailcounttype else ""   for each in PBStatus.objects.all() }

        mapid2obj={}
        for each in list_items:
            tmpObj = {}
            tmpObj["lvmdbid"] = mappblvmid[each.precastbeam_id]
            tmpObj["color"] = mapstatuscolor[each.status_id]
            mapid2obj[each.precastbeam_id]=tmpObj
        response_data["pblist"]=mapid2obj.values()
    except Exception, e:
        traceback.print_exc()
        print e
    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/") 
def getpblist2(request):
    response_data = {}
    try:
        pbstatus = request.GET.get('pbstatus', '')
        timerange = request.GET.get('timerange', '')
        curUnitId = request.GET.get('curUnitId', '')
        
        list_items = PBStatusRecord.objects.filter(precastbeam__elevation__unitproject=curUnitId)
        if timerange:
            startdate,enddate = GetDateRange(timerange)
            list_items=list_items.filter(time__gte=startdate,time__lte=enddate)


        if pbstatus and pbstatus!="":
            status = PBStatus.objects.get(id = pbstatus)
            if status.sequence ==0 :
                list_items=list_items.filter(status=pbstatus)
            else:
                list_items=list_items.filter(Q(status=pbstatus)&Q(isactive=True))
        else:
            pass
            
        list_items.query.group_by = ['precastbeam_id']
        
        pbidlist = list_items.values_list('precastbeam_id', flat=True)
        pbidlist = list(pbidlist)

        list_items = PrecastBeam.objects.filter(Q(id__in=pbidlist))
        selElevations = request.GET.get('selElevations', '')
        #print len(selElevations)
        if len(selElevations)>0:
            ElevationIds = []
            for ElevationId in selElevations[:-1].split(","):
                ElevationIds.append(int(ElevationId))
            list_items=list_items.filter(elevation__in=ElevationIds)
        
        selPbtypes = request.GET.get('selPbtypes', '')
        #print len(selPbtypes)
        if len(selPbtypes)>0:
            PbtypesIds = []
            for PbtypesId in selPbtypes[:-1].split(","):
                PbtypesIds.append(int(PbtypesId))
            list_items=list_items.filter(pbtype__in=PbtypesIds)
        
        result=""
        pageinfo=""
        response_data = {}
        if True:
            paginator = Paginator(list_items ,6)
            listcount=len(list_items)
    
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
        
            try:
                list_items = paginator.page(page)
            except :
                list_items = paginator.page(paginator.num_pages)
           
            for item in list_items:
                result+="<tr>"
                result+="<td><input type='radio' onchange='changefunction()' name='pbcheck' value='%s'></td>" % (item.lvmdbid)
                result+="<td>%s</td>" % (item.sign,)
                result+="<td>%s</td>" % (item.curstatus,)
                result+="</tr>"
            
            try:
                pageinfo+="<li><a onclick='changepage2PageStatus(1)'>首页</a></li>"
                if list_items.number>1:
                    pageinfo+="<li><a onclick='changepage2PageStatus(%s)'><i class='fa fa-chevron-left'></i></a></li>" % (list_items.previous_page_number(),) 
                pageinfo+="<li><a>第 %s 页，共 %s页</a></li>" % (list_items.number,paginator.num_pages)
                if list_items.has_next:
                    pageinfo+="<li><a onclick='changepage2PageStatus(%s)'><i class='fa fa-chevron-right'></i></a></li>" % (list_items.next_page_number(),)
                pageinfo+="<li><a onclick='changepage2PageStatus(%s)'>尾页</a></li>" % (paginator.num_pages,)
            except Exception, e:
                print e
        
        response_data["pageinfo"]=pageinfo
        response_data["pblist"] = result
        response_data["issuc"]="true"
    except Exception, e: 
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  

@login_required(login_url="/login/")
def goujian_statusmanager(request):
  
    list_items = PBType.objects.all()
    list_factoryarea = FactoryArea.objects.all()
    list_flowtemplate = FlowTemplate.objects.all()
    list_formtemplate = BiaoDanMuBan.objects.all()
    list_color = StatusCountType.objects.all().order_by('sequence')
    list_user = getPrjUserlist()
    t = get_template('TaskAndFlow/goujian/statusmanager.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

@login_required(login_url="/login/")
@csrf_exempt
def goujian_glys(request):
    try:
        rdata= {}
        rdata['goujians'] = []
        goujians = None
        if request.method == 'GET':
            nodeid = request.GET.get('id')
            major = request.GET.get('major',None)
            # parents ["unitprj_1", "model", "#"]
            euid = nodeid.split('_')[1]
            if "unitprj" in nodeid:
                # goujians = PrecastBeam.objects.filter(elevation__unitproject_id=int(euid))
                # if major:
                #     goujians = goujians.filter(pbtype__major_id=int(major))
                pass
            elif "floor" in nodeid:
                goujians = PrecastBeam.objects.filter(elevation_id=int(euid)).order_by("sign")
                if major:
                    goujians = goujians.filter(pbtype__major_id=int(major)) 
            elif "zone" in nodeid:
                goujians = PrecastBeam.objects.filter(zone_id=int(euid)).order_by("sign")
                if major:
                    goujians = goujians.filter(pbtype__major_id=int(major)) 
            else:
                pass

            if goujians:
                setpb =set([each.relatedid for each in Monitoringelement.objects.filter(typetable="构件")])
                for g in goujians:
                    if g.id not in setpb:
                        continue
                    louceng = str(g.elevation.id) 
                    loudong = str(g.elevation.unitproject_id)
                    rdata['goujians'].append({"id":g.id,"sign":g.sign,"class":"floor_"+louceng+" "+"unitprj_"+loudong})
        return HttpResponse(json.dumps(rdata))
    except:
        traceback.print_exc()
        return HttpResponse("{'res':'error'}",content_type="application/json")

@login_required(login_url="/login/")
@csrf_exempt
def goujian_glrw(request):
    try:
        rdata= {}
        rdata['renwu'] = []
        renwus = None
        if request.method == 'GET':
            gid = request.GET.get('id')
            print gid
            if gid=="#":
                renwus = ProjectTask.objects.all()
            else:
                euid = gid.split('_')[1]
                renwus = ProjectTask.objects.filter(parentid_id=euid)
        if renwus:
            for g in renwus:
                rdata['renwu'].append({"id":g.id,"name":g.name})
        return HttpResponse(json.dumps(rdata))
    except:
        traceback.print_exc()
        rdata = {"name":bda.name,"content":bda.content}
        return HttpResponse("{'res':'error'}",content_type="application/json")


@login_required(login_url="/login/")
def goujian_glys_mobile(request):
    rdata= {}
    rdata['issuc'] = "true"
    rdata['glys'] = []
    try:
        nodeid = request.GET.get('nodeid','0')
        eletype = request.GET.get('eletype','')
        major = request.GET.get('major',None)

        glyslist = None
        euid = nodeid.split('_')[1]
        if eletype=="pbgrp":#分区
            if "unitprj" in nodeid:
                zonelist = ZoneElevation.objects.filter(elevation__unitproject_id=int(euid)).values_list('zone_id', flat=True)
                glyslist = Pbgroup.objects.filter(zone_id__in=zonelist)
            elif "floor" in nodeid:
                zonelist =ZoneElevation.objects.filter(elevation_id=int(euid)).values_list('zone_id', flat=True)
                glyslist = Pbgroup.objects.filter(zone_id__in=zonelist)
                
            elif "zone" in nodeid:
                glyslist = Pbgroup.objects.filter(zone__id=int(euid))
            else:
                pass

        if glyslist:
            setpbgrp =set([each.relatedid for each in Monitoringelement.objects.filter(typetable="构件组")])
            for g in glyslist:
                if g.id not in setpbgrp:
                    continue
                if major and g.pbtype.major_id!=int(major):
                    continue
                tmp = {}
                tmp["id"] = g.id
                tmp["name"] = g.number
                if tmp not in rdata['glys']:
                    rdata['glys'].append(tmp)
    except:
        traceback.print_exc()
        rdata['issuc'] = "false"
        rdata['error'] = "获取数据失败！"
    return HttpResponse(json.dumps(rdata))

@login_required(login_url="/login/")
def goujian_glys_pbtype(request):
    rdata= {}
    rdata['issuc'] = "true"
    rdata['glys'] = []
    try:
        nodeid = request.GET.get('id','0')

        glyslist = None
        typeid = nodeid.split('_')[1]
        pbtype = PBType.objects.get(id=typeid)
        if pbtype.isprebuilt:
            glyslist = PrecastBeam.objects.filter(pbtype=pbtype)
        else:
            glyslist = Pbgroup.objects.filter(pbtype=pbtype)

        if glyslist:
            for g in glyslist:
                tmp = {}
                tmp["id"] = g.id
                tmp["name"] = g.number
                if tmp not in rdata['glys']:
                    rdata['glys'].append(tmp)
    except:
        traceback.print_exc()
        rdata['issuc'] = "false"
        rdata['error'] = "获取数据失败！"
    return HttpResponse(json.dumps(rdata))


@login_required(login_url="/login/")
def get_glys_qrcode(request):
    rdata= {}
    rdata['issuc'] = "true"
    rdata['qrcode'] = []
    try:
        typetable = request.GET.get('typetable','')
        relatedids = eval(request.GET.get('relatedids','[]'))
        print typetable
        for relatedid in relatedids:
            if Monitoringelement.objects.filter(typetable=typetable,relatedid=relatedid).count()>0:
                ele = Monitoringelement.objects.filter(typetable=typetable,relatedid=relatedid)[0]
                rdata['qrcode'].append(ele.qrcode)
            else:
                rdata['issuc'] = "false"
                rdata['error'] = typetable+relatedid+"没有设置二维码"
                break
        if typetable=="构件" and PrecastBeam.objects.filter(id__in=relatedids).values('pbtype_id').distinct().count()>1:
            typelist = PrecastBeam.objects.filter(id__in=relatedids).values('pbtype_id').distinct().values_list('pbtype_id', flat=True)
            types = PBType.objects.filter(id__in=typelist)
            rdata['issuc'] = "false"
            rdata['error'] = "只能同时选择一种构件类型，已选:"
            for each in types:
                rdata['error'] += each.name+","
            rdata['error'] =rdata['error'][:-1]
       
    except:
        traceback.print_exc()
        rdata['issuc'] = "false"
        rdata['error'] = "获取数据失败！"
    return HttpResponse(json.dumps(rdata))

@login_required(login_url="/login/")
def getelebyqrcode(request):
    rdata= {}
    rdata['issuc'] = "true"
    rdata['element'] = []
    rdata['elementinfo'] = ""
    try:
        qrcode = request.GET.get('qrcode','')
        
        ele =  Monitoringelement.objects.get(qrcode = qrcode)
        
        tmp = {}
        tmp["typetable"] = ele.typetable
        tmp["relatedid"] = ele.relatedid
        rdata['element'].append(tmp)
        rdata['elementinfo'] = GetRelateTypeInfo(ele.typetable,ele.relatedid)
    except:
        traceback.print_exc()
        rdata['issuc'] = "false"
        rdata['error'] = "获取数据失败！"
    return HttpResponse(json.dumps(rdata))

@csrf_exempt
@login_required(login_url="/login/") 
def getelestatuslist(request):
    response_data={}
    response_data['issuc'] = "true"
    response_data["statuslist"]=[]
    try: 
        elelist = eval(request.POST.get("elelist"))

        typeset = set()
        relatedidset = set()
        for ele in elelist:
            typeset.add(ele["typetable"])
            relatedidset.add(ele["relatedid"])
        print typeset
        print relatedidset
        if len(typeset)>1:
            error = "只能同时选择一种类型进行扫码，已选:"
            for each in list(typeset):
                error += each+","
            error = error[:-1]
            raise Exception(error)

        if list(typeset)[0]=="构件" and PrecastBeam.objects.filter(id__in=list(relatedidset)).values('pbtype_id').distinct().count()>1:
            typelist = PrecastBeam.objects.filter(id__in=list(relatedidset)).values('pbtype_id').distinct().values_list('pbtype_id', flat=True)
            types = PBType.objects.filter(id__in=typelist)
            error = "只能同时选择一种构件类型，已选:"
            for each in types:
                error += each.name+","
            error = error[:-1]
            raise Exception(error)

        if elelist:
            goujianObj = Monitoringelement.objects.get(typetable=elelist[0]["typetable"],relatedid=elelist[0]["relatedid"])
            if goujianObj:

                statuslist = fetchStatusList(goujianObj, request.user)
                    
                curstatus = getCurStatus(goujianObj)

                if statuslist:
                    for each in statuslist:
                        tmpObj={}
                        tmpObj["id"]=each.id
                        tmpObj["statusname"]=each.statusname
                        response_data["statuslist"].append(tmpObj)
                
                if curstatus and curstatus.nextstatus in statuslist:
                    response_data["defaultstatus"] = curstatus.nextstatus_id
                elif curstatus in statuslist:
                    response_data["defaultstatus"] = curstatus.id

    except Exception, e: 
        traceback.print_exc()
        response_data['issuc'] = "false"
        response_data['error'] = '%s' % e
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")   

@csrf_exempt
@login_required(login_url="/login/") 
def getelestatuslisthis(request):
    response_data={}
    response_data['issuc'] = "true"
    response_data["statuslist"]=[]
    try: 
        elelist = eval(request.POST.get("elelist"))

        typeset = set()
        relatedidset = set()
        for ele in elelist:
            typeset.add(ele["typetable"])
            relatedidset.add(ele["relatedid"])
        print typeset
        print relatedidset
        if len(typeset)>1:
            error = "只能同时选择一种类型进行扫码，已选:"
            for each in list(typeset):
                error += each+","
            error = error[:-1]
            raise Exception(error)

        if list(typeset)[0]=="构件" and PrecastBeam.objects.filter(id__in=list(relatedidset)).values('pbtype_id').distinct().count()>1:
            typelist = PrecastBeam.objects.filter(id__in=list(relatedidset)).values('pbtype_id').distinct().values_list('pbtype_id', flat=True)
            types = PBType.objects.filter(id__in=typelist)
            error = "只能同时选择一种构件类型，已选:"
            for each in types:
                error += each.name+","
            error = error[:-1]
            raise Exception(error)

        if elelist:
            goujianObj = Monitoringelement.objects.get(typetable=elelist[0]["typetable"],relatedid=elelist[0]["relatedid"])
            if goujianObj:
                statuslist_zhijian = fetchZhiJianStatusList(goujianObj)
                if statuslist_zhijian:
                    for each in statuslist_zhijian:
                        tmpObj={}
                        tmpObj["id"]=each
                        tmpObj["statusname"]=PBStatus.objects.get(id=each).statusname
                        response_data["statuslist"].append(tmpObj)
        
    except Exception, e: 
        traceback.print_exc()
        response_data['issuc'] = "false"
        response_data['error'] = '%s' % e
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")    

@login_required(login_url="/login/")
@check_permission_ajax
def getrelatefilelist(request):
    response_data = {}
    response_data["issuc"]="false"
    response_data["filelist"]=[]
    try:
        RelateId = int(request.GET.get('RelateId', '0'))
        RelateType = request.GET.get('RelateType', '构件')
        filelist = Doc2Relate.objects.filter(relatetype=RelateType,relateid=RelateId)
        for each in filelist:
            tmp={}
            tmp['fileid']=each.document.id
            tmp['filename']=each.document.name
            tmp['fileshortname']=each.document.shortname
            tmp['filepath']=str(each.document.filepath)
            response_data["filelist"].append(tmp)

        response_data["issuc"]="true"
    except:
        traceback.print_exc()
        response_data['issuc'] = "false"
        response_data['error'] = "获取失败！"
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def goujian_pbcountdesc(request):
    rdata= {}
    rdata['issuc'] = "true"
    rdata['list_obj_weekly'] = {}
    rdata['list_obj_monthly'] = {}
    try:
        list_obj_weekly={}
        weekstartdate = datetime.date.today()+datetime.timedelta(0-datetime.date.today().weekday())
        weektenddate = weekstartdate + datetime.timedelta(7)
        rdata['weekstartdate'] = weekstartdate.strftime("%Y/%m/%d")
        rdata['weektenddate'] = weektenddate.strftime("%Y/%m/%d")
    
        maptypemajor = { each.id: each.major.name for each in PBType.objects.all() }
        mapstatusname = { each.id: each.statusname for each in PBStatus.objects.all() }

        pblist = PrecastBeam.objects.filter(curstatustime__isnull=False,curstatustime__gt=weekstartdate,curstatustime__lt=weektenddate)
        for each in pblist:
            if list_obj_weekly.has_key(maptypemajor[each.pbtype_id]):
                if list_obj_weekly[maptypemajor[each.pbtype_id]].has_key(mapstatusname[each.curstatus_id]):
                    if len(list_obj_weekly[maptypemajor[each.pbtype_id]][mapstatusname[each.curstatus_id]])<5:
                        list_obj_weekly[maptypemajor[each.pbtype_id]][mapstatusname[each.curstatus_id]].append(each.number)
                else:
                    list_obj_weekly[maptypemajor[each.pbtype_id]][mapstatusname[each.curstatus_id]]=[each.number]
            else:
                list_obj_weekly[maptypemajor[each.pbtype_id]]={mapstatusname[each.curstatus_id]:[each.number]}

        rdata['list_obj_weekly']=list_obj_weekly

        list_obj_monthly={}
        curdate = datetime.date.today()
        monthstartdate = curdate +datetime.timedelta(1-curdate.day)
        monthstartend =  datetime.datetime.now()
        monthenddate = curdate+datetime.timedelta(0-curdate.day+calendar.monthrange(curdate.year, curdate.month)[1])
        rdata['monthstartdate'] = monthstartdate.strftime("%Y/%m/%d")
        rdata['monthenddate'] = monthenddate.strftime("%Y/%m/%d")
    

        pblist = PrecastBeam.objects.filter(curstatustime__isnull=False,curstatustime__gte=monthstartdate,curstatustime__lt=monthstartend)
        for each in pblist:
            if list_obj_monthly.has_key(maptypemajor[each.pbtype_id]):
                if list_obj_monthly[maptypemajor[each.pbtype_id]].has_key(mapstatusname[each.curstatus_id]):
                    if len(list_obj_monthly[maptypemajor[each.pbtype_id]][mapstatusname[each.curstatus_id]])<5:
                        list_obj_monthly[maptypemajor[each.pbtype_id]][mapstatusname[each.curstatus_id]].append(each.number)
                else:
                    list_obj_monthly[maptypemajor[each.pbtype_id]][mapstatusname[each.curstatus_id]]=[each.number]
            else:
                list_obj_monthly[maptypemajor[each.pbtype_id]] = {mapstatusname[each.curstatus_id]:[each.number]}

        rdata['list_obj_monthly']=list_obj_monthly
       
    except:
        traceback.print_exc()
        rdata['issuc'] = "false"
        rdata['error'] = "获取数据失败！"
    return HttpResponse(json.dumps(rdata))