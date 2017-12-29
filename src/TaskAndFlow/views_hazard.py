# -*- coding: utf-8 -*-
from TaskAndFlow.models import Hazardevent,Hazardlisthistory,HazardStatus,UnitProject,Elevation
from UserAndPrj.models import UserMajor
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import loader, Context, RequestContext
import json,traceback,datetime
from TaskAndFlow.utility import *
from TaskAndFlow.utility_hazard import *
from Scc4PM.settings import *
from UserPrjConfig.permissions import *

def getroot(j):
    tmp = j
    while True:
        if tmp.parent_id:
            tmp=tmp.parent
        else:
            return tmp.hazard_name

def getfullname(each):#获取危险源全名
    relateid = each.relatedspace_id
    if each.relatedspace_type == u'单位工程':
        kjys =KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name +":"+ UnitProject.objects.get(id=relateid).name

    elif each.relatedspace_type == u'楼层':
        lc = Elevation.objects.get(id=relateid)

        kjys =KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name +":"+  UnitProject.objects.get(id=lc.unitproject_id).name + lc.name
    elif each.relatedspace_type == u'分区':

        kjys =KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name +":"+  Zone.objects.get(id=relateid).name
    else:
        kjys = KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name
    return kjys


@csrf_exempt
@login_required(login_url="/login/")
def hazardopt(request):
    try:
        response_data={}
        if request.method=='POST':
            opt = request.POST.get('opt','create')
            if(opt=="create"):
                if not request.user.has_perm("编辑危险源"):
                    return HttpResponse(status=403)
                kj = request.POST.get('kj','')
                majorid = request.POST.get('majorid','0')
                isctr = request.POST.get('isctr','1')
                describ = request.POST.get('describ','')
                days = request.POST.get('days','null')
                hardid = request.POST.get('hardid','')
                gid = request.POST.get('id',None)
                gid = int(gid) if gid else None
                hardcode = KnowledgeHazardlist.objects.get(id=int(hardid)).hazard_code
                # kj = request.POST.get('kj','0')
                # unitprj_1 floor_178 113zone_1
                # kjfullname=''
                # newhahis=None
                # if len(Hazardlisthistory.objects.filter(his_date=datetime.date.today()))==0:
                #     newhahis = Hazardlisthistory.objects.create(his_date=datetime.date.today())
                # else:
                #     newhahis = Hazardlisthistory.objects.get(his_date=datetime.date.today())
                rid = 0
                if kj != 'model' and kj:
                    kjys = kj.split('_')
                    kjty = kjys[0]
                    kjid = kjys[1]
                    if kjty == 'unitprj':
                        kjty = u'单位工程'
                    elif kjty == 'floor':
                        kjty = u'楼层'
                        # lc = Elevation.objects.get(id=int(kjid))
                        # kjfullname = UnitProject.objects.get(id=lc.unitproject_id).name + lc.name + u'层'
                    elif 'zone' in kjty:
                        kjty = u'分区'

                    if gid:
                        newha = Hazardevent.objects.filter(id=gid)
                        if newha[0].curstatus_id!=int(isctr):
                            if HazardStatus.objects.get(id=int(isctr)).statusname==u"不受控":
                                rid = gid
                        newha.update(name=describ,duration=int(days),
                            curstatus_id=int(isctr),relatedspace_type=kjty,relatedspace_id=int(kjid))
                    else:
                        
                        if days != 'null':
                            days = int(days)
                        else:
                            #查询昨天是否有该危险源
                            day1 = datetime.date.today() + datetime.timedelta(-1)
                            beforeha = Hazardevent.objects.filter(his_date=day1,hazard_code=hardcode,relatedspace_id=int(kjid))
                            days = beforeha[0].duration+1 if len(beforeha)>0 else 1
                        newha = Hazardevent.objects.create(hazard_code=hardcode,name=describ,duration=days,
                                curstatus_id=int(isctr),relatedspace_type=kjty,relatedspace_id=int(kjid),his_date=datetime.date.today())
                        if newha.curstatus.statusname==u"不受控":
                            rid = newha.id

                response_data['rid']=rid
            elif(opt=="del"):
                if not request.user.has_perm("删除危险源"):
                    return HttpResponse(status=403)
                Hazardevent.objects.filter(his_date=datetime.date.today()).delete()
            elif(opt=="delone"):
                if not request.user.has_perm("删除危险源"):
                    return HttpResponse(status=403)

                gid = request.POST.get('id',None)
                if gid:
                    Hazardevent.objects.filter(id=int(gid)).delete()
            elif(opt=="copy"):#复制昨天，前天，大前天
                if not request.user.has_perm("编辑危险源"):
                    return HttpResponse(status=403)
                d = datetime.date.today()
                dtype = request.POST.get('dtype','before1')# dtype= 1, 2, 3
                d = d + datetime.timedelta(-int(dtype[-1]))
                hazardlist = []
                zuotian = datetime.date.today()+datetime.timedelta(-1)
                
                for each in Hazardevent.objects.filter(his_date=d):
                    tmp={}
                    knowl = KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code)
                    tmp['major'] = knowl.major.name
                    tmp['isctr'] = each.curstatus_id
                    tmp['describe'] = each.name
                    tmp['wxy'] = knowl.hazard_name
                    tmp['weixianku'] = 'weixianku_'+ str(knowl.id)
                    if len(Hazardevent.objects.filter(his_date=zuotian,hazard_code=each.hazard_code,
                                relatedspace_type=each.relatedspace_type,relatedspace_id=each.relatedspace_id)[:2])>0:#昨天有 持续天数+1
                        tmp['days'] = each.duration + 1
                    else:
                        tmp['days'] = 1
                    tmp['ji'] = knowl.hazard_grade


                    relateid = each.relatedspace_id
                    if each.relatedspace_type == u'单位工程':
                        tmp['kjys'] = UnitProject.objects.get(id=relateid).name
                        tmp['val'] = 'unitprj_' + str(each.relatedspace_id)
                    elif each.relatedspace_type == u'楼层':
                        lc = Elevation.objects.get(id=relateid)
                        tmp['val'] = 'floor_' + str(each.relatedspace_id)
                        tmp['kjys'] = UnitProject.objects.get(id=lc.unitproject_id).name + lc.name + u'层'
                    elif each.relatedspace_type == u'分区':
                        tmp['val'] = 'zone_' + str(each.relatedspace_id)
                        tmp['kjys'] = Zone.objects.get(id=relateid).name
                    else:
                        tmp['kjys'] = '选择空间'
                        tmp['val'] = 'model'
                    hazardlist.append(tmp)
                response_data['data']=hazardlist
            elif(opt=='tongjiClosedHazard'):#统计关闭的危险源
                day = datetime.date.today()
                todayha = Hazardevent.objects.filter(curstatus__statusname=u'关闭').order_by('-id')
                data = []
                for today in todayha:
                    hazard_name = KnowledgeHazardlist.objects.get(hazard_code=today.hazard_code).hazard_name
                    tmp={'hazard':getfullname(today),'closedate':str(today.his_date),u'受控':[],u'不受控':[]}

                    beforeha = Hazardevent.objects.filter(hazard_code=today.hazard_code,his_date__lt=today.his_date,
                                relatedspace_type=today.relatedspace_type,relatedspace_id=today.relatedspace_id,).order_by('-id')
                    start = None
                    end = None
                    status = None
                    cout = len(beforeha)
                    for before in beforeha:
                        if before.curstatus.statusname == u"关闭":
                            if status and start and end:
                                tmp[status].append(str(start)+'~'+str(end))
                            break
                        cout -= 1
                        his_date = before.his_date
                        tmp_status = before.curstatus.statusname
                        if not start:
                            start,end = his_date,his_date
                            status = tmp_status
                        elif (end-his_date).days==1 and status==tmp_status:
                            start = his_date
                        elif (end-his_date).days>1 or status!=tmp_status:
                            tmp[status].append(str(start)+'~'+str(end))
                            start,end = his_date,his_date
                            status = tmp_status

                        if cout==0:
                            tmp[status].append(str(start)+'~'+str(end))
                    data.append(tmp)
                response_data['data']=data
            response_data["res"]="succ"
            # print type(json.dumps(response_data))
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        traceback.print_exc()

