# -*- coding: utf-8 -*-
'''

@author: fgf
'''

import traceback

from django.shortcuts import render,render_to_response
from Assist.models import BiaoDan,BiaoDanMuBan,BiaoDanType,Formtag,Formtempandformtag
from UserAndPrj.models import UserMajor,Project
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template import loader,Context,RequestContext
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.http import HttpResponse
import json,time
from TaskAndFlow.models import UnitProject,Zone,Elevation,PrecastBeam,projectevent
from TaskAndFlow.utility_flowtemplate import getRijiMsg
from Scc4PM.settings import CURRENT_PROJECT_ID#项目id
from utility import *
import datetime
@login_required(login_url="/login/")
@csrf_exempt
def biaodan_biaodan(request):
    try:
        if request.method == 'POST':
            table_data = json.loads(request.body)
            creater = request.user
            bid = table_data.get('id', None)
            name = table_data.get('name', None)
            content = table_data.get('content',None)
            major = table_data.get('major',None)
            formtype= table_data.get('formtype',None)
            mbId = table_data.get('mbId',None)

            if(bid==-1):#新增表单
                if name and content:
                    bda = BiaoDan(name =name ,content=content,creater=creater,formtemplet_id=int(mbId),
                                    major_id=int(major),formtype_id=int(formtype))
                    bda.save()
                    bdid = bda.id
                    rdata = {'id':bdid}


                    rdata['res']='succ'
                    print "add succ"
                    return HttpResponse(json.dumps(rdata))
            else:#修改表单
                bda = BiaoDan.objects.get(id=int(bid))
                if name:
                    bda.name = name
                if content:
                    bda.content = content
                if major:
                    bda.major_id=int(major)
                if formtype:
                    bda.formtype_id=int(formtype)
                bda.save()
                print "edit succ"
                rdata = {'id':bid}
                rdata['res']='succ'
                return HttpResponse(json.dumps(rdata))

        elif request.method == 'DELETE':
            table_data = json.loads(request.body)
            delID = table_data.get('id', None)
            if delID:
                bda = BiaoDan.objects.get(id=int(delID))
                bda.delete()
            return HttpResponse("{'res':'succ'}")
        elif request.method == 'GET':
            # table_data = json.loads(request.GET.get('id'))
            cID = request.GET.get('id')
            if cID:
                bda = BiaoDan.objects.get(id=int(cID))
                rdata={}
                rdata ["name"]=bda.name
                rdata ["content"]=bda.content
                rdata ["major"]=bda.major_id
                rdata ["formtype"]=bda.formtype_id
                rdata ["createdate"]=bda.createdate.strftime("%Y-%m-%d")

                rdata['res']='succ'
                return HttpResponse(json.dumps(rdata))
        # return "{'res':'succ'}"
        # return render_to_response('TaskAndFlow/filemanager/filemanager.html', RequestContext(request,locals()))
    except:
        traceback.print_exc()
        return HttpResponse("{'res':'error'}",content_type="application/json")
#单位工程名称
def get_projectname(glys,kj):
    try:
        for ys in eval(glys):
            if ys["typetable"]==u'构件':
                return PrecastBeam.objects.get(id=ys["relatedid"]).elevation.unitproject.name
        if kj != 'model' and kj:
            print kj
            kjys = kj.split('_')
            kjty = kjys[0]
            kjid = kjys[1]
            if kjty == 'unitprj':
                # print UnitProject.objects.get(id=kjid).name
                return UnitProject.objects.get(id=kjid).name

            elif kjty == 'floor':
                lc = Elevation.objects.get(id=kjid)
                return UnitProject.objects.get(id=lc.unitproject_id).name + lc.name + u'层'

            elif 'zone' in kjty:
                return Zone.objects.get(id=kjid).name
    except:
        traceback.print_exc()
        return "单位工程填入失败"

