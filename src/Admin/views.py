# -*- coding: utf-8 -*-

import traceback
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt


from UserAndPrj.models import *
from TaskAndFlow.models import *
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
import json,datetime,random
from dss.Serializer import serializer as objtojson
from Scc4PM.settings import UPLOAD_DIR,CURRENT_PROJECT_ID
from PIL import Image

@login_required(login_url="/login/")
def Navigation_editor(request):
    return render_to_response('xadmin/Navigation_editor.html', RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/")
def navigation_editor_mobile(request):
    if request.method=='GET':
        return render_to_response('xadmin/navigation_mobile.html', RequestContext(request,locals()))
    elif request.method=='POST':
        response_data = {}
        response_data["issuc"] = 'false'
        try:
            id=request.POST.get('id', None)
            name=request.POST.get('name', None)
            icon=request.POST.get('icon',None)
            param=request.POST.get('param',None)
            isrecord=request.POST.get('isrecord',None)
            color=request.POST.get('color',None)
            menu = ProjectmenuMobile.objects.get(id=id)
            menu.name = name
            menu.icon = icon
            menu.param = param
            menu.isrecord = isrecord
            menu.color = color
            menu.save()

            response_data["issuc"] = 'true'
        except:
            traceback.print_exc()
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
@login_required(login_url="/login/")
def function_editor(request):
    if request.method=='GET':
        return render_to_response('xadmin/function_editor.html', RequestContext(request,locals()))
    elif request.method=='POST':
        response_data = {}
        response_data["issuc"] = 'false'
        try:
            id=request.POST.get('id', None)
            name=request.POST.get('name', None)
            icon=request.POST.get('icon',None)
            param=request.POST.get('param',None)
            isrecord=request.POST.get('isrecord',None)
            color=request.POST.get('color',None)
            type = id.split('_')[0]
            id = id.split('_')[1]
            if type=="category":
                menu = AdminFunctionCategory.objects.get(id=id)
                menu.name = name
                menu.icon = icon
                menu.param = param
                menu.isrecord = isrecord
                menu.color = color
                menu.save()
            elif type=="function":
                menu = AdminFunction.objects.get(id=id)
                menu.name = name
                menu.icon = icon
                menu.param = param
                menu.isrecord = isrecord
                menu.save()

            response_data["issuc"] = 'true'
        except:
            traceback.print_exc()
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def pbstatus(request):
    response_data = {}
    response_data["issuc"]="true"
    try:
        if request.method=='GET':
            pbtype = request.GET.get('pbtype',0)
            pbstatus = PBStatus.objects.filter(pbtype_id=int(pbtype)).order_by('sequence')
            response_data["data"]=objtojson(pbstatus)
        elif request.method=='POST':
            opt = request.POST.get('opt','')
            if opt=='add':
                statusname = request.POST.get('statusname','')
                isqualify = True if request.POST.get('isqualify','')=='true' else False
                iswancheng = True if request.POST.get('iswancheng','')=='true' else False
                flowtemplate = request.POST.get('flowtemplate',None)
                formtemplate = request.POST.get('formtemplate',None)
                pbtype = request.POST.get('pbtype',None)
                factoryarea = request.POST.get('factoryarea',None)
                color =request.POST.get('color',None)
                cucolor =request.POST.get('cucolor',None)
                try:
                    sequence = PBStatus.objects.filter(pbtype_id=pbtype).order_by('-sequence')[0].sequence+1
                except:
                    sequence=0
                    traceback.print_exc()
                buhegenext=None
                if isqualify:
                    buhegenext = request.POST.get('buhegenext',None)
                    sequence=0
                npbs = PBStatus.objects.create(statusname=statusname,
                                    factoryarea_id=factoryarea,
                                    isqualify=isqualify,pbtype_id=pbtype,
                                    detailcounttype_id = color,
                                    roughcounttype_id = cucolor,
                                    sequence=sequence,nextstatus_id=buhegenext,
                                    relatedflowtemplate_id = flowtemplate,
                                    relatedformtemplate_id = formtemplate,
                                    iscritical=iswancheng)
                userlist = eval(request.POST.get('userlist','[]'))
                for each in userlist:
                    User2PBStatus.objects.create(user_id=int(each),status_id=npbs.id)
                response_data["status"]=objtojson(npbs)
            elif opt=='change':
                idp = request.POST.get('id','0')
                statusname = request.POST.get('statusname','')
                isqualify = True if request.POST.get('isqualify','')=='true' else False
                iswancheng = True if request.POST.get('iswancheng','')=='true' else False
                flowtemplateb = request.POST.get('flowtemplate','0')
                try:
                    flowtemplate = int(flowtemplateb) if flowtemplateb!='0' else None
                except:
                    flowtemplate = None
                formtemplateb = request.POST.get('formtemplate','0')
                try:
                    formtemplate = int(formtemplateb) if formtemplateb!='0' else None
                except:
                    formtemplate=None
                pbtypeb = request.POST.get('pbtype','0')
                pbtype = int(pbtypeb) if pbtypeb!='0' else None
                factoryarea = request.POST.get('factoryarea',None)
                color =request.POST.get('color',None)
                cucolor =request.POST.get('cucolor',None)
                if isqualify:
                    buhegenextb = request.POST.get('buhegenext','0')
                    buhegenext = int(buhegenextb) if buhegenextb!='0' else None
                    sequence=0
                    PBStatus.objects.filter(id=int(idp)).update(statusname=statusname,
                                    factoryarea_id=factoryarea,
                                    isqualify=isqualify,pbtype_id=pbtype,sequence=0,
                                    detailcounttype_id = color,
                                    roughcounttype_id = cucolor,
                                    nextstatus_id=buhegenext,
                                    relatedflowtemplate_id = flowtemplate,
                                    relatedformtemplate_id = formtemplate,
                                    iscritical=iswancheng)
                else:
                    PBStatus.objects.filter(id=int(idp)).update(statusname=statusname,
                                    factoryarea_id=factoryarea,
                                    isqualify=isqualify,pbtype_id=pbtype,
                                    detailcounttype_id = color,
                                    roughcounttype_id = cucolor,
                                    relatedflowtemplate_id = flowtemplate,
                                    relatedformtemplate_id = formtemplate,
                                    iscritical=iswancheng)
                User2PBStatus.objects.filter(status_id=int(idp)).delete()
                userlist = eval(request.POST.get('userlist','[]'))
                for each in userlist:
                    User2PBStatus.objects.create(user_id=int(each),status_id=int(idp))
            elif opt=='getone':
                idp = request.POST.get('id','0')
                response_data['data']=objtojson(PBStatus.objects.get(id=int(idp)))
                users = {'users':[each.user_id for each in User2PBStatus.objects.filter(status_id=int(idp))]}
                response_data['data'].update(users)

            elif opt=='del':
                idp = request.POST.get('id','')
                if idp:
                    try:
                        PBStatus.objects.filter(nextstatus_id=int(idp)).update(nextstatus=None)
                    except:
                        traceback.print_exc()
                    PBStatus.objects.get(id=int(idp)).delete()
                    User2PBStatus.objects.filter(status_id=int(idp)).delete()
            elif opt=='sort':
                lisort = eval(request.POST.get('lisort','[]'))
                print lisort
                l = len(lisort)
                for each in xrange(l):
                    pbs = PBStatus.objects.get(id=int(lisort[each]))
                    if pbs.isqualify:
                        pbs.sequence=l-1
                        pbs.save()
                        continue
                    pbs.sequence=each
                    if each+1==l:
                        pbs.nextstatus_id=None
                    else:
                        pbs.nextstatus_id=int(lisort[each+1])
                    pbs.save()

    except Exception, e: 
        traceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def stylecolor(request):
    response_data = {}
    response_data["issuc"]="true"
    try:
        if request.method=='GET':

            pbcolors = StatusCountType.objects.all()
            response_data["data"]=[each.rendercolor for each in pbcolors]
        elif request.method=='POST':
            opt = request.POST.get('opt','')
            if opt=='del':
                idp = request.POST.get('id','')
                if idp:
                    StatusCountType.objects.get(id=int(idp)).delete()
            elif opt=='get':
                idp = request.POST.get('id','')
                color = StatusCountType.objects.get(id=int(idp))
                response_data["color"] = objtojson(color)
            elif opt=='edit':
                idp = request.POST.get('id','')
                colorname = request.POST.get('colorname',None)
                rendercolor = request.POST.get('rendercolor',None)
                StatusCountType.objects.filter(id=int(idp)).update(name=colorname,rendercolor=rendercolor)
            elif opt=='add':
                colorname = request.POST.get('colorname',None)
                rendercolor = request.POST.get('rendercolor',None)
                sequence = 0
                try:
                    sequence = StatusCountType.objects.all().order_by('-sequence')[0].sequence+1
                except:
                    pass
                color = StatusCountType.objects.create(name=colorname,rendercolor=rendercolor,sequence=sequence)
                response_data["color"] = objtojson(color)
            elif opt=='sort':
                    lisort = eval(request.POST.get('lisort','[]'))
                    for i,val in enumerate(lisort):
                        color = StatusCountType.objects.get(id=int(val))
                        color.sequence=i
                        color.save()

    except:
        response_data["issuc"]="false"
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def menutree(request):
    response_data = {}
    try:
        id=request.GET.get('id', '')
        print id
        prj = Project.objects.get(id=CURRENT_PROJECT_ID)
        if id=='#':
            response_data["id"]="menutree"
            response_data["text"]=prj.name
            response_data["state"]= {'opened':True }

            child_list=[]
            menulist = Projectmenu.objects.filter(parent_id__isnull=True).order_by('seq')
            for menu in menulist:
                child_data = {}
                child_data["id"]="rootmenu_"+str(menu.id)
                child_data["text"]=menu.name
                #child_data["children"]=True
                child_data["icon"]=False

                tmpObj  = {}
                tmpObj["id"] = menu.id
                tmpObj["name"] = menu.name
                tmpObj["icon"] = menu.icon
                tmpObj["parent_id"] = menu.parent.name if menu.parent else '-'
                tmpObj["url"] = menu.url
                tmpObj["param"] = menu.param
                tmpObj["isrecord"] = menu.isrecord
                tmpObj["color"] = menu.color
                tmpObj["seq"] = menu.seq
                child_data["data"]=tmpObj

                subchild_list=[]
                submenulist = Projectmenu.objects.filter(parent_id=menu.id).order_by('seq')
                for submenu in submenulist:
                    subchild_data = {}
                    subchild_data["id"]="submenu_"+str(submenu.id)
                    subchild_data["text"]=submenu.name
                    subchild_data["icon"]=submenu.icon

                    tmpObj  = {}
                    tmpObj["id"] = submenu.id
                    tmpObj["name"] = submenu.name
                    tmpObj["icon"] = submenu.icon
                    tmpObj["parent_id"] = submenu.parent.name if submenu.parent else '-'
                    tmpObj["url"] = submenu.url
                    tmpObj["param"] = submenu.param
                    tmpObj["isrecord"] = submenu.isrecord
                    tmpObj["color"] = submenu.color
                    tmpObj["seq"] = submenu.seq
                    subchild_data["data"]=tmpObj

                    subchild_list.append(subchild_data)

                child_data["children"] = subchild_list
                child_list.append(child_data)

            response_data["children"]=child_list


        #print json.dumps(response_data)

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        traceback.print_exc()


@login_required(login_url="/login/")
def menutreemobile(request):
    response_data = {}
    try:
        id=request.GET.get('id', '')
        print id
        prj = Project.objects.get(id=CURRENT_PROJECT_ID)
        if id=='#':
            response_data["id"]="menutree"
            response_data["text"]=prj.name
            response_data["state"]= {'opened':True }

            child_list=[]
            menulist = ProjectmenuMobile.objects.filter(parent_id__isnull=True).order_by('seq')
            for menu in menulist:
                child_data = {}
                child_data["id"]="rootmenu_"+str(menu.id)
                child_data["text"]=menu.name
                #child_data["children"]=True
                child_data["icon"]=False

                tmpObj  = {}
                tmpObj["id"] = menu.id
                tmpObj["name"] = menu.name
                tmpObj["icon"] = menu.icon
                tmpObj["parent_id"] = menu.parent.name if menu.parent else '-'
                tmpObj["url"] = menu.url
                tmpObj["param"] = menu.param
                tmpObj["isrecord"] = menu.isrecord
                tmpObj["color"] = menu.color
                child_data["data"]=tmpObj

                subchild_list=[]
                submenulist = ProjectmenuMobile.objects.filter(parent_id=menu.id).order_by('seq')
                for submenu in submenulist:
                    subchild_data = {}
                    subchild_data["id"]="submenu_"+str(submenu.id)
                    subchild_data["text"]=submenu.name
                    subchild_data["icon"]=submenu.icon

                    tmpObj  = {}
                    tmpObj["id"] = submenu.id
                    tmpObj["name"] = submenu.name
                    tmpObj["icon"] = submenu.icon
                    tmpObj["parent_id"] = submenu.parent.name if submenu.parent else '-'
                    tmpObj["url"] = submenu.url
                    tmpObj["param"] = submenu.param
                    tmpObj["isrecord"] = submenu.isrecord
                    tmpObj["color"] = submenu.color
                    subchild_data["data"]=tmpObj

                    subchild_list.append(subchild_data)

                child_data["children"] = subchild_list
                child_list.append(child_data)

            response_data["children"]=child_list


        #print json.dumps(response_data)


    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def functiontree(request):
    response_data = {}
    try:
        id=request.GET.get('id', '')
        print id
        prj = Project.objects.get(id=CURRENT_PROJECT_ID)
        if id=='#':
            response_data["id"]="menutree"
            response_data["text"]=prj.name
            response_data["state"]= {'opened':True }

            child_list=[]
            menulist = AdminFunctionCategory.objects.all()
            for menu in menulist:
                child_data = {}
                child_data["id"]="category_"+str(menu.id)
                child_data["text"]=menu.name
                #child_data["children"]=True
                child_data["icon"]=False

                tmpObj  = {}
                tmpObj["id"] = menu.id
                tmpObj["name"] = menu.name
                tmpObj["icon"] = menu.icon
                tmpObj["isrecord"] = menu.isrecord
                tmpObj["color"] = menu.color
                child_data["data"]=tmpObj

                subchild_list=[]
                submenulist = AdminFunction.objects.filter(category_id=menu.id)
                for submenu in submenulist:
                    subchild_data = {}
                    subchild_data["id"]="function_"+str(submenu.id)
                    subchild_data["text"]=submenu.name
                    subchild_data["icon"]=submenu.icon

                    tmpObj  = {}
                    tmpObj["id"] = submenu.id
                    tmpObj["name"] = submenu.name
                    tmpObj["icon"] = submenu.icon
                    tmpObj["parent_id"] = submenu.category.name if submenu.category else '-'
                    tmpObj["url"] = submenu.url
                    tmpObj["param"] = submenu.param
                    tmpObj["isrecord"] = submenu.isrecord
                    tmpObj["color"] = menu.color
                    subchild_data["data"]=tmpObj

                    subchild_list.append(subchild_data)

                child_data["children"] = subchild_list
                child_list.append(child_data)

            response_data["children"]=child_list


        #print json.dumps(response_data)


    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def prjmenujson(request):
    response_data = {}
    response_data["issuc"] = 'false'
    try:
        menulist = Projectmenu.objects.filter(parent_id__isnull=True,isrecord=1).order_by('seq')
        if not request.user.is_admin:
            menulist=menulist.exclude(name="系统配置")
        response_data["menulist"] = []
        for menu in menulist:
            menuobj=objtojson(menu)
            childlist = Projectmenu.objects.filter(parent_id=int(menu.id),isrecord=1).order_by('seq')
            menuobj["submenu"] = []
            for submenu in childlist:
                menuobj["submenu"].append(objtojson(submenu))

            response_data["menulist"].append(menuobj)
        response_data["issuc"] = 'true'
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def prjmenujson_mobile(request):
    response_data = {}
    response_data["issuc"] = 'false'
    try:
        menulist = ProjectmenuMobile.objects.filter(parent_id__isnull=True,isrecord=1)
        response_data["menulist"] = []
        for menu in menulist:
            menuobj=objtojson(menu)
            childlist = ProjectmenuMobile.objects.filter(parent_id=int(menu.id),isrecord=1).order_by('-seq')
            menuobj["submenu"] = []
            for submenu in childlist:
                menuobj["submenu"].append(objtojson(submenu))

            response_data["menulist"].append(menuobj)
        response_data["issuc"] = 'true'
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def baseinfo(request):
    response_data = {}
    response_data["issuc"] = 'false'
    try:
        logo = "/images/title.png"
        docs = Document.objects.filter(doctype='logo').order_by("-createtime")
        if docs:
            logo = "/"+str(docs[0].filepath)+docs[0].name
        response_data["logo"]=logo

        project_title = '智慧建筑管理平台'
        if CustomInfo.objects.filter(infotype='project_title'):
            project_title =CustomInfo.objects.filter(infotype='project_title')[0].custominfo

        response_data["project_title"]=project_title

        development_units = ['上海建工四建集团有限公司','上海筑众信息科技有限公司']
        if CustomInfo.objects.filter(infotype='development_unit'):
            development_units =eval(CustomInfo.objects.filter(infotype='development_unit')[0].custominfo)

        response_data["development_units"]=' '.join(development_units)

        response_data["project_name"] = Project.objects.get(id=CURRENT_PROJECT_ID).name

        response_data["issuc"] = 'true'

    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def savemenu(request):
    response_data = {}
    response_data["issuc"] = 'false'
    try:
        id=request.POST.get('id', None)
        name=request.POST.get('name', None)
        icon=request.POST.get('icon',None)
        param=request.POST.get('param',None)
        isrecord=request.POST.get('isrecord',None)
        color=request.POST.get('color',None)
        seq=request.POST.get('seq','0')
        menu = Projectmenu.objects.get(id=id)
        menu.name = name
        menu.icon = icon
        menu.param = param
        menu.isrecord = isrecord
        menu.color = color
        menu.seq=seq
        menu.save()

        response_data["issuc"] = 'true'
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def adminconfigure(request):
    templateName = 'xadmin/AdminConfigure.html'
    return render_to_response(templateName, RequestContext(request, locals()))

def admincommonindex(request):
    templateName = 'xadmin/common-index.html'
    return render_to_response(templateName, RequestContext(request, locals()))

def adminmanagerpicture(request):
    templateName = 'xadmin/manager-picture.html'
    docs = Document.objects.filter(doctype='lunbo').order_by("-createtime")
    if docs:
        imgdoc = docs[0]
    return render_to_response(templateName, RequestContext(request, locals()))

def adminmanagerbackpic(request):
    templateName = 'xadmin/manager-backpic.html'
    docs = Document.objects.filter(doctype='back').order_by("-createtime")
    if docs:
        imgdoc = docs[0]
    return render_to_response(templateName, RequestContext(request, locals()))

def adminmanagerlogopic(request):
    templateName = 'xadmin/manager-logopic.html'
    docs = Document.objects.filter(doctype='logo').order_by("-createtime")
    if docs:
        imgdoc = docs[0]
    return render_to_response(templateName, RequestContext(request, locals()))

def delimg(request):
    response_data = {}
    response_data['issuc'] = 'true'
    docid = request.GET.get('docid')
    doc = Document.objects.get(id=docid)
    doc.delete()
    return HttpResponse(json.dumps(response_data,encoding="UTF-8",ensure_ascii=False), content_type="application/json")

def cropimg(request):
    response_data = {}
    response_data['issuc'] = 'true'
    IMAGE_BAKUP = u"upload/"
    _CONTENT_TYPES = { 'image/png': '.png', 'image/gif': '.gif', 'image/jpeg': '.jpg', 'image/jpeg': '.jpeg' }
    IMAGE_BAKUP = ''
    IMAGE_PATH = UPLOAD_DIR+'/'+request.GET.get("IMAGE_PATH")#UPLOAD_DIR+'/picture.jpg'
    IMAGE_X1 = int(request.GET.get("IMAGE_X1"))
    IMAGE_Y1 = int(request.GET.get("IMAGE_Y1"))
    IMAGE_X2 = int(request.GET.get("IMAGE_X2"))
    IMAGE_Y2 = int(request.GET.get("IMAGE_Y2"))

    docid = request.GET.get('docid')
    doctype = request.GET.get('doctype','normal')
    predoc = Document.objects.get(id=docid)

    im = Image.open(IMAGE_PATH) #打开图片句柄
    box = (IMAGE_X1,IMAGE_Y1,IMAGE_X2,IMAGE_Y2) #设定裁剪区域
    region = im.crop(box)  #裁剪图片，并获取句柄region
    path=UPLOAD_DIR
    fn = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fn = fn + '_%d' % random.randint(0,100)+'.jpg'
    path = path+fn
    region.save(path) #保存图片

    doc = Document()
    doc.name = fn
    doc.shortname = fn
    doc.filepath = u"upload/"
    doc.creator=request.user
    doc.doctype=doctype
    doc.save()
    predoc.delete()
    response_data["docpath"] = '/'+u"upload/"+fn
    response_data["docid"] = doc.id
    return HttpResponse(json.dumps(response_data,encoding="UTF-8",ensure_ascii=False), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def directorynotify(request):
    if request.method=='GET':
        return render_to_response('xadmin/directorynotify.html', RequestContext(request,locals()))
    elif request.method=='POST':
        response_data={}
        response_data["issuc"]='false'
        try:
            opt = request.POST.get('opt','')
            if(opt=="get"):
                dirId = int(request.POST.get('dirId'))
                response_data["userlist"] =[{"userId":each.notifyuser_id,"userName":each.notifyuser.truename}
                                             for each in  DirectoryNotifyuser.objects.filter(directory_id=dirId)]
            elif(opt=="set"):
                dirId = int(request.POST.get('dirId'))
                ntfuserlist = eval(request.POST.get('ntfuserlist','[]'))

                DirectoryNotifyuser.objects.filter(directory_id=dirId).delete()
                user_list_to_insert = list()
                for user in ntfuserlist:
                    user_list_to_insert.append(DirectoryNotifyuser(directory_id=dirId, notifyuser_id=user))
                DirectoryNotifyuser.objects.bulk_create(user_list_to_insert)

            response_data["issuc"]='true'
        except:
            traceback.print_exc()
            response_data["error"] = "操作失败！"
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def directoryauth(request):
    if request.method=='GET':
        return render_to_response('xadmin/directoryauth.html', RequestContext(request,locals()))
    elif request.method=='POST':
        response_data={}
        response_data["issuc"]='false'
        try:
            opt = request.POST.get('opt','')
            if(opt=="get"):
                dirId = int(request.POST.get('dirId'))
                response_data["authuserlist"] =[{"userId":each.user_id,"userName":each.user.truename,"auth":each.auth}
                                             for each in  DirectoryUser.objects.filter(directory_id=dirId)]
            elif(opt=="set"):
                dirId = int(request.POST.get('dirId'))
                authuserlist = eval(request.POST.get('authuserlist','[]'))
                print authuserlist

                DirectoryUser.objects.filter(directory_id=dirId).delete()
                user_list_to_insert = list()
                for each in authuserlist:
                    user_list_to_insert.append(DirectoryUser(directory_id=dirId, user_id=each["user"],auth=each["auth"]))
                DirectoryUser.objects.bulk_create(user_list_to_insert)

            response_data["issuc"]='true'
        except:
            traceback.print_exc()
            response_data["error"] = "操作失败！"
        return HttpResponse(json.dumps(response_data), content_type="application/json")




@login_required(login_url="/login/")
def noticiConfig(request):
    if request.method=='GET':
        return render_to_response('xadmin/noticeConfig.html', RequestContext(request,locals()))
    else:
        pass