@csrf_exempt
@login_required(login_url="/login/")
def hazard_task(request):
    try:
        if request.method=='GET':
            if not request.user.has_perm("编辑危险源"):
                return HttpResponseRedirect('/error_403/')

            fangAnlist = Technical.objects.all()
            pts = ProjectTaskHazard.objects.all()
            hazard_task = []
            for each in pts:
                tmp={}
                kjys,val = getkjname(each)
                tmp['kjys'] = kjys
                tmp['kjval'] = val
                tmp['projecttask']=each.projecttask if each.projecttask else {'id':'model','name':u'选择任务'}
                tmp['technical']=each.technical if each.technical else {'id':'model','name':u'选择方案'}
                # tmp['hazard_code']=each.projecttask
                knowl = KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code)
                tmp['wxy'] = knowl.hazard_name
                tmp['kjval'] = val
                tmp['weixianku'] = 'weixianku_'+ str(knowl.id)
                tmp['ji'] = knowl.hazard_grade

                hazard_task.append(tmp)
            
            templateName = 'TaskAndFlow/flowtemplate/hazard_task.html'
            return render_to_response(templateName, RequestContext(request, locals()))
        elif request.method=='POST':
            response_data={}
            response_data["res"]="succ"
            opt = request.POST.get('opt','')
            if opt=='del':
                if not request.user.has_perm("编辑危险源"):
                    return HttpResponse(status=403)
                ProjectTaskHazard.objects.all().delete()
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            elif opt=='create':
                if not request.user.has_perm("编辑危险源"):
                    return HttpResponse(status=403)
                projecttask=None
                hazard_code=None
                relatedspace_type=None
                relatedspace_id=None
                kj = request.POST.get('kj',None)
                if kj != 'model' and kj:
                    kjys = kj.split('_')
                    kjty = kjys[0]
                    relatedspace_id = int(kjys[1])
                    if kjty == 'unitprj':
                        relatedspace_type = u'单位工程'
                    elif kjty == 'floor':
                        relatedspace_type = u'楼层'
                    elif 'zone' in kjty:
                        relatedspace_type = u'分区'

                hardid = int(request.POST.get('hardid',None))
                hardcode = KnowledgeHazardlist.objects.get(id=hardid).hazard_code
                renwu = request.POST.get('renwu',None)
                if renwu != 'renwu_model' and renwu:
                    projecttask = int(renwu.split('_')[1])
                fangan = request.POST.get('fangan',None)
                if fangan == 'model':
                    fangan = None

                # floor_256 901 renwu_2227
                print projecttask,hardcode,relatedspace_type,relatedspace_id,fangan
                ProjectTaskHazard.objects.create(projecttask_id=projecttask,technical_id=fangan,hazard_code=hardcode,
                                relatedspace_type=relatedspace_type,relatedspace_id=relatedspace_id)
                return HttpResponse(json.dumps(response_data), content_type="application/json")

    except:
        traceback.print_exc()