#安全日记
def get_anquanriji(rijidate):
    try:
        msg = getRijiMsg(rijidate,"安全问题")
        return msg
    except:
        traceback.print_exc()
        return "安全日记填入失败"

#质量日记
def get_zhiliangriji(rijidate):
    try:
        msg = getRijiMsg(rijidate,"质量问题")
        return msg
    except:
        traceback.print_exc()
        return "质量日记填入失败"

def get_customdate(rijidate):
    try:
        if not rijidate:
            rijidate=str(datetime.date.today())
        rijidate = datetime.datetime.strptime(str(rijidate),'%Y-%m-%d')
        rijidate = rijidate.strftime("%Y年%m月%d日")
        return rijidate
    except:
        traceback.print_exc()
        return " 年 月 日 "

def get_weekdaystr(rijidate):
    try:
        if not rijidate:
            rijidate=str(datetime.date.today())
        rijidate = datetime.datetime.strptime(str(rijidate),'%Y-%m-%d')
        return get_week_day(rijidate)
    except:
        traceback.print_exc()
        return " 星期  "

def get_jindu(rijidate,index):
    try:
        if not rijidate:
            rijidate=str(datetime.date.today())
        #rijidate = datetime.datetime.strptime(str(rijidate),'%Y-%m-%d')
        startdate=datetime.datetime.strptime(rijidate+" 00:00:00",'%Y-%m-%d %H:%M:%S')
        enddate=datetime.datetime.strptime(rijidate+" 23:59:59",'%Y-%m-%d %H:%M:%S')
        print startdate,enddate

        tasklist = PrecastBeam.objects.filter(curstatustime__range=(startdate,enddate)).values_list('task_id',flat=True).distinct()
        if len(tasklist)>index-1:
            curtask = tasklist[index-1]
            return ProjectTask.objects.get(id=curtask).name
        else:
            return ""


    except:
        traceback.print_exc()
        return ""

@login_required(login_url="/login/")
@csrf_exempt
def biaodan_muban(request):
    try:
        if request.method == 'POST':
            table_data = json.loads(request.body)
            creater = request.user
            mid = table_data.get('id', None)
            name = table_data.get('name', None)
            content = table_data.get('content',None)
            major = table_data.get('major',None)
            formtype= table_data.get('formtype',None)
            select_shujuyuan= eval(table_data.get('select_shujuyuan','[]'))
            if(mid==-1):#新建
                if name and content:
                    nbd = BiaoDanMuBan.objects.create(name =name,content=content,creater=creater)
                    if select_shujuyuan:
                        [Formtempandformtag.objects.create(formtemplet_id=nbd.id,formtag_id=int(sjy)) for sjy in set(select_shujuyuan)]
                    if major:
                        nbd.major_id=int(major)
                    if formtype:
                        nbd.formtype_id=int(formtype)
                    nbd.save()
                    print "add succ"
            else:#修改
                bda = BiaoDanMuBan.objects.get(id=int(mid))
                oldformtempandformtag = [each.formtag_id for each in Formtempandformtag.objects.filter(formtemplet_id=bda.id)]
                if select_shujuyuan:
                    [Formtempandformtag.objects.create(formtemplet_id=bda.id,formtag_id=int(sjy)) for sjy in set(select_shujuyuan) if int(sjy) not in oldformtempandformtag]
                if name:
                    bda.name = name
                if content:
                    bda.content = content
                if major:
                    bda.major_id=int(major)
                if formtype:
                    bda.formtype_id=int(formtype)
                bda.save()
                print "edit succ"
            return HttpResponse("{'res':'succ'}")
        elif request.method == 'DELETE':
            table_data = json.loads(request.body)
            delID = table_data.get('id', None)
            rdata={}
            if BiaoDan.objects.filter(formtemplet_id=int(delID)).count()>0:
                rdata['res']='error'
            else:
                if delID:
                    bda = BiaoDanMuBan.objects.get(id=int(delID))
                    bda.delete()
                rdata['res']='succ'
            return HttpResponse(json.dumps(rdata), content_type="application/json")  
        elif request.method == 'GET':
            # table_data = json.loads(request.GET.get('id'))
            cID = request.GET.get('id')
            cf =  request.GET.get('from',"")
            user = request.user
            # from urllib import urlencode
            glys = request.GET.get('glys','')
            kj= request.GET.get('kj','')
            rijidate = request.GET.get('rijidate',None)
            # tihua = ''
            # for each in glys:
            #     print each['typetable']
            #     print each
            #     if each['typetable']==u'构件':
            #         tihua = PrecastBeam.objects.get(id=int(each['relatedid'])).sign
            #         print 'tihua',tihua

            bda = BiaoDanMuBan.objects.get(id=int(cID))
            # .replace('{{goujianbiaoshi}}','构件1')
            content = bda.content
            if cf=='createissue':
                for each in Formtempandformtag.objects.filter(formtemplet_id=bda.id):
                    try:
                        # print "--------------------------------"
                        # print "{{"+each.formtag.tagname+"}}"
                        # print each.formtag.tag
                        # print eval(each.formtag.tag)
                        content = content.replace("{{"+each.formtag.tagname+"}}",eval(each.formtag.tag))
                    except:
                        traceback.print_exc()
            rdata = {"name":bda.name,"content":content,"formtype":bda.formtype.id,"major":bda.major.id}
            return HttpResponse(json.dumps(rdata))
        # return "{'res':'succ'}"
        # return render_to_response('TaskAndFlow/filemanager/filemanager.html', RequestContext(request,locals()))
    except:
        traceback.print_exc()
        return HttpResponse("{'res':'error'}",content_type="application/json")