@login_required(login_url="/login/")
@check_permission
def hazard_general(request):
    try:

        majorList = UserMajor.objects.all()
        curMajorId = getUserMajor(request.user)
        print "111111111111"
        hazard_status_list = HazardStatus.objects.all()
        #当天危险源
        hazardlist = []
        for each in Hazardevent.objects.filter(his_date=datetime.date.today()).exclude(curstatus__statusname=u'关闭').order_by('hazard_code'):
            tmp={}
            knowl = KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code)
            tmp['major'] = knowl.major.name
            tmp['isctr'] = each.curstatus_id
            tmp['describe'] = each.name
            tmp['wxy'] = knowl.hazard_name
            tmp['weixianku'] = 'weixianku_'+ str(knowl.id)
            tmp['duration'] = each.duration
            tmp['ji'] = knowl.hazard_grade
            kjys,val = getkjname(each)
            tmp['kjys'] = kjys
            tmp['val'] = val
            tmp['id'] = each.id
            hazardlist.append(tmp)


        templateName = 'TaskAndFlow/flowtemplate/anquan_hazard.html'
        return render_to_response(templateName, RequestContext(request, locals()))
    except:
        traceback.print_exc()


@csrf_exempt
@login_required(login_url="/login/")
def hazard_list(request):
    if checkMobile(request):
        try:
            if request.method=="GET":
                if not perm_check(request):
                    return HttpResponseRedirect('/error_403/')

                config={}
                ticket, appid, _ = fetch_ticket()
                
                sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.path)
                
                config = sign.sign()
                config["appid"] = appid

                hazard_status_list = HazardStatus.objects.all()
                hazardlist = []
                for each in Hazardevent.objects.filter(his_date=datetime.date.today()).order_by('hazard_code'):
                    tmp={}
                    tmp['id']=each.id
                    tmp['isctr'] = each.curstatus_id
                    info = GetRelateTypeInfo(each.relatedspace_type,each.relatedspace_id)
                    tmp['text'] = info + KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name
                    hazardlist.append(tmp)
                templateName = 'TaskAndFlow/anquan_hazard_list.html'
                return render_to_response(templateName, RequestContext(request, locals()))
            elif request.method=="POST":#手机端改变危险源状态， 选择附件
                if not perm_check(request):
                    return HttpResponse(status=403)
                response_data={}
                hazardid= request.POST.get('hazardid','')
                status = request.POST.get('status','0')
                changeha = Hazardevent.objects.get(id=hazardid)
                skid = HazardStatus.objects.get(statusname=u'受控').id
                bskid = HazardStatus.objects.get(statusname=u'不受控').id
                if int(status)==skid:
                    changeha.curstatus_id = bskid
                    response_data['statusid'] = bskid
                    response_data['status']=u'不受控'

                else:
                    changeha.curstatus_id = skid
                    response_data['statusid'] = skid
                    response_data['status']=u'受控'

                changeha.save()
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        except:
            traceback.print_exc()
    else:
        # 网页端改变危险源状态， 选择附件
        response_data={}
        hazardid= request.POST.get('hazardid','')
        try:
            changeha = Hazardevent.objects.get(id=hazardid)
            status = changeha.curstatus_id

            skid = HazardStatus.objects.get(statusname=u'受控').id
            bskid = HazardStatus.objects.get(statusname=u'不受控').id
            if status==bskid:
                changeha.curstatus_id = skid
                response_data['statusid'] = skid
                response_data['status']=u'受控'

            else:
                changeha.curstatus_id =bskid
                response_data['statusid'] = bskid
                response_data['status']=u'不受控'
            changeha.save()
        except:
            traceback.print_exc()
        return HttpResponse(json.dumps(response_data), content_type="application/json")
@csrf_exempt
@login_required(login_url="/login/")
@check_permission_ajax
def hazard_attachment(request):
    try:
        if request.method=="POST":
            haid = request.POST.get('haid','0')
            imageserverids = eval(request.POST.get('imageserverids','[]'))

            uploadfile_weixin(imageserverids,haid,'hazardevent', '危险源', request.user, haid)
        return HttpResponse(json.dumps({}), content_type="application/json")
    except:
        traceback.print_exc()