@login_required(login_url="/login/")
def biaodan_getrelatestep(request):
    rdata= {}
    rdata['relatestep'] = []
    rdata['issucc'] = "false"
    try:
        mbId = request.GET.get('mbId',None)
        if mbId:
            tmpllist = FlowTemplateStep.objects.filter(relatedformtemplate_id=int(mbId)).values_list('template_id', flat=True)
            print tmpllist
            steplist = FlowTemplateStep.objects.filter(template_id__in=tmpllist)
            for each in steplist:
                tmp = {}
                tmp["id"]=each.id
                tmp["name"] =each.name
                rdata['relatestep'].append(tmp)

            rdata['issucc'] = "true"
    except:
        traceback.print_exc()
        rdata['error']="获取数据出错"

    return HttpResponse(json.dumps(rdata))

@login_required(login_url="/login/")
def biaodan_manerger(request):
    if request.method=='GET':
        qname=request.GET.get('qname','')
        qformmajor= int(request.GET.get('qformmajor','0'))
        qformtype=int(request.GET.get('qformtype','0'))
        page = int(request.GET.get('page', '1'))

        biaodanList = BiaoDanMuBan.objects.all()
        if qname:
            biaodanList = biaodanList.filter(name__contains=qname)
        if qformmajor:
            biaodanList = biaodanList.filter(major_id=qformmajor)
        if qformtype:
            biaodanList = biaodanList.filter(formtype_id=qformtype)
        majorList = UserMajor.objects.all()
        formtypeList = BiaoDanType.objects.all()
        shujuyuan = Formtag.objects.all()

        paginator = Paginator(biaodanList,10)
        try:
            biaodanList = paginator.page(page)
        except:
            traceback.print_exc()
            biaodanList = paginator.page(paginator.num_pages)
    # biaodanList = None
    return render_to_response('TaskAndFlow/flowtemplate/biaodanmanerger.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
def biaodan_edit(request):
    majorList = UserMajor.objects.all()
    formtypeList = BiaoDanType.objects.all()
    return render_to_response('TaskAndFlow/flowtemplate/biaodanedit.html', RequestContext(request,locals()))
