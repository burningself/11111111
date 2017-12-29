# -*- coding: utf-8 -*-
'''

@author: pgb
'''
import traceback
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import loader, Context, RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from TaskAndFlow.utility import *
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
import datetime
from Business.models import *
from TaskAndFlow.utility_filemanager import *
from UserPrjConfig.permissions import *

# Create your views here.


def create_flowtype(request):
    form = FlowTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = FlowTypeForm()

    t = get_template('TaskAndFlow/flowtemplate/create_flowtype.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def list_flowtype(request):

    list_items = FlowType.objects.all()
    paginator = Paginator(list_items, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/flowtemplate/list_flowtype.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def view_flowtype(request, id):
    flowtype_instance = FlowType.objects.get(id=id)

    t = get_template('TaskAndFlow/flowtemplate/view_flowtype.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def edit_flowtype(request, id):

    flowtype_instance = FlowType.objects.get(id=id)

    form = FlowTypeForm(request.POST or None, instance=flowtype_instance)

    if form.is_valid():
        form.save()

    t = get_template('TaskAndFlow/flowtemplate/edit_flowtype.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


@csrf_exempt
@login_required(login_url="/login/")
def create_flowtemplate(request):
    response_data = {}
    templateName = request.POST.get('templateName', '')
    templateMajor = request.POST.get('templateMajor', '')
    templateType = request.POST.get('templateType', '')
    templateDesc = request.POST.get('templateDesc', '')
    selBrowsers = eval(request.POST.get('selBrowsers', '[]'))

    if not templateName:
        response_data["issuc"] = "false"
        response_data["error"] = u"模板名称不能为空！"

    elif FlowTemplate.objects.filter(name=templateName):
        response_data["issuc"] = "false"
        response_data["error"] = u"模板已经存在！"

    else:
        newRecord = FlowTemplate.objects.create(name=templateName, major_id=templateMajor,
                                                flowtype_id=templateType, describe=templateDesc)
        tmp2user_list_to_insert = list()
        for each in selBrowsers:
            tmp2user_list_to_insert.append(FlowTemplateUser(template=newRecord, user_id=int(each)))
        FlowTemplateUser.objects.bulk_create(tmp2user_list_to_insert)

        response_data["templateId"] = newRecord.id
        response_data["issuc"] = "true"

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def list_flowtemplate(request):
    MajorChoices = UserMajor.objects.all()
    TypeChoices = FlowType.objects.all()

    memberList = getPrjUserlist()

    list_items = FlowTemplate.objects.all()

    typeId = int(request.GET.get('queryType', '0'))
    majorId = int(request.GET.get('queryMajor', '0'))
    tempName = request.GET.get('tempName', '')

    if tempName != "":
        list_items = list_items.filter(name__icontains=tempName)

    if majorId != 0:
        list_items = list_items.filter(major_id=majorId)

    if typeId != 0:
        list_items = list_items.filter(flowtype_id=typeId)

    paginator = Paginator(list_items, 10)
    listcount = list_items.count()
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    if checkMobile(request):
        t = get_template(
            'TaskAndFlow/flowtemplate/list_flowtemplate_mobile.html')
    else:
        t = get_template('TaskAndFlow/flowtemplate/list_flowtemplate.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


@csrf_exempt
@login_required(login_url="/login/")
def view_flowtemplate(request, id):
    flowtemplate_instance = FlowTemplate.objects.get(id=id)
    if request.method == "POST":
        response_data = {"status": 1}

        response_data["tmpObj"] = {}
        response_data["tmpObj"][
            "tmpType"] = flowtemplate_instance.flowtype.name
        response_data["tmpObj"]["majorType"] = flowtemplate_instance.major.name

        return HttpResponse(json.dumps(response_data), content_type="application/json")
#        return serializers.serialize('json',flowtemplate_instance)

    t = get_template('TaskAndFlow/flowtemplate/view_flowtemplate.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


@csrf_exempt
@login_required(login_url="/login/")
def update_flowtemplate_info(request):
    try:
        response_data = {}
        form = FlowTemplateStepForm(request.POST or None)

        if form.is_valid():
            form.save()

        response_data["status"] = 1
    except:
        traceback.print_exc()
        response_data["status"] = 0
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def update_flowtemplate(request):
    try:
        response_data = {}
        flowtemplateId = int(request.POST.get('flowtemplate', 0))
        queueStr = request.POST.get('queueStr', [])
        queueList = queueStr.split(",")[1:]

        for each in FlowTemplateStep.objects.filter(template_id=flowtemplateId, isstartstep=1):
            each.isstartstep = False
            each.save()

        for each in queueList:
            tmpStep = FlowTemplateStep.objects.get(
                template_id=flowtemplateId, id=each)
            if queueList.index(each) == 0:
                tmpStep.isstartstep = True
            tmpStep.sequence = queueList.index(each)
            tmpStep.save()

        response_data["status"] = 1
    except:
        traceback.print_exc()
        response_data["status"] = 0
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def edit_flowtemplate(request, id):
    if request.method=="GET":
        flowtemplate_instance = FlowTemplate.objects.get(id=id)

        flowTemplateStepform = FlowTemplateStepForm()

        TemplateSteplist = FlowTemplateStep.objects.filter(
            template=flowtemplate_instance).order_by("sequence").values()

        for eachStep in TemplateSteplist:
            eachStep["actors"] = []
            eachStep["observer"] = []
            eachStep["rules"] = []

            for each in FlowStepUser.objects.filter(flowstep_id=eachStep["id"], isactor=1):
                eachStep["actors"].append(
                    each.user.name + "_" + each.user.truename)

            for each in FlowStepUser.objects.filter(flowstep_id=eachStep["id"], isactor=0):
                eachStep["observer"].append(
                    each.user.name + "_" + each.user.truename)

            for each in FlowStepOperation.objects.filter(flowstep_id=eachStep["id"]):
                tmpObj = {}
                tmpObj["actortype"] = each.actortype.name
                tmpObj["stepname"] = each.name
                tmpObj["nextstep"] = each.nextflowstep.name
                eachStep["rules"].append(tmpObj)

        memberList = getPrjUserlist()
        actorMode = ActorType.objects.all()
        MajorChoices = UserMajor.objects.all()
        TypeChoices = FlowType.objects.all()
        browserlist =[each.user for each in FlowTemplateUser.objects.filter(template=flowtemplate_instance)]

        for each in memberList:
            if each in browserlist:
                each.selected = True
            else:
                each.selected = False

        t = get_template('TaskAndFlow/flowtemplate/edit_flowtemplate.html')
        c = RequestContext(request, locals())
        return HttpResponse(t.render(c))
    else:
        response_data = {}
        try:
            templateName = request.POST.get('templateName', '')
            templateMajor = request.POST.get('templateMajor', '')
            templateType = request.POST.get('templateType', '')
            templateDesc = request.POST.get('templateDesc', '')
            selBrowsers = eval(request.POST.get('selBrowsers', '[]'))

            if not templateName:
                response_data["issuc"] = "false"
                response_data["error"] = u"模板名称不能为空！"

            elif FlowTemplate.objects.filter(name=templateName).exclude(id=id):
                response_data["issuc"] = "false"
                response_data["error"] = u"模板名称重复！"

            else:
                FlowTemplate.objects.filter(id=id).update(name=templateName, major_id=templateMajor,
                                    flowtype_id=templateType, describe=templateDesc)

                FlowTemplateUser.objects.filter(template_id=id).delete()

                tmp2user_list_to_insert = list()
                for each in selBrowsers:
                    tmp2user_list_to_insert.append(FlowTemplateUser(template_id=id, user_id=int(each)))
                FlowTemplateUser.objects.bulk_create(tmp2user_list_to_insert)

                response_data["issuc"] = "true"
        except:
            traceback.print_exc()
            response_data["issuc"] = false
            response_data["error"] = "提交失败！"
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def delete_flowtemplate(request):
    try:
        flag = 1
        response_data = {"status": 1}
        tmpid = int(request.POST.get('tmpid', 0))

        if projectevent.objects.filter(template_id=tmpid):
            response_data["status"] = 0
            response_data["error"] = "已有关联项目，不允许删除！"
        else:
            for each in FlowTemplateStep.objects.filter(template_id=tmpid):
                FlowStepOperation.objects.filter(flowstep=each).delete()
                FlowStepUser.objects.filter(flowstep=each).delete()
                each.delete()
            FlowTemplate.objects.filter(id=tmpid).delete()

    except:
        traceback.print_exc()
        response_data["status"] = 0
        response_data["error"] = "提交失败！"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def create_flowtemplatestep(request):
    try:
        response_data = {"status": 1}
        form = FlowTemplateStepForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            template = form.cleaned_data['template']
            isstartstep = form.cleaned_data['isstartstep']
            isendstep = form.cleaned_data['isendstep']
            isautotransfer = form.cleaned_data['isautotransfer']
            maxDuration = form.cleaned_data['maxDuration']
            sequence = form.cleaned_data['sequence']

            if FlowTemplateStep.objects.filter(template_id=template,name=name).count() == 0:
                if isstartstep or FlowTemplateStep.objects.filter(template_id=template).count() == 0:
                    for each in FlowTemplateStep.objects.filter(template_id=template):
                        each.sequence = each.sequence + 1
                        each.isstartstep = 0
                        each.save()

                    form.instance.isstartstep = 1
                    form.instance.sequence = 0
                    form.save()

                elif isendstep or sequence >= FlowTemplateStep.objects.filter(template_id=template).latest('sequence').sequence or sequence <= 0:
                    FlowTemplateStep.objects.filter(
                        template_id=template).update(isendstep=0)
                    form.instance.isendstep = 1
                    form.instance.sequence = FlowTemplateStep.objects.filter(
                        template_id=template).latest('sequence').sequence + 1
                    form.save()

                elif sequence > 0 and sequence < FlowTemplateStep.objects.filter(template_id=template).latest('sequence').sequence:
                    for each in FlowTemplateStep.objects.filter(sequence__gte=sequence, template_id=template):
                        each.sequence = each.sequence + 1
                        each.save()

                    form.save()
                else:
                    response_data["status"] = 0
                    response_data["msg"] = "序号信息有误！"
            else:
                response_data["status"] = 0
                response_data["msg"] = "步骤名称重复！"

        else:
            response_data["status"] = 0
            response_data["msg"] = "提交信息不全！"

    except Exception, e:
        response_data['msg'] = '%s' % e
        response_data["status"] = 0

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def changename_flowtemplatestep(request):
    try:
        response_data = {}
        NewTemplateStepName = request.GET.get('NewTemplateStepName', '')
        curTemplateStepId = int(request.GET.get('curTemplateStepId', 0))
        if not NewTemplateStepName:
            response_data["issuc"] = "false"
            response_data["error"] = u"名称不能为空！"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        each = FlowTemplateStep.objects.get(id=curTemplateStepId)
        each.name = NewTemplateStepName
        each.save()
        response_data["issuc"] = "true"
    except:
        traceback.print_exc()

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def list_flowtemplatestep_form(request):
    # 根据流程查询表单模板
    response_data = {}
    try:
        liuchengid = request.GET.get('liuchengid', 0)

        if liuchengid:
            print 'print liuchengid', liuchengid
            try:
                fts = FlowTemplateStep.objects.get(isstartstep=True, template_id=int(
                liuchengid), relatedformtemplate__isnull=False)
                response_data['formtempid'] = fts.relatedformtemplate.id
                response_data['formtempname'] = fts.relatedformtemplate.name
                response_data['stepid'] = fts.id
            except:
                traceback.print_exc()
                response_data['formtempid'] = None
                response_data['stepid'] =""
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({'res': 'error'}), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def get_flowtemplatestep(request, id):
    try:
        response_data = {"status": 1}
        stpOperList = []
        flowtemplatestep_instance = FlowTemplateStep.objects.get(id=id)

        for each in FlowStepOperation.objects.filter(flowstep=flowtemplatestep_instance).values():
            tmpObj = {}
            tmpObj["name"] = each["name"]
            tmpObj["id"] = each["id"]
            stpOperList.append(tmpObj)
        response_data["stpOperList"] = stpOperList
    except:
        traceback.print_exc()
        response_data["status"] = 0
        response_data["error"] = "获取操作失败！"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def view_flowtemplatestep(request, id):
    flowtemplatestep_instance = FlowTemplateStep.objects.get(id=id)

    t = get_template('TaskAndFlow/flowtemplate/view_flowtemplatestep.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


@csrf_exempt
@login_required(login_url="/login/")
def update_flowtemplatestep(request, id):
    try:
        response_data = {'status': 1}
        flowtemplatestep_instance = FlowTemplateStep.objects.get(id=id)
        form = FlowTemplateUpdateStepForm(
            request.POST or None, instance=flowtemplatestep_instance)
        if request.method == 'POST':
            if form.is_valid():
                name = form.cleaned_data['name']
                template = form.cleaned_data['template']
                if FlowTemplateStep.objects.filter(template_id=template,name=name).exclude(id=id).count() == 0:
                    form.save()
                else:
                    response_data["status"] = 0
                    response_data["msg"] = "步骤名称重复！"
        else:
            response_data['form'] = form.as_table()
    except:
        traceback.print_exc()
        response_data["status"] = 0
        response_data["error"] = "提交失败！"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def edit_flowtemplatestep(request, id):
    response_data = {}
    response_data["status"] = 1
    try:
        flag = 1
        flowtemplatestep_instance = FlowTemplateStep.objects.get(id=int(id))
        actorList = request.POST.get('actorStr', '').split(":")
        observerList = request.POST.get('observerStr', '').split(":")
        ruleList = request.POST.get('ruleStr', '').split(":")
        print ruleList

        if "" in actorList:
            actorList.remove("")

        if "" in observerList:
            observerList.remove("")

        if "" in ruleList:
            ruleList.remove("")

        actoruidList = []
        observeruidList = []
        for each in actorList:
            if each.split("_")[0] != "":
                actoruidList.append(User.objects.get(
                    name=each.split("_")[0]).id)

        for each in observerList:
            if each.split("_")[0] != "":
                observeruidList.append(
                    User.objects.get(name=each.split("_")[0]).id)

        FlowStepUser.objects.filter(isactor=1, flowstep=flowtemplatestep_instance).exclude(
            user_id__in=actoruidList).delete()
        FlowStepUser.objects.filter(isactor=0, flowstep=flowtemplatestep_instance).exclude(
            user_id__in=observeruidList).delete()
#        FlowStepOperation.objects.filter(flowstep=flowtemplatestep_instance).delete()

        for each in actorList:
            if "_" in each:
                if not FlowStepUser.objects.filter(isactor=1, flowstep=flowtemplatestep_instance, user=User.objects.get(name=each.split("_")[0])):
                    FlowStepUser.objects.create(
                        isactor=1, flowstep=flowtemplatestep_instance, user=User.objects.get(name=each.split("_")[0]))

        for each in observerList:
            if "_" in each:
                if not FlowStepUser.objects.filter(isactor=0, flowstep=flowtemplatestep_instance, user=User.objects.get(name=each.split("_")[0])):
                    FlowStepUser.objects.create(
                        isactor=0, flowstep=flowtemplatestep_instance, user=User.objects.get(name=each.split("_")[0]))

        if len(ruleList):
            tgtStpId = []
            for each in ruleList:
                if "_" in each:
                    tgtStpId.append(each.split("_")[2])
                    if FlowStepOperation.objects.filter(flowstep_id=id, nextflowstep_id=int(each.split("_")[2])):
                        FlowStepOperation.objects.filter(flowstep_id=id, nextflowstep_id=int(each.split(
                            "_")[2])).update(actortype_id=int(each.split("_")[0]), name=each.split("_")[1])
                    else:
                        FlowStepOperation.objects.create(actortype_id=int(each.split("_")[0]), name=each.split(
                            "_")[1], flowstep_id=id, nextflowstep_id=int(each.split("_")[2]))

            for each in FlowStepOperation.objects.filter(flowstep_id=id).exclude(nextflowstep_id__in=tgtStpId):
                if not EventStepOperation.objects.filter(flowstepoper=each):
                    each.delete()
                    pass
                else:
                    response_data["status"] = 0
                    response_data["error"] = "操作规则不能删除，已启用！"
        else:
            for each in FlowStepOperation.objects.filter(flowstep_id=id):
                if not EventStepOperation.objects.filter(flowstepoper=each):
                    each.delete()
                else:
                    response_data["status"] = 0
                    response_data["error"] = "操作规则不能删除，已启用！"

    except:
        traceback.print_exc()
        response_data["status"] = 0
        response_data["error"] = "设置失败！"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def delete_flowtemplatestep(request):
    try:
        flag = 1
        response_data = {"status": 1}
        stpid = int(request.POST.get('stpid', 0))

        if Eventstep.objects.filter(flowstep_id=stpid):
            response_data["status"] = 0
            response_data["error"] = "已有关联项目，不允许删除！"
        else:
            FlowStepOperation.objects.filter(flowstep_id=stpid).delete()
            FlowStepUser.objects.filter(flowstep_id=stpid).delete()
            FlowTemplateStep.objects.get(id=stpid).delete()

    except:
        traceback.print_exc()
        response_data["status"] = 0
        response_data["error"] = "提交失败！"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def create_flowstepuser(request):
    form = FlowStepUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = FlowStepUserForm()

    t = get_template('TaskAndFlow/flowtemplate/create_flowstepuser.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def list_flowstepuser(request):

    list_items = FlowStepUser.objects.all()
    paginator = Paginator(list_items, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/flowtemplate/list_flowstepuser.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def view_flowstepuser(request, id):
    flowstepuser_instance = FlowStepUser.objects.get(id=id)

    t = get_template('TaskAndFlow/flowtemplate/view_flowstepuser.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def edit_flowstepuser(request, id):

    flowstepuser_instance = FlowStepUser.objects.get(id=id)

    form = FlowStepUserForm(request.POST or None,
                            instance=flowstepuser_instance)

    if form.is_valid():
        form.save()

    t = get_template('TaskAndFlow/flowtemplate/edit_flowstepuser.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def create_actortype(request):
    form = ActorTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ActorTypeForm()

    t = get_template('TaskAndFlow/flowtemplate/create_actortype.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def list_actortype(request):

    list_items = ActorType.objects.all()
    paginator = Paginator(list_items, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/flowtemplate/list_actortype.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def view_actortype(request, id):
    actortype_instance = ActorType.objects.get(id=id)

    t = get_template('TaskAndFlow/flowtemplate/view_actortype.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def edit_actortype(request, id):

    actortype_instance = ActorType.objects.get(id=id)

    form = ActorTypeForm(request.POST or None, instance=actortype_instance)

    if form.is_valid():
        form.save()

    t = get_template('TaskAndFlow/flowtemplate/edit_actortype.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def create_flowstepoperation(request):
    form = FlowStepOperationForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = FlowStepOperationForm()

    t = get_template('TaskAndFlow/flowtemplate/create_flowstepoperation.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def list_flowstepoperation(request):

    list_items = FlowStepOperation.objects.all()
    paginator = Paginator(list_items, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    t = get_template('TaskAndFlow/flowtemplate/list_flowstepoperation.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def view_flowstepoperation(request, id):
    flowstepoperation_instance = FlowStepOperation.objects.get(id=id)

    t = get_template('TaskAndFlow/flowtemplate/view_flowstepoperation.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def edit_flowstepoperation(request, id):

    flowstepoperation_instance = FlowStepOperation.objects.get(id=id)

    form = FlowStepOperationForm(
        request.POST or None, instance=flowstepoperation_instance)

    if form.is_valid():
        form.save()

    t = get_template('TaskAndFlow/flowtemplate/edit_flowstepoperation.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


@login_required(login_url="/login/")
@check_permission
def qualitycenter(request):
    if CustomInfo.objects.filter(infotype='hide_function'):
            hide_function =eval(CustomInfo.objects.filter(infotype='hide_function')[0].custominfo)
    templateName = 'TaskAndFlow/flowtemplate/zhiliang_general.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def qualitycenter_getpbstatuslist(request):
    list_items = filterPbListRequest(request)

    iswholemodel = request.GET.get('_isWholeModel', '')

    list_items_issue = list_items


    response_data = {}
    response_data["pbstatuslist"]=[]

    issuetype = request.GET.get('issuetype', None)
    issueId = request.GET.get('issueId', None)

    acclist = None
    if issuetype:
        if issuetype=="zhiliangyanshou":
            acclist = Acceptanceinfo.objects.filter(id=int(issueId))
    else:
        acclist = Acceptanceinfo.objects.exclude(status=3)

    if  acclist:
        unitprjIdlist=[]
        elevationIdlist=[]
        zoneIdlist=[]
        PbGrpIdlist=[]
        PbIdlist=[]
        for ele in acclist:
            if ele.relatedspace_type=="单位工程":
                unitprjIdlist.append(ele.relatedspace_id)
            elif ele.relatedspace_type=="楼层":
                elevationIdlist.append(ele.relatedspace_id)
            elif ele.relatedspace_type=="分区":
                zoneIdlist.append(ele.relatedspace_id)
            elif ele.relatedspace_type=="构件组":
                PbGrpIdlist.append(ele.relatedspace_id)
            elif ele.relatedspace_type=="构件":
                PbIdlist.append(ele.relatedspace_id)
            else:
                pass

        if len(PbGrpIdlist)>0:
            pbgrppblist = Pbgrouprelation.objects.filter(pbgroup__in=PbGrpIdlist).values_list('pb_id', flat=True)
            PbIdlist.extend(pbgrppblist)

        # if len(zoneIdlist)>0:
        #     Pbgroups=Pbgroup.objects.filter(zone_id__in=zoneIdlist)
        #     pbgrppblist = Pbgrouprelation.objects.filter(pbgroup__in=Pbgroups).values_list('pb_id', flat=True)
        #     PbIdlist.extend(pbgrppblist)

        list_items=list_items.filter(Q(elevation__unitproject_id__in=unitprjIdlist)|
                                     Q(elevation_id__in=elevationIdlist)|
                                     Q(zone_id__in=zoneIdlist)|
                                     Q(id__in=PbIdlist))

        tmpObj = {}
        tmpObj["type"]=""
        if iswholemodel=="true":
            tmpObj["color"] = "#f6f634"
        else:
            tmpObj["color"] = "#f6f634"
        tmpObj["pblist"] = []
        for eachpb in list_items:
            tmpPb = {}
            tmpPb["lvmdbid"] = eachpb.lvmdbid
            tmpObj["pblist"].append(tmpPb)
        response_data["pbstatuslist"].append(tmpObj)


    getIssuePblist("zhiliang",issueId,response_data,request,list_items_issue,iswholemodel)

    response_data["issuc"]="true"

    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def anquan_getpbstatuslist(request):
    list_items = filterPbListRequest(request)

    iswholemodel = request.GET.get('_isWholeModel', '')

    list_items_issue = list_items


    response_data = {}
    response_data["pbstatuslist"]=[]

    issuetype = request.GET.get('issuetype', None)
    issueId = request.GET.get('issueId', None)

    hazardlist = None
    if issuetype:
        if issuetype=="weixianyuan":
            hazardlist = Hazardevent.objects.filter(id=int(issueId))
    else:
        hazardlist = Hazardevent.objects.filter(his_date=datetime.date.today())

    if  hazardlist:
        unitprjIdlist=[]
        elevationIdlist=[]
        zoneIdlist=[]
        PbIdlist=[]
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

        print zoneIdlist
        # if len(zoneIdlist)>0:
        #     Pbgroups=Pbgroup.objects.filter(zone_id__in=zoneIdlist)
        #     pbgrppblist = Pbgrouprelation.objects.filter(pbgroup__in=Pbgroups).values_list('pb_id', flat=True)
        #     PbIdlist.extend(pbgrppblist)

        list_items=list_items.filter(Q(elevation__unitproject_id__in=unitprjIdlist)|
                                     Q(elevation_id__in=elevationIdlist)|
                                     Q(zone_id__in=zoneIdlist))

        tmpObj = {}
        tmpObj["type"]=""
        if iswholemodel=="true":
            tmpObj["color"] = "#BAF300"
        else:
            tmpObj["color"] = "#BAF300"
        tmpObj["pblist"] = []
        for eachpb in list_items:
            tmpPb = {}
            tmpPb["lvmdbid"] = eachpb.lvmdbid
            tmpObj["pblist"].append(tmpPb)
        response_data["pbstatuslist"].append(tmpObj)


    getIssuePblist("anquan",issueId,response_data,request,list_items_issue,iswholemodel)

    response_data["issuc"]="true"

    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
@login_required(login_url="/login/")
def jishu_fangan(request):
    try:
        if request.method == 'GET':
            isMobile = checkMobile(request)

            if isMobile:
                technicallist = Technical.objects.all().order_by('-id')
                templateName = 'TaskAndFlow/jishu_fangan_mobile.html'
            else:
                memberList = getPrjUserlist()

                page = int(request.GET.get('page', '1'))
                mingcheng = request.GET.get('mingcheng', '')
                if mingcheng:
                    technicallist =[ {'self':each,'ha':KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name if each.hazard_code else ''}  for each in  Technical.objects.filter(name__contains=mingcheng).order_by('-id')]
                else:
                    technicallist =[ {'self':each,'ha':KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name if each.hazard_code else ''}  for each in  Technical.objects.all().order_by('-id')]
                paginator = Paginator(technicallist, 10)
                listcount = len(technicallist)
                try:
                    technicallist = paginator.page(page)
                except:
                    technicallist = paginator.page(paginator.num_pages)

                templateName = 'TaskAndFlow/flowtemplate/jishu_fangan.html'
            return render_to_response(templateName, RequestContext(request, locals()))
        elif request.method == 'POST':  # 创建，交底，修改，跟踪
            def dochandle(docs,qid,t):
                mulu = getTypeDirectory('jishufangan')
                for FileId in docs:
                    print FileId
                    docId = int(FileId)
                    Doc2Relate.objects.create(relatetype=t, relateid=qid,
                                              creator=request.user, document_id=docId, createtime=datetime.datetime.now())
                    if mulu:
                        doc = Document.objects.get(id=docId)
                        doc.docdirectory.add(mulu)
                        movefiletoDir(doc,mulu)

            opt = request.POST.get('opt', 'create')
            response_data = {'issuc': 'true'}
            if opt == 'create':
                qnumber = request.POST.get('qnumber', '')
                qname = request.POST.get('qname', '')
                qcomment = request.POST.get('qcomment', '')
                qcreate_date = request.POST.get('qcreate_date', '')
                qdisclosure_date = request.POST.get('qdisclosure_date', '')
                qfuzeren = request.POST.get('qfuzeren', '0')
                weixianyuanid = request.POST.get('weixianyuanid', '0')
                try:
                    weixianyuan = KnowledgeHazardlist.objects.get(id=int(weixianyuanid))
                    hazard_code = weixianyuan.hazard_code
                except:
                    hazard_code = None
                Technical.objects.create(number=qnumber, name=qname, create_date=qcreate_date,
                                         disclosure_date=qdisclosure_date, hazard_code=hazard_code, comment=qcomment, user_id=int(qfuzeren))
            elif opt == 'xiugai':
                qsubmit_date = request.POST.get('qsubmit_date', '')
                qapprove_date = request.POST.get('qapprove_date', '')
                qid = int(request.POST.get('qid', '0'))
                changeTe = Technical.objects.get(id=int(qid))
                if qsubmit_date:
                    changeTe.submit_date = qsubmit_date
                if qapprove_date:
                    changeTe.approve_date = qapprove_date
                changeTe.save()
                docs = eval(request.POST.get('docs', '[]'))
                qid = int(request.POST.get('qid', '0'))
                dochandle(docs,qid, u"技术方案修改")
            elif opt == 'chakan':
                chaid = int(request.POST.get('chaid', '0'))
                if Technical.objects.filter(id=chaid).count()>0:
                    technicalitem =Technical.objects.filter(id=chaid)[0]
                    response_data["technicalitem"] = objtojson(Technical.objects.get(id=chaid))
                else:
                    response_data["technicalitem"] = None
                docids = [each.document_id for each in Doc2Relate.objects.filter(
                    relatetype__contains='技术方案', relateid=chaid)]
                print docids
                docs = [{"docid": each.id, "shortname": each.shortname, 'name': each.name}
                        for each in Document.objects.filter(id__in=docids)]
                response_data["docs"] = objtojson(docs)

            elif opt == 'genzong':
                docs = eval(request.POST.get('docs', '[]'))
                qid = int(request.POST.get('qid', '0'))
                dochandle(docs,qid, u"技术方案跟踪")
            elif opt == 'getmore':
                page = int(request.POST.get('page', '0'))
                start= page*10
                end = page*10+10
                if end>Technical.objects.all().count():
                    end=Technical.objects.all().count()
                response_data['more'] = objtojson(Technical.objects.all()[start:end])
            else:
                #1未完成，2已上报，3已审批，4已交底
                opth = {
                    'jiaodi':u'技术方案交底',
                    'shenpi':u'技术方案审批',
                    'shangchuan':u'技术方案上传'
                }
                optStatus = {
                    'jiaodi':4,
                    'shenpi':3,
                    'shangchuan':2
                }

                docs = eval(request.POST.get('docs', '[]'))
                qid = int(request.POST.get('qid', '0'))
                dochandle(docs,qid, opth[opt])

                qsubmit_date = request.POST.get('qsubmit_date', '')
                qapprove_date = request.POST.get('qapprove_date', '')
                qdisclosure_date = request.POST.get('qdisclosure_date', '')
   
                cs = Technical.objects.get(id=int(qid))
                if qsubmit_date:
                    cs.submit_date = qsubmit_date
                if qapprove_date:
                    cs.approve_date = qapprove_date
                if qdisclosure_date:
                    cs.disclosure_date = qdisclosure_date

                cs.status=optStatus.get(opt,1)
                cs.save()
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    except:
        traceback.print_exc()

@csrf_exempt
@login_required(login_url="/login/")
def jishu_fanganopt(request,id):
    try:
        if request.method=='GET':
            config={}
            ticket, appid, _ = fetch_ticket()

            sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.path)

            config = sign.sign()
            config["appid"] = appid
            technical = Technical.objects.get(id=id)
            docs = [each.document for each in Doc2Relate.objects.filter(relatetype__contains='技术方案', relateid=id)]
            templateName = 'TaskAndFlow/jishufangan/jishu_fangan_opt.html'
            return render_to_response(templateName, RequestContext(request, locals()))
        elif request.method=='POST':
            response_data = {'issuc': 'true'}
            opt = request.POST.get('opt','')
            opth = {
                'jiaodi':u'技术方案交底',
                'shenpi':u'技术方案审批',
                'shangchuan':u'技术方案上传',
                'genzong':u"技术方案跟踪"
            }
            optStatus = {
                'jiaodi':4,
                'shenpi':3,
                'shangchuan':2
            }
            technical = Technical.objects.get(id=id)
            try:
                technical.status=optStatus[opt]
                technical.save()
            except:
                print 'genzong', opt
            #手机端技术方案附件
            imageserverids = eval(request.POST.get('imageserverids','[]'))
            if imageserverids:
                uploadfile_weixin(imageserverids,id,'jishufangan', opth[opt], request.user, id)
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        traceback.print_exc()


@login_required(login_url="/login/")
def jishu_list(request):
    isMobile = checkMobile(request)

    if isMobile:
        return render_to_response('TaskAndFlow/jishu_list_mobile.html', RequestContext(request, locals()))
    else:
        return render_to_response('TaskAndFlow/jishu_list.html', RequestContext(request, locals()))


@login_required(login_url="/login/")
def jishu_jichu(request):
    templateName = 'TaskAndFlow/flowtemplate/jishu_jichu.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def jishu_chengxu(request):
    templateName = 'TaskAndFlow/flowtemplate/jishu_chengxu.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def jishu_jixuwenti(request):
    templateName = 'TaskAndFlow/flowtemplate/jishu_jixuwenti.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def jishu_jianceshi(request):
    templateName = 'TaskAndFlow/flowtemplate/jishu_jianceshi.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def jishu_guanbiao(request):
    templateName = 'TaskAndFlow/flowtemplate/jishu_guanbiao.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def issuecreate_html(request):
    try:
        issuetype = request.GET.get('issuetype', u'zhiliang')
        title = getTitleFromUrl(request,"/task/issue/list/?issuetype="+issuetype)
        issuetype = transIssueType(issuetype)

        FlowTemplateList = getUserFlowTempList(request.user,issuetype)
        print "1111111111111111111:"+str(len(FlowTemplateList))
        #FlowTemplateList = FlowTemplate.objects.filter(flowtype__name=issuetype)
        majorList = UserMajor.objects.all()
        curMajorId = None
        if FlowTemplateList:
            curMajorId = FlowTemplateList[0].major_id
        biaohao = getEventNumber(issuetype)
    except:
        traceback.print_exc()
    templateName = 'TaskAndFlow/flowtemplate/issuecreate.html'
    return render_to_response(templateName, RequestContext(request, locals()))




@login_required(login_url="/login/")
def anquan_biaodan(request):
    templateName = 'TaskAndFlow/flowtemplate/anquan_biaodan.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@csrf_exempt
@login_required(login_url="/login/")
def chankan(request, id):
    try:
        doclist = Doc2Relate.objects.filter(relatetype=u"质量验收",relateid=int(id))
        if doclist:
            fujian='true'
        acc = Acceptanceinfo.objects.get(id=int(id))
        bds = AcceptanceinfoForm.objects.filter(acceptanceinfo_id=int(id))
        if bds:
            display = 'true'

        if not acc.comment:
                acc.comment = ''
        if checkMobile(request):
            config = {}
            ticket, appid, _ = fetch_ticket()

            sign = Sign(ticket, "http://" +
                        request.META["HTTP_HOST"] + request.path)

            config = sign.sign()
            config["appid"] = appid
            templateName = 'TaskAndFlow/flowtemplate/zhiliangyanshouchakan_mobile.html'
        else:
            templateName = 'TaskAndFlow/flowtemplate/zhiliangyanshouchakan.html'
        return render_to_response(templateName, RequestContext(request, locals()))
    except:
        traceback.print_exc()

@csrf_exempt
@login_required(login_url="/login/")
def newyanshou(request, id):
    try:
        if request.method=='GET':
            acc = Acceptanceinfo.objects.get(id=int(id))
            imglist = Doc2Relate.objects.filter(relatetype=u"质量验收",relateid=int(id), document__filetype__contains="image")
            voiceList = Doc2Relate.objects.filter(relatetype=u"质量验收", relateid=int(id),  document__filetype__contains="audio")

            if not acc.comment:
                acc.comment = ''
            bds = AcceptanceinfoForm.objects.filter(acceptanceinfo_id=int(id))
            if bds:
                display = 'true'
            if checkMobile(request):
                config = {}
                ticket, appid, _ = fetch_ticket()

                sign = Sign(ticket, "http://" +
                            request.META["HTTP_HOST"] + request.path)

                config = sign.sign()
                config["appid"] = appid
                templateName = 'TaskAndFlow/flowtemplate/zhiliangyanshouaction_mobile.html'
            else:
                templateName = 'TaskAndFlow/flowtemplate/zhiliangyanshouaction.html'
            return render_to_response(templateName, RequestContext(request, locals()))
        elif request.method=='POST':
            def dochandle(docs,qid,t):
                mulu = getTypeDirectory('zhiliangyanshou')
                for FileId in docs:
                    print FileId
                    docId = int(FileId)
                    Doc2Relate.objects.create(relatetype=t, relateid=qid,
                                              creator=request.user, document_id=docId, createtime=datetime.datetime.now())
                    if mulu:
                        doc = Document.objects.get(id=docId)
                        doc.docdirectory.add(mulu)
                        movefiletoDir(doc,mulu)
            comment = request.POST.get('comment','')
            opt = request.POST.get('opt','')
            acc = Acceptanceinfo.objects.get(id=int(id))
            if comment:
                acc.comment = comment
            if opt=='yanshou':
                acc.status=2
            elif opt=='close':
                acc.status=3
            acc.save()
            RelateFileList = eval(request.POST.get('RelateFileList','[]'))
            if RelateFileList:
                dochandle(RelateFileList,int(id),"质量验收")

            imgList = eval(request.POST.get('imgList','[]'))
            if imgList:
                if uploadfile_weixin(imgList, acc.acceptancetype.name, 'zhiliangyanshou', '质量验收', request.user, int(id)):
                    raise Exception(u"问题修改,图片上传失败！")
            voiceid = request.POST.get('voiceId','')
            if voiceid:
                voiceList = []
                voiceList.append(voiceid)
                if fetchVoice_weixin(voiceList,  acc.acceptancetype.name, 'zhiliangyanshou', '质量验收', request.user, int(id)):
                    raise Exception(u"问题修改,语音上传失败！")


            return HttpResponse(json.dumps({'res': u'succ'}), content_type="application/json")
    except:
        traceback.print_exc()

@csrf_exempt
@login_required(login_url="/login/")
def guanjiandianyanshou(request, id):
    try:

        if request.method == "POST":

            rdata = [{"name": each.form.name, "content": each.form.content, 'id': each.form.id}
                     for each in AcceptanceinfoForm.objects.filter(acceptanceinfo_id=int(id))]

            return HttpResponse(json.dumps(rdata), content_type="application/json")
        elif request.method == "GET":
            # 改变id 的关键点状态
            acc = Acceptanceinfo.objects.get(id=int(id))
            acc.status = 2
            acc.save()
            templateName = 'TaskAndFlow/flowtemplate/guanjiandianyanshou.html'
            return render_to_response(templateName, RequestContext(request, locals()))
    except:
        traceback.print_exc()


@login_required(login_url="/login/")
def zhiliang_yanshou(request):
    try:
        # 关键点
        typeye = 1  # 区分关键点与工序分页效果
        acces = []
        curstatus = request.GET.get('curstatus', '0')
        tianjiaren = request.GET.get('tianjiaren', '')
        deadlineTimerange = request.GET.get('deadlineTimerange', '')


        if request.GET.has_key('deadlineTimerange'):
            typeye = 1
        elif request.GET.has_key('gxdeadlineTimerange'):
            typeye = 2

        startdate = None
        enddate = None

        if deadlineTimerange:
            startdate, enddate = GetDateRange(deadlineTimerange)
        acces = [{'id': each.id, 'status': each.status,'acceptancetype': each.acceptancetype.name,  'user': each.acceptuser,
                  'kjty': each.relatedspace_type, 'kjid': each.relatedspace_id, 'jzsj': each.finiishedtime,
                  'bds': [{'bdid': accef.form_id, 'bdname': accef.form.name} for accef in AcceptanceinfoForm.objects.filter(acceptanceinfo_id=each.id)]}
                  for each in Acceptanceinfo.objects.all().order_by("status")]
        statusRange = {'s': 0, 'p': 0, 'e': 0}
        sacces = []
        for a in acces:
            # 前台搜索筛选条件
            if deadlineTimerange:
                if a['jzsj'] < startdate or a['jzsj'] > enddate:
                    continue
            if curstatus != '0' and a['status'] != int(curstatus):
                continue

            if tianjiaren and tianjiaren not in a['user']:
                continue


            a['guanbiquanxian'] = 1

            try:
                # 获取空间全名
                a['kjys'] = ""
                if a['kjty'] == u'单位工程':
                    a['kjys'] = UnitProject.objects.get(id=a['kjid']).name
                elif a['kjty'] == u'楼层':
                    lc = Elevation.objects.get(id=a['kjid'])
                    a['kjys'] = UnitProject.objects.get(
                        id=lc.unitproject_id).name + lc.name + u'层'
                elif a['kjty'] == u'分区':
                    a['kjys'] = Zone.objects.get(id=a['kjid']).name
                elif a['kjty'] == u'构件组':
                    a['kjys'] = u'构件组:' + Pbgroup.objects.get(id=a['kjid']).number
                elif a['kjty'] == u'构件':
                    a['kjys'] = u'构件:' + PrecastBeam.objects.get(id=a['kjid']).sign
            except Exception as e:
                traceback.print_exc()
                pass

            sacces.append(a)
            # 分页
        paginator = Paginator(sacces, 15)
        listcount = len(sacces)
        try:
            page = int(request.GET.get('pagegjd'))
            typeye = 1
        except:
            page = 1
        try:
            sacces = paginator.page(page)
        except:
            sacces = paginator.page(paginator.num_pages)

        
    except:
        traceback.print_exc()

    templateName = 'TaskAndFlow/flowtemplate/zhiliang_yanshou.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@csrf_exempt
@login_required(login_url="/login/")
def optacceptance(request, id):
    try:
        if request.method == "DELETE":  # 删除关键点
            print u"删除"
            delacc = Acceptanceinfo.objects.get(id=int(id))
            if delacc.status != 1:
                return HttpResponse(json.dumps({'res': u'error', 'error': u'不能删除正在处理的元素'}), content_type="application/json")
            AcceptanceinfoForm.objects.filter(acceptanceinfo=delacc).delete()
            delacc.delete()
            return HttpResponse(json.dumps({'res': u'succ'}), content_type="application/json")
        if request.method == "POST":  # 删除关键点
            print u"关闭"
            delacc = Acceptanceinfo.objects.get(id=int(id))
            delacc.status = 3
            delacc.save()
            #表单归档
            Form2FileAcceptance(delacc)
            return HttpResponse(json.dumps({'res': u'succ'}), content_type="application/json")
    except:
        traceback.print_exc()
    return HttpResponse(json.dumps({'res': u'error'}), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def createacceptance(request):
    try:
        if request.method == "GET":
            # 添加质量关键点页面
            acceptancetpList = Acceptancetype.objects.all()
            majorList = UserMajor.objects.all()
            if acceptancetpList:
                curMajorId = acceptancetpList[0].major_id
            templateName = 'TaskAndFlow/flowtemplate/acceptancecreate.html'
            return render_to_response(templateName, RequestContext(request, locals()))

        elif request.method == "POST":  # 添加
            def dochandle(docs,qid,t):
                mulu = getTypeDirectory('zhiliangyanshou')
                for FileId in docs:
                    print FileId
                    docId = int(FileId)
                    Doc2Relate.objects.create(relatetype=t, relateid=qid,
                                              creator=request.user, document_id=docId, createtime=datetime.datetime.now())
                    if mulu:
                        doc = Document.objects.get(id=docId)
                        doc.docdirectory.add(mulu)
                        movefiletoDir(doc,mulu)
            deadline = request.POST.get('deadline', None)
            acceptancetype = request.POST.get('Acceptancetype', '')  # 验收类型
            RelateFileList = request.POST.get('RelateFileList', '')  # 附件
            selectedKJ = request.POST.get('selectedKJ', '')  # 关联元素
            bdids = eval(request.POST.get('bdids', '[]'))  # 表单list
            comment = request.POST.get('comment', None)
            if AcceptancetypeFormtmp.objects.get(acceptancetype_id=int(acceptancetype)).formtpl:
                if not bdids:
                    return HttpResponse(json.dumps({'res': 'error', 'error': u'必须填写至少一个表单'}), content_type="application/json")
            if not deadline:
                return HttpResponse(json.dumps({'res': 'error', 'error': u'请填写截止日期'}), content_type="application/json")
            # model floor_110 113zone_1 unitprj_3
            newacc = None
            if selectedKJ != 'model' and selectedKJ:
                kjys = selectedKJ.split('_')
                kjty = kjys[0]
                kjid = kjys[1]
                if kjty == 'unitprj':
                    kjty = u'单位工程'
                elif kjty == 'floor':
                    kjty = u'楼层'
                elif 'zone' in kjty:
                    kjty = u'分区'
                # status 1 待处理  2处理中 3处理完成
                newacc = Acceptanceinfo.objects.create(relatedspace_type=kjty,comment=comment, relatedspace_id=int(
                    kjid), finiishedtime=deadline, acceptuser=request.user, status=1,acceptancetype_id=int(acceptancetype))
            else:
                newacc = Acceptanceinfo.objects.create(
                    finiishedtime=deadline,comment=comment, acceptuser=request.user, status=1,acceptancetype_id=int(acceptancetype))
            if bdids:
                for bdid in bdids:
                    AcceptanceinfoForm.objects.create(
                        acceptanceinfo=newacc, form_id=int(bdid))
            if RelateFileList:

                dochandle(RelateFileList[:-1].split(","),newacc.id,"质量验收")
            # 创建质量关键点
            # {"qnumber":"1488370686000","qdescribe":"123","Acceptancetype":"2","RelateFileList":"269,","selectedGJs":"[{\"typetable\":\"任务\",\"relatedid\":\"2099\"}]","bdids":"[\"94\"]"}
            # print u"创建质量关键点"
            return HttpResponse(json.dumps({'res': u'succ'}), content_type="application/json")
    except:
        traceback.print_exc()
        return HttpResponse(json.dumps({'res': u'succ'}), content_type="application/json")


@login_required(login_url="/login/")
def huiyi(request):
    huiyitype = request.GET.get('huiyitype', '质量')
    templateName = 'TaskAndFlow/flowtemplate/huiyi.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@csrf_exempt
@login_required(login_url="/login/")
def issue_list_forgeneral(request):
    rdata={'res': u'succ'}
    rdata['ilist']=[]
    try:
        issuetype = request.GET.get('issuetype', u'zhiliang')
        if issuetype==u'zhiliang':
            ##获取问质量问题列表
            rdata['ilist'] = getUserIssueList(request.user,u'质量问题')

        elif issuetype==u'anquan':
            # 获取问题列表
            print u"获取问题列表"
            rdata['ilist'] = getUserIssueList(request.user, u'安全问题')

        elif issuetype==u'zhiliangyanshou':
            ##获取质量关键点列表
            acces = [{'id': each.id, 'status': each.status, 'user': each.acceptuser.truename, 'kjty': each.relatedspace_type, 'kjid': each.relatedspace_id, 'jzsj': str(each.finiishedtime), 'bdids': [
                accef.form_id for accef in AcceptanceinfoForm.objects.filter(acceptanceinfo_id=each.id)]} for each in Acceptanceinfo.objects.all().order_by("status")]
            for a in acces:
                # 获取空间全名
                if a['kjty'] == u'单位工程':
                    a['kjys'] = UnitProject.objects.get(id=a['kjid']).name
                elif a['kjty'] == u'楼层':
                    lc = Elevation.objects.get(id=a['kjid'])
                    a['kjys'] = UnitProject.objects.get(
                        id=lc.unitproject_id).name + lc.name + u'层'
                elif a['kjty'] == u'分区':
                    a['kjys'] = Zone.objects.get(id=a['kjid']).name
                elif a['kjty'] == u'构件':
                    a['kjys'] = u'构件:' + PrecastBeam.objects.get(id=a['kjid']).sign
                else:
                    # continue
                    a['kjys'] = u'无空间位置'
                rdata['ilist'].append(a)

        elif issuetype==u'weixianyuan':
            def getfullname(each):
                if each.relatedspace_type == u'单位工程':
                    return UnitProject.objects.get(
                        id=each.relatedspace_id).name + KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name
                elif each.relatedspace_type == u'楼层':
                    lc = Elevation.objects.get(id=each.relatedspace_id)
                    return UnitProject.objects.get(
                        id=lc.unitproject_id).name + lc.name + u'层' + KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name
                elif each.relatedspace_type == u'分区':
                    return Zone.objects.get(
                        id=each.relatedspace_id).name + KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name
                else:
                    return KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name
            rdata['ilist'] = [{'name': getfullname(each), 'id': each.id, 'status':each.curstatus_id,'curstatus': each.curstatus.statusname} for each in Hazardevent.objects.filter(his_date=datetime.date.today()).order_by('curstatus')]
    except:
        traceback.print_exc()

    return HttpResponse(json.dumps(rdata), content_type="application/json")

@login_required(login_url="/login/")
def issue_list(request):
    try:
        # 查询条件
        issuetypeorg = request.GET.get('issuetype', 'zhiliang')
        curdealstep = request.GET.get('curdealstep', '0')
        fuzefenbao = int(request.GET.get('fuzefenbao', '0'))
        createtTimerange = request.GET.get('createtTimerange', '')

        title = getTitleFromUrl(request,"/task/issue/list/?issuetype="+issuetypeorg)
        issuetype = transIssueType(issuetypeorg)

        list_items = []
        if createtTimerange:
            startdate, enddate = GetDateRange(createtTimerange)
            if fuzefenbao:
                list_items = projectevent.objects.filter(
                    template__flowtype__name=issuetype, createtime__range=(startdate, enddate),
                    template__major__id=fuzefenbao).order_by("curdealstep","deadline")
            else:
                list_items = projectevent.objects.filter(
                    template__flowtype__name=issuetype, createtime__range=(startdate, enddate)).order_by("curdealstep","deadline")
        else:
            if fuzefenbao:
                list_items = projectevent.objects.filter(template__flowtype__name=issuetype,
                                                        template__major__id=fuzefenbao).order_by("curdealstep","deadline")
            else:
                list_items = projectevent.objects.filter(template__flowtype__name=issuetype).order_by("curdealstep","deadline")

        issuelistUnDo = []
        issuelistSaved = []
        issuelistDoing = []
        issuelistDone = []
        # 获取页数
        page = int(request.GET.get('page', '1'))
        # startindex = (page-1)*10+1
        # endindex = page*10
        # index = 0;
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
        for each in EventStepOperation.objects.all():
            if not mapeventuser.has_key(each.eventstep.projectevent_id):
                mapeventuser[each.eventstep.projectevent_id] = set()
                mapeventuser[each.eventstep.projectevent_id].add(each.actor_id)
            else:
                mapeventuser[each.eventstep.projectevent_id].add(each.actor_id)

        mapusername = { each.id:each.truename for each in getPrjUserlist() }

        for each in list_items:
            # 只有保存的用户可以编辑 pgb
            if each.issave and request.user.id != each.saveuser_id:
                continue

            # 当前用户没有权限 且之前操作步骤指派人没有我
            #eventoprlist = EventStepOperation.objects.filter(Q(eventstep__projectevent=each.id)).order_by("-oprtime")
            # if not checkEventRight(request.user, each.curflowstep.id) and \
            #    eventoprlist.filter(Q(actor=request.user)).count() == 0:
            #    if not checkEventNeedWatch(each, request.user):
            #         continue
            if (mapstepactor.has_key(each.curflowstep_id) and request.user.id not in mapstepactor[each.curflowstep_id]) and  \
               (mapstepwatch.has_key(each.curflowstep_id) and request.user.id not in mapstepwatch[each.curflowstep_id]) and\
               request.user.id not in mapeventuser[each.id]:
                continue

            issue = {}

            issue["dangqianjieduan"] = GetJianDuanFromStep(each)

            if  curdealstep != "0":
                if curdealstep != issue["dangqianjieduan"]["jianduan"]:
                    continue

            if issue["dangqianjieduan"]["jianduan"] == u"已结束":
                issuelistDone.append(issue)
            elif issue["dangqianjieduan"]["jianduan"] == u"正在处理":
                issuelistDoing.append(issue)
            elif issue["dangqianjieduan"]["jianduan"] == u"待编辑":
                issuelistSaved.append(issue)
            else:
                issuelistUnDo.append(issue)

            issue["each"] = each
        
        issuelist = []
        issuelist.extend(issuelistSaved)
        issuelist.extend(issuelistUnDo)
        issuelist.extend(issuelistDoing)
        issuelist.extend(issuelistDone)

        print "11111111111111111111111:"+str(time.time() - starttime)

        paginator = Paginator(issuelist, 10)
        listcount = len(issuelist)
        try:
            issuelist = paginator.page(page)
        except:
            issuelist = paginator.page(paginator.num_pages)

        # FlowTemplateList = FlowTemplate.objects.filter(flowtype__name=issuetype)
        for issue in issuelist:
            each = issue["each"]
            issue["issueId"] = each.id
            issue["number"] = each.number
            issue["describe"] = each.describe
            issue["faqiren"] = mapusername[each.createuser_id] if mapusername.has_key(each.createuser_id) else "--"
            issue["faqishijian"] = each.createtime
            issue["dangqianfuzeren"] = ""
            if mapstepactor.has_key(each.curflowstep_id):
                issue["dangqianfuzeren"] = ','.join([mapusername[stepuser] if mapusername.has_key(stepuser) else "--" for stepuser in mapstepactor[each.curflowstep_id]])

            if each.issave:
                issue["needdeal"] = True
            else:
                issue["needdeal"] = checkEventNeedDeal(each, request.user)


            if EventStepOperation.objects.filter(Q(eventstep__projectevent_id=each.id)).count()>0:
                lasteventopr = EventStepOperation.objects.filter(Q(eventstep__projectevent_id=each.id)).order_by("-oprtime")[0]
                if lasteventopr.actor_id==request.user.id and issue["dangqianjieduan"]["jianduan"] not in (u"已结束",u"待编辑"):
                    issue["canupdate"] = True

            glyss = ProjecteventElement.objects.filter(event_id=each.id)
            issue["guanlianyuansu"] = []
            issue["guanlianyuansudis"]=""
            for glys in glyss:
                s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
                issue["guanlianyuansu"].append(s)
                issue["guanlianyuansudis"] +=s+","
            issue["guanlianyuansudis"]=issue["guanlianyuansudis"][:-1]


        print "222222222222222222222:"+str(time.time() - starttime)

        majorList = UserMajor.objects.all()
        if checkMobile(request):
            templateName = 'TaskAndFlow/zhiliang_list_mobile.html'
        else:
            templateName = 'TaskAndFlow/flowtemplate/issue_list.html'
    except:
        if checkMobile(request):
            templateName = 'TaskAndFlow/zhiliang_list_mobile.html'
        else:
            templateName = 'TaskAndFlow/flowtemplate/issue_list.html'
        traceback.print_exc()
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
@check_permission
def anquan_general(request):
    title = getTitleFromUrl(request,request.get_full_path())
    if CustomInfo.objects.filter(infotype='hide_function'):
        hide_function =eval(CustomInfo.objects.filter(infotype='hide_function')[0].custominfo)
    templateName = 'TaskAndFlow/flowtemplate/anquan_general.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@csrf_exempt
@login_required(login_url="/login/")
def anquan_jiancha(request):
    if request.method=="GET":
        check_list=Pbtypetimedcheck.objects.all()

        pbtypeList = PBType.objects.filter(major_id=17)
        formlist = BiaoDanMuBan.objects.filter(formtype__name=u'安全设施待检')
        templateName = 'TaskAndFlow/flowtemplate/anquan_jiancha.html'
        return render_to_response(templateName, RequestContext(request, locals()))
    else:
        response_data={}
        response_data["issuc"]="false"
        try:
            opt=request.POST.get('opt', '')
            if opt=="create":
                name=request.POST.get('new_name', '')
                pbtype=int(request.POST.get('new_pbtype', '0'))
                zhouqitype = request.POST.get('zhouqitype', '')
                createtime=request.POST.get('createtime', '')
                relateform = int(request.POST.get('relateform', '0'))
                if relateform==0:
                    relateform = None

                Pbtypetimedcheck.objects.create(name=name,pbtype_id=pbtype,task_cycle_type=zhouqitype,
                                                task_cycle=createtime,relatedformtemplate_id=relateform)
            elif opt=="delete":
                id=int(request.POST.get('id', '0'))
                Pbtypetimedcheck.objects.filter(id=id).delete()
            elif opt=="edit":
                pass
            else:
                raise Exception(u'未知操作！')


            response_data["issuc"]="true"
        except Exception, e:
            traceback.print_exc()
            response_data['error'] = '%s' % e
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def anquan_jianchadetail(request):
    if request.method=="GET":
        jianchaId=int(request.GET.get('jianchaId', '0'))
        jiachan=Pbtypetimedcheck.objects.get(id=jianchaId)

        pblist = PbtimedcheckRecord.objects.filter(timedcheck=jiachan,status_reset_time=jiachan.status_reset_time)
        templateName = 'TaskAndFlow/flowtemplate/anquan_jiancha_detail.html'
        return render_to_response(templateName, RequestContext(request, locals()))

@login_required(login_url="/login/")
def anquan_jiancharead(request):
    response_data={}
    response_data["issuc"]="false"
    response_data["mubans"] = []
    try:
        goujians = request.POST.get("goujian",None)

        goujians = goujians.split(',')
        mubans = []
        elelist = Monitoringelement.objects.filter(qrcode__in=goujians)
        for ele in elelist:
            reclist = PbtimedcheckRecord.objects.filter(monitoring=ele,isneedcheck=True).order_by("-status_reset_time")
            if reclist:
                rec = reclist[0]
                if rec.timedcheck.relatedformtemplate:
                    response_data["issuc"]="true"
                    tmp = {}
                    tmp["id"]=rec.timedcheck.relatedformtemplate.id
                    tmp["name"]=rec.timedcheck.relatedformtemplate.name
                    response_data["mubans"].append()
                    break
    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def anquan_jianchajiancha(request):
    if request.method=="GET":
        jianchaId=request.GET.get('jianchaId', None)
        RecordId=request.GET.get('RecordId', None)
        monitorings = None
        jiancha = None
        if RecordId:
            rec = PbtimedcheckRecord.objects.get(id=RecordId)
            monitorings = rec.monitoring.qrcode
            jiancha = rec.timedcheck
        elif jianchaId:
            jiancha=Pbtypetimedcheck.objects.get(id=jianchaId)
            reclist = PbtimedcheckRecord.objects.filter(timedcheck=jiancha,status_reset_time=jiancha.status_reset_time)
            for rec in reclist:
                if monitorings:
                    monitorings = monitorings+","+rec.monitoring.qrcode
                else:
                    monitorings = rec.monitoring.qrcode

        if checkMobile(request):
            config = getMobileConfig(request)
            templateName = 'TaskAndFlow/flowtemplate_mobile/anquan_jiancha_mobile.html'
        else:
            templateName = 'TaskAndFlow/flowtemplate/anquan_jiancha_jiancha.html'
        return render_to_response(templateName, RequestContext(request, locals()))
    else:
        response_data={}
        response_data["issuc"]="false"
        try:
            goujians = request.POST.get("goujian",None)
            beizhu=request.POST.get('beizhu','')
            imgInfo = request.POST.get('zhijian',None)
            relatefiles = eval(request.POST.get("relatefiles","[]"))
            relatebdids = eval(request.POST.get("relatebdids","[]"))
            lururq = request.POST.get('lururq',None)
            if lururq:
                lururq = datetime.datetime.strptime(lururq,'%Y-%m-%d %H:%M')
            else:
                lururq = datetime.datetime.now()

            goujians = goujians.split(',')
            msg = "检查成功"
            errorlist = []
            timecheck = set()
            elelist = Monitoringelement.objects.filter(qrcode__in=goujians)
            for ele in elelist:
                reclist = PbtimedcheckRecord.objects.filter(monitoring=ele,isneedcheck=True).order_by("-status_reset_time")
                if reclist:
                    rec = reclist[0]
                    rec.actor = request.user
                    rec.time = lururq
                    rec.description = beizhu
                    rec.isneedcheck = False
                    if relatebdids:
                        rec.related_form_id = relatebdids[0]
                    rec.save()

                    if imgInfo and ':' in imgInfo:
                        imgList=imgInfo.split(':')[1].split(';')
                        uploadfile_weixin(imgList,'anquanjiancha','anquanjiancha', '安全检查记录', request.user, rec.id)
                    if len(relatefiles)>0:
                        dir = getTypeDirectory('anquanjiancha',None)
                        for docId in relatefiles:
                            doc = Document.objects.get(id=int(docId))
                            Doc2Relate.objects.create(relatetype='安全检查记录', relateid=rec.id, creator_id=request.user.id,
                                                      document_id=doc.id, createtime=datetime.datetime.now())
                            if dir:
                                doc.docdirectory.add(dir)
                                movefiletoDir(doc,dir)


                    timecheck.add(rec.timedcheck)
                else:
                    errorlist.append(ele)


            for check in timecheck:
                if not PbtimedcheckRecord.objects.filter(timedcheck=check,status_reset_time=check.status_reset_time,isneedcheck=True):
                    check.isneedcheck = False
                    check.save()


            #raise Exception(u'未知操作！')
            response_data["msg"] = msg
            response_data["issuc"]="true"
        except Exception, e:
            traceback.print_exc()
            response_data['error'] = '%s' % e
        return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url="/login/")
def anquan_jianchatrace(request):
    RecordId=request.GET.get('RecordId', None)
    rec = PbtimedcheckRecord.objects.get(id=RecordId)
    reclist = PbtimedcheckRecord.objects.filter(timedcheck=rec.timedcheck,monitoring=rec.monitoring).order_by("-status_reset_time")[:5]
    reclistWithDoc = []
    for each in reclist:
        tmp = {}
        tmp["rec"] = each
        doclist = Doc2Relate.objects.filter(relatetype='安全检查记录', relateid=each.id)
        tmp["doclist"] = doclist
        reclistWithDoc.append(tmp)

    return render_to_response('TaskAndFlow/flowtemplate/anquan_jiancha_trace.html', RequestContext(request, locals()))

@login_required(login_url="/login/")
def jiancha_getpbstatuslist(request):
    list_items = filterPbListRequest(request)

    iswholemodel = request.GET.get('_isWholeModel', '')


    response_data = {}
    response_data["pbstatuslist"]=[]
    response_data["jianchapblist"] = []
    jianchaId = request.GET.get('jianchaId', None)
    jianchalist = Pbtypetimedcheck.objects.filter(isneedcheck=True)

    if jianchaId:
        jianchalist=jianchalist.filter(id=jianchaId)

    pblistall = []
    for jiancha in jianchalist:
        PbGrpIdlist=[]
        PbIdlist=[]
        reclist = PbtimedcheckRecord.objects.filter(timedcheck=jiancha,isneedcheck=True,status_reset_time=jiancha.status_reset_time)
        for ele in reclist:
            if ele.monitoring.typetable=="构件组":
                PbGrpIdlist.append(ele.monitoring.relatedid)
            elif ele.monitoring.typetable=="构件":
                PbIdlist.append(ele.monitoring.relatedid)
            else:
                pass

        if len(PbGrpIdlist)>0:
            pbgrppblist = Pbgrouprelation.objects.filter(pbgroup__in=PbGrpIdlist).values_list('pb_id', flat=True)
            PbIdlist.extend(pbgrppblist)


        list_issue_pbs=list_items.filter( Q(id__in=PbIdlist)).exclude(lvmdbid__isnull=True).values_list('lvmdbid', flat=True)

        tmpObj = {}
        tmpObj["jiancha"] = jiancha.id
        tmpObj["pblist"] = map(int,map(str,list_issue_pbs))
        response_data["jianchapblist"].append(tmpObj)

        pblistall.extend(list_issue_pbs)

    tmpObj = {}
    tmpObj["type"]="needtick"
    color = "#FF0000"
    tmpObj["color"] = color
    tmpObj["pblist"] = []
    for eachpb in set(pblistall):
        tmpPb = {}
        tmpPb["lvmdbid"] = eachpb
        tmpObj["pblist"].append(tmpPb)
    response_data["pbstatuslist"].append(tmpObj)


    response_data["issuc"]="true"

    #print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def jixie_general(request):
    anquan_list = projectevent.objects.filter(
        template__flowtype__name="安全问题").order_by("deadline")
    cm_list = ConstructionMachine.objects.all().exclude(cmtype__name="设施")
    cm_status_list = CMStatus.objects.all()

    templateName = 'TaskAndFlow/flowtemplate/anquan_jixie.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def jixie_list(request):
    if checkMobile(request):
        config = {}
        ticket, appid, _ = fetch_ticket()

        sign = Sign(ticket, "http://" +
                    request.META["HTTP_HOST"] + request.path)

        config = sign.sign()
        config["appid"] = appid

        templateName = 'TaskAndFlow/goujian_list_mobile.html'
    else:
        list_items = ConstructionMachine.objects.filter(cmtype__name="设施")
        cm_status_list = CMStatus.objects.all()
        cm_type_list = CMType.objects.all()

        if request.method == 'GET':
            groupid = request.GET.get('number', '')
            progress = int(request.GET.get('progress', '0'))
            gtype = int(request.GET.get('gtype', '0'))
            hzstatus = int(request.GET.get('pbstatus', '0'))
            orderby = request.GET.get('orderby', 'id')
            clickcount = request.GET.get('clickcount', '0')

        paginator = Paginator(list_items, 20)
        listcount = len(list_items)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            list_items = paginator.page(page)
        except:
            list_items = paginator.page(paginator.num_pages)
        templateName = 'TaskAndFlow/anquan_jixie_list.html'

    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
@check_permission
def sheshi_general(request):

    jianchalist = Pbtypetimedcheck.objects.all()

    templateName = 'TaskAndFlow/flowtemplate/anquan_sheshi.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def sheshi_list(request):
    if checkMobile(request):
        config = {}
        ticket, appid, _ = fetch_ticket()

        sign = Sign(ticket, "http://" +
                    request.META["HTTP_HOST"] + request.path)

        config = sign.sign()
        config["appid"] = appid

        templateName = 'TaskAndFlow/goujian_list_mobile.html'
    else:
        list_items = ConstructionMachine.objects.filter(cmtype__name="设施")
        cm_status_list = CMStatus.objects.all()
        cm_type_list = CMType.objects.all()

        if request.method == 'GET':
            groupid = request.GET.get('number', '')
            progress = int(request.GET.get('progress', '0'))
            gtype = int(request.GET.get('gtype', '0'))
            hzstatus = int(request.GET.get('pbstatus', '0'))
            orderby = request.GET.get('orderby', 'id')
            clickcount = request.GET.get('clickcount', '0')

        paginator = Paginator(list_items, 20)
        listcount = len(list_items)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            list_items = paginator.page(page)
        except:
            list_items = paginator.page(paginator.num_pages)
        templateName = 'TaskAndFlow/anquan_sheshi_list.html'

    return render_to_response(templateName, RequestContext(request, locals()))


def get_hazard_event_tree(request):
    try:
        response_data = {}
        response_data["id"] = "allhazardevent"
        response_data["text"] = "危险源"
        response_data["icon"] = "/img/Catalog.png"
        response_data["state"] = {'opened': True}

        response_data["children"] = []

        # 七天去重
        today = datetime.date.today()
        day7 = today + datetime.timedelta(-7)
        quchong = []
        # __lt=start 小于某个时间
        #__range=(start_date, end_date) 时间段
        for each in Hazardevent.objects.filter(his_date__gt=day7):
            qc = str(each.hazard_code) + each.relatedspace_type + \
                str(each.relatedspace_id)
            if qc in quchong:
                continue
            quchong.append(qc)
            tmp = {}
            info = GetRelateTypeInfo(each.relatedspace_type, each.relatedspace_id)
            
            tmp['text'] = info+KnowledgeHazardlist.objects.get(hazard_code=each.hazard_code).hazard_name

            tmp['icon'] = False
            tmp['id'] = each.id
            response_data["children"].append(tmp)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        traceback.print_exc()


def get_hazard_tree(request):
    try:
        id = request.GET.get('id', '')
        response_data = {}
        child_list = []

        if id == '#':
            response_data["id"] = "pbtype"
            response_data["text"] = "危险源分类"
            response_data["icon"] = "/img/Catalog.png"
            response_data["state"] = {'opened': True}

            treelist =KnowledgeHazardlist.objects.filter(parent_id__isnull=True).exclude(hazard_name="特大")#.values_list('hazard_grade').distinct()
            for each in treelist:
                child_data = {}
                child_data["id"] = each.id
                child_data["text"] = each.hazard_name
                child_data["icon"] = "/img/majortype2.png"
                child_data["children"] = True
                child_data["data"] = {'major': "",'majorid':"0"}
                child_list.append(child_data)

            response_data["children"] = child_list
        else:
            child_list = []

            treelist = KnowledgeHazardlist.objects.filter(parent_id=int(id))
            for each in treelist:
                child_data = {}
                child_data["id"] = str(each.id)
                child_data["text"] = each.hazard_name
                if each.major:
                    child_data["data"] = {'major': each.major.name,'majorid': each.major_id}
                else:
                    child_data["data"] = {'major': "",'majorid': "0"}
                if KnowledgeHazardlist.objects.filter(parent=each).count() > 0:
                    child_data["icon"] = "/img/majortype2.png"
                    child_data["children"] = True
                else:
                    child_data["icon"] = False
                child_list.append(child_data)

            response_data = child_list

        # print json.dumps(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except:
        traceback.print_exc()


def get_sheshi_tree(request):
    id = request.GET.get('id', '')
    response_data = {}
    child_list = []

    if id == '#':
        response_data["id"] = "cmtype"
        response_data["text"] = "设施类型"
        response_data["icon"] = "/img/Catalog.png"
        response_data["state"] = {'opened': True}

        flag = 0
        for each in CMType.objects.filter(name="设施"):
            child_list = [{"id": str(flag) + "-1", "text": "施工用电"},
                          {"id": str(flag) + "-2", "text": "临边管理"},
                          {"id": str(flag) + "-3", "text": "牌价管理"},
                          {"id": str(flag) + "-4", "text": "周转材料管理"},
                          {"id": str(flag) + "-5", "text": "安全通道"},
                          {"id": str(flag) + "-6", "text": "围墙"},
                          {"id": str(flag) + "-7", "text": "沉淀池"},
                          {"id": str(flag) + "-8", "text": "排水沟"},
                          {"id": str(flag) + "-9", "text": "P2.5临监"},
                          {"id": str(flag) + "-10", "text": "喷淋"},
                          {"id": str(flag) + "-11", "text": "办公室"},
                          {"id": str(flag) + "-12", "text": "办公室"},
                          {"id": str(flag) + "-13", "text": "监控系统"},
                          ]

        response_data["children"] = child_list

    # print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_jixie_tree(request):
    id = request.GET.get('id', '')
    response_data = {}
    child_list = []

    if id == '#':
        response_data["id"] = "cmtype"
        response_data["text"] = "机械类型"
        response_data["icon"] = "/img/Catalog.png"
        response_data["state"] = {'opened': True}

        flag = 0
        for each in CMType.objects.all().exclude(name="设施"):
            flag += 1
            child_data = {}
            child_data["id"] = str(each.id)
            child_data["text"] = each.name
            child_data["icon"] = "/img/majortype2.png"

            child_list.append(child_data)

        response_data["children"] = child_list

    # print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def issue_createconfig(request):
    issuetype = request.GET.get('issuetype', u'质量问题')

    response_data = {}
    response_data["dealTemplateList"] = []

    FlowTemplateList = FlowTemplate.objects.filter(flowtype__name=issuetype)
    for each in FlowTemplateList:
        tmpObj = {}
        tmpObj["id"] = each.id
        tmpObj["name"] = each.name
        response_data["dealTemplateList"].append(tmpObj)

    response_data["issuetypeList"] = []
    issuetypeList = FlowType.objects.all()
    for each in issuetypeList:
        tmpObj = {}
        tmpObj["id"] = each.id
        tmpObj["name"] = each.name
        response_data["issuetypeList"].append(tmpObj)

    response_data["issuc"] = "true"

    # print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def getrelatetype(request):
    relatetype = request.GET.get('relatetype', u'构件')
    qitem = request.GET.get('q', u'')

    response_data = {}
    response_data["items"] = []

    if relatetype == u"构件":
        if PrecastBeam.objects.filter(sign__icontains=qitem).count() > 50:
            pblist = PrecastBeam.objects.filter(sign__icontains=qitem)[0:50]
        else:
            pblist = PrecastBeam.objects.filter(sign__icontains=qitem)
        for each in pblist:
            tmpObj = {}
            tmpObj["id"] = each.id
            tmpObj["text"] = each.sign
            response_data["items"].append(tmpObj)
    elif relatetype == u"任务":
        if ProjectTask.objects.filter(name__icontains=qitem).count() > 50:
            tasklist = ProjectTask.objects.filter(name__icontains=qitem)[0:50]
        else:
            tasklist = ProjectTask.objects.filter(name__icontains=qitem)
        for each in tasklist:
            tmpObj = {}
            tmpObj["id"] = each.id
            tmpObj["text"] = each.name
            response_data["items"].append(tmpObj)

    # response_data["issuc"]="true"

    # print json.dumps(response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def getacceptancetypeform(request):
    acceptancetype = int(request.GET.get('acceptancetype', 0))
    response_data = {}
    response_data['mubans'] = []
    try:
        afs = None
        print "acceptancetype", acceptancetype
        if acceptancetype:
            '''质量验收工作类型表单模板关系'''
            afs = AcceptancetypeFormtmp.objects.filter(
                acceptancetype_id=acceptancetype)

        else:
            afs = AcceptancetypeFormtmp.objects.all()

        for af in afs:
            print af.id
            m = BiaoDanMuBan.objects.get(id=af.formtpl_id)
            print m.id
            response_data['mubans'].append({'id': m.id, 'name': m.name})
    except:
        traceback.print_exc()
    print response_data
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def getmajortemplate(request):
    major = int(request.GET.get('major', u'0'))
    issuetype = request.GET.get('issuetype', u'质量问题')
    # print issuetype
    response_data = {}
    response_data["TemplateList"] = []
    try:
        TemplateList = getUserFlowTempList(request.user,issuetype)

        for each in TemplateList:
            if major != 0 and each.major_id!=major:
                continue
            tmpObj = {}
            tmpObj["id"] = each.id
            tmpObj["name"] = each.name
            response_data["TemplateList"].append(tmpObj)
        response_data["issuc"] = "true"
        # print json.dumps(response_data)
    except Exception, e:
        print e
        response_data["error"] = "处理异常！"
        response_data["issuc"] = "false"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def getissuetypetemplate(request):
    issuetype = request.GET.get('issuetype', u'质量问题')
    # print issuetype
    response_data = {}
    response_data["TemplateList"] = []
    try:
        TemplateList = FlowTemplate.objects.filter(flowtype__name=issuetype)

        for each in TemplateList:
            tmpObj = {}
            tmpObj["id"] = each.id
            tmpObj["name"] = each.name
            response_data["TemplateList"].append(tmpObj)
        response_data["issuc"] = "true"
        # print json.dumps(response_data)
    except Exception, e:
        print e
        response_data["error"] = "处理异常！"
        response_data["issuc"] = "false"

    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url="/login/")
def issuedeal(request, id):
    issueId = id
    issave = projectevent.objects.get(id=issueId).issave


    curEventsteplist = Eventstep.objects.filter(
        Q(projectevent_id=id)).values_list("id")
    issueoprlist = EventStepOperation.objects.filter(
        eventstep__in=curEventsteplist).order_by('oprtime')

    issueoprlistWithDoc = []
    for opr in issueoprlist:
        # 获取表单
        tmp = {}
        tmp['bds'] = []
        for eventstepid in curEventsteplist:
            eventstep = Eventstep.objects.get(id=int(eventstepid[0]))
            bd = {}
            if eventstep.relatedform:
                bd["bdid"] = eventstep.relatedform.id
                bd["bdname"] = eventstep.relatedform.name
            if bd:
                tmp['bds'].append(bd)

        tmp["issueopr"] = opr
        imglist = Doc2Relate.objects.filter(Q(relatetype=u"事件步骤操作") & Q(relateid=opr.id) & Q( document__filetype__contains="image"))
        tmp["issueoprimg"] = imglist
        doclist = Doc2Relate.objects.filter(Q(relatetype=u"事件步骤操作") & Q(relateid=opr.id)).exclude(document__filetype__contains="image")
        tmp["issueoprdoc"] = doclist
        issueoprlistWithDoc.append(tmp)

    return render_to_response('TaskAndFlow/flowtemplate/issue_deal.html', RequestContext(request, locals()))


@login_required(login_url="/login/")
def issue_dealconfig(request):
    issueId = int(request.GET.get('issueId', '0'))
    response_data = {}
    try:
        each = projectevent.objects.get(id=issueId)

        issue = {}
        issue["issueId"] = each.id
        issue["number"] = each.number
        issue["describe"] = each.describe
        issue["faqiren"] = each.createuser.truename
        issue["faqishijian"] = str(each.createtime)
        issue["dangqianbuzhou"] = each.curflowstep.name
        issue["major"] = each.template.major.name
        issue["issave"] = str(each.issave)
        issue["stepid"] = each.curflowstep_id
        issue["needfile"] = getDealNeedFile(each)
        issue["defaultcomment"] = each.curflowstep.defaultcomment if each.curflowstep.defaultcomment else ''

        glyss = ProjecteventElement.objects.filter(event_id=issueId)
        guanlianyuansudis=""
        for glys in glyss:
            s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
            guanlianyuansudis +=s+","
        guanlianyuansudis=guanlianyuansudis[:-1]
        issue["guanlianyuansudis"] = guanlianyuansudis

        issue["RelateElement"] = []

        for pe in ProjecteventElement.objects.filter(event_id=issueId):
            tmp = {}
            tmp['typetable'] = pe.typetable
            tmp['info'] = GetRelateTypeInfo(pe.typetable, pe.relatedid)
            issue["RelateElement"].append(tmp)
        # todo 关联元素展示 pgb
        # if each.relatetype == u"构件":
        #     pb = PrecastBeam.objects.get(id=each.relateid)
        #     issue["RelateElement"] = each.relatetype + ":" + pb.sign
        # elif each.relatetype == u"任务":
        #     task = ProjectTask.objects.get(id=each.relateid)
        #     issue["RelateElement"] = each.relatetype + ":" + task.name

        issue["dangqianjieduan"] = GetJianDuanFromStep(each)

        issue["priority"] = projectevent.get_priority_desc(each.priority)
        issue["deadline"] = str(each.deadline).split(' ')[0]
        response_data["StepOperation"] = []

        if FlowStepOperation.objects.filter(Q(flowstep=each.curflowstep)).count() > 0:
            StepOperation = FlowStepOperation.objects.filter(
                Q(flowstep=each.curflowstep))
            for step in StepOperation:
                tmpObj = {}
                tmpObj["id"] = step.id
                tmpObj["name"] = step.name
                response_data["StepOperation"].append(tmpObj)
        else:
            tmpObj = {}
            tmpObj["id"] = 0
            tmpObj["name"] = each.curflowstep.name
            response_data["StepOperation"].append(tmpObj)

        # 获取关联表单
        response_data["RelateFormList"] = []
        eventsteplist = Eventstep.objects.filter(projectevent=each)
        for eventstep in eventsteplist:
            if eventstep.relatedform:
                tmpObj = {}
                tmpObj["id"] = eventstep.relatedform.id
                tmpObj["name"] = eventstep.relatedform.name
                tmpObj["type"] = "biaodan"
                response_data["RelateFormList"].append(tmpObj)

        if each.curflowstep.relatedformtemplate:
            tmpObj = {}
            tmpObj["id"] = each.curflowstep.relatedformtemplate.id
            tmpObj["name"] = each.curflowstep.relatedformtemplate.name
            tmpObj["type"] = "muban"
            response_data["RelateFormList"].append(tmpObj)

        response_data["issue"] = issue
        response_data["issuc"] = "true"
        # print json.dumps(response_data)
    except:
        traceback.print_exc()
        response_data["issuc"] = "false"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def dealissue(request):
    issueId = int(request.GET.get('issueId', '0'))
    operId = int(request.GET.get('operId', '0'))
    feedback = request.GET.get('feedback', '')
    Chuli_RelateFileList = request.GET.get('Chuli_RelateFileList', '')
    bdid = request.GET.get('bdid', '')
    response_data = {}
    try:
        curprojectevent = projectevent.objects.get(id=issueId)

        if feedback == "":
            raise Exception(u"问题反馈不能为空！")

        # 判断是否有权限
        if not checkEventRight(request.user, curprojectevent.curflowstep.id):
            raise Exception(u"用户无权限！")

        # 保存表单
        curEventstep = getEventStep(curprojectevent)
        if bdid:
            curEventstep.relatedform_id = int(bdid)
            curEventstep.save()

        if not curprojectevent.issave:
            flag = True
            while flag:
                curFlowStepOperation = None
                if operId != 0:
                    curFlowStepOperation = FlowStepOperation.objects.get(
                        id=operId)

                curEventStepOperation = updateEventStepOper(
                    request.user, curprojectevent.curflowstep_id, curprojectevent,  curFlowStepOperation,  feedback)

                # 关联附件
                if len(Chuli_RelateFileList) > 0:
                    print Chuli_RelateFileList
                    dir = getTypeDirectory('quality',curprojectevent)
                    for FileId in Chuli_RelateFileList[:-1].split(","):
                        docId = int(FileId)
                        relatedDocWithEventOpr(request.user, docId, curEventStepOperation.id, curprojectevent.template.flowtype.name)
                        if dir:
                            doc = Document.objects.get(id=docId)
                            doc.docdirectory.add(dir)
                            movefiletoDir(doc,dir)

                response_data["issuc"] = "true"
                break
        else:
            curFlowStepOperation = None
            if operId != 0:
                curFlowStepOperation = FlowStepOperation.objects.get(id=operId)

            curprojectevent.issave = False
            curprojectevent.save()

            curEventStepOperation = updateEventStepOper(
                request.user, curprojectevent.curflowstep_id, curprojectevent,  curFlowStepOperation, curprojectevent.savecomment)

            Doc2Relate.objects.filter(relatetype='事件保存', relateid=curprojectevent.id).update(relatetype='事件步骤操作',relateid=curEventStepOperation.id)

            curprojectevent.saveuser = None
            curprojectevent.savecomment = None
            curprojectevent.save()

            response_data["issuc"] = "true"

        #结束归档文件
        if curprojectevent.curflowstep.isendstep:
            archiveEventDoc(curprojectevent)
            updateRelateType(curprojectevent)
            # print json.dumps(response_data)
    except Exception, e:
        traceback.print_exc()
        response_data["error"] ='%s' % e
        response_data["issuc"] = "false"

    return HttpResponse(json.dumps(response_data), content_type="application/json")

# Zhiliang


@login_required(login_url="/login/")
def issue_read(request, id):
    curprojectevent = projectevent.objects.get(id=id)
    jieduan = GetJianDuanFromStep(curprojectevent)
    priority = projectevent.get_priority_desc(curprojectevent.priority)
    curEventsteplist = Eventstep.objects.filter(
        Q(projectevent=curprojectevent)).values_list("id")
    issueoprlist = EventStepOperation.objects.filter(
        eventstep__in=curEventsteplist).order_by('oprtime')

    glyss = ProjecteventElement.objects.filter(event_id=id)
    guanlianyuansudis=""
    for glys in glyss:
        s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
        guanlianyuansudis +=s+","
    guanlianyuansudis=guanlianyuansudis[:-1]

    issueoprlistWithDoc = []
    for opr in issueoprlist:
        # 获取表单
        tmp = {}
        tmp['bds'] = []
        for eventstepid in curEventsteplist:
            eventstep = Eventstep.objects.get(id=int(eventstepid[0]))
            bd = {}
            if eventstep.relatedform:
                bd["bdid"] = eventstep.relatedform.id
                bd["bdname"] = eventstep.relatedform.name
            if bd:
                tmp['bds'].append(bd)

        tmp["issueopr"] = opr
        imglist = Doc2Relate.objects.filter(Q(relatetype=u"事件步骤操作") & Q(relateid=opr.id) & Q( document__filetype__contains="image"))
        tmp["issueoprimg"] = imglist
        doclist = Doc2Relate.objects.filter(Q(relatetype=u"事件步骤操作") & Q(relateid=opr.id)).exclude(document__filetype__contains="image")
        tmp["issueoprdoc"] = doclist
        issueoprlistWithDoc.append(tmp)
    return render_to_response('TaskAndFlow/flowtemplate/issue_read.html', RequestContext(request, locals()))



def issue_readfront(request, id):
    curprojectevent = projectevent.objects.get(id=id)
    jieduan = GetJianDuanFromStep(curprojectevent)
    priority = projectevent.get_priority_desc(curprojectevent.priority)
    curEventsteplist = Eventstep.objects.filter(
        Q(projectevent=curprojectevent)).values_list("id")
    issueoprlist = EventStepOperation.objects.filter(
        eventstep__in=curEventsteplist).order_by('oprtime')

    glyss = ProjecteventElement.objects.filter(event_id=id)
    guanlianyuansudis=""
    for glys in glyss:
        s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
        guanlianyuansudis +=s+","
    guanlianyuansudis=guanlianyuansudis[:-1]

    issueoprlistWithDoc = []
    for opr in issueoprlist:
        # 获取表单
        tmp = {}
        tmp['bds'] = []
        for eventstepid in curEventsteplist:
            eventstep = Eventstep.objects.get(id=int(eventstepid[0]))
            bd = {}
            if eventstep.relatedform:
                bd["bdid"] = eventstep.relatedform.id
                bd["bdname"] = eventstep.relatedform.name
            if bd:
                tmp['bds'].append(bd)

        tmp["issueopr"] = opr
        imglist = Doc2Relate.objects.filter(Q(relatetype=u"事件步骤操作") & Q(relateid=opr.id) & Q( document__filetype__contains="image"))
        tmp["issueoprimg"] = imglist
        doclist = Doc2Relate.objects.filter(Q(relatetype=u"事件步骤操作") & Q(relateid=opr.id)).exclude(document__filetype__contains="image")
        tmp["issueoprdoc"] = doclist
        issueoprlistWithDoc.append(tmp)
    return render_to_response('TaskAndFlow/flowtemplate/issue_read_front.html', RequestContext(request, locals()))

@csrf_exempt
@login_required(login_url="/login/")
def issue_update(request):
    if request.method=='GET':
        issueId = int(request.GET.get("issueId",None))
        curprojectevent = projectevent.objects.get(id=issueId)
        jieduan = GetJianDuanFromStep(curprojectevent)
        priority = projectevent.get_priority_desc(curprojectevent.priority)
        eventoprlist = EventStepOperation.objects.filter(Q(eventstep__projectevent=curprojectevent.id)).order_by("-oprtime")

        glyss = ProjecteventElement.objects.filter(event_id=issueId)
        guanlianyuansudis=""
        for glys in glyss:
            s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
            guanlianyuansudis +=s+","
        guanlianyuansudis=guanlianyuansudis[:-1]

        curopr = eventoprlist[0]

        eventstep = Eventstep.objects.get(id=curopr.eventstep_id)

        doclist = Doc2Relate.objects.filter(Q(relatetype=u"事件步骤操作") & Q(relateid=curopr.id))
        listcount=len(doclist)

        return render_to_response('TaskAndFlow/flowtemplate/issue_edit.html', RequestContext(request, locals()))
    elif request.method=='POST':
        operId = int(request.POST.get("operId",None))
        feedback = request.POST.get("feedback","")
        RelateFileList = eval(request.POST.get("RelateFileList",'[]'))

        response_data = {}
        response_data["issuc"] = "false"
        try:
            curEventStepOperation = EventStepOperation.objects.get(id=operId)
            curEventStepOperation.comment = feedback
            curEventStepOperation.save()

            curprojectevent = curEventStepOperation.eventstep.projectevent
            # 关联附件
            if len(RelateFileList) > 0:
                dir = getTypeDirectory('quality',curprojectevent)
                for FileId in RelateFileList:
                    docId = int(FileId)
                    relatedDocWithEventOpr(request.user, docId, curEventStepOperation.id, curprojectevent.template.flowtype.name)
                    if dir:
                        doc = Document.objects.get(id=docId)
                        doc.docdirectory.add(dir)
                        movefiletoDir(doc,dir)
            response_data["issuc"] = "true"
        except:
            traceback.print_exc()
            response_data["error"] = "更新问题异常！"
            response_data["issuc"] = "false"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        HttpResponseRedirect("/error_404")

@login_required(login_url="/login/")
def anquan_list(request):
    if checkMobile(request):

        templateName = 'TaskAndFlow/anquan_list_mobile.html'
    else:
        templateName = 'TaskAndFlow/anquan_list.html'
    return render_to_response(templateName, RequestContext(request, locals()))


@login_required(login_url="/login/")
def anquan_create(request):
    return render_to_response('TaskAndFlow/anquan_list.html', RequestContext(request, locals()))


@login_required(login_url="/login/")
def biaodan_shigongriji(request):
    return render_to_response('biaodan/shigongriji.html', RequestContext(request, locals()))


@csrf_exempt
@login_required(login_url="/login/")
def createissue(request):
    response_data = {}
    try:
        qnumber = request.POST.get('qnumber', '')
        qtitle = request.POST.get('qtitle', '')
        qdescribe = request.POST.get('qdescribe', '')
        category = request.POST.get('category', '')
        dealTemplateMajor = request.POST.get('dealTemplateMajor', '')  # 负责分包
        selectedGJs = eval(request.POST.get('selectedGJs', '[]'))  # 关联元素
        selectedKJ = request.POST.get('selectedKJ', '')  #关联空间
        RelateFileList = request.POST.get('RelateFileList', '')  # 附件列表
        dealTemplate = int(request.POST.get('dealTemplate', '0'))  # 流程
        issuePriority = int(request.POST.get('issuePriority', '0'))  # 优先级
        deadline = request.POST.get('deadline', '')  # 截止时间
        bdid = request.POST.get('bdid', None)
        elelist = eval(request.POST.get('relateQrcode', '[]'))

        while 1:
            if projectevent.objects.filter(number=qnumber):
                response_data["issuc"] = "false"
                response_data["error"] = "请不要重复创建！"
                break
            if not qdescribe:
                response_data["issuc"] = "false"
                response_data["error"] = "问题描述不能为空！"
                break
            if not deadline:
                response_data["issuc"] = "false"
                response_data["error"] = "问题截至时间不能为空！"
                break
            curFlowTemplate = FlowTemplate.objects.get(id=dealTemplate)
            curflowstep = FlowTemplateStep.objects.filter(
                Q(template=dealTemplate) & Q(isstartstep=True))[0]

            # 判断是否有权限
            if not checkEventRight(request.user, curflowstep.id):
                response_data["issuc"] = "false"
                response_data["error"] = "用户无权限！"
                break

            #扩展信息
            extenddict = {}
            extendinfo = ''
            if category:
                extenddict["category"] = category
            if extenddict:
                extendinfo = str(extenddict)

            curprojectevent = projectevent.objects.create(template=curFlowTemplate, number=qnumber, title=qtitle,
                                                          describe=qdescribe,deadline=deadline, priority=issuePriority,
                                                           curflowstep=curflowstep, createuser=request.user, extend=extendinfo)

            for ele in elelist:
                monele = Monitoringelement.objects.get(qrcode=ele)
                ProjecteventElement.objects.create(typetable=monele.typetable, relatedid=monele.relatedid, event=curprojectevent)

            # 保存关联元素
            for ys in selectedGJs:
                ProjecteventElement.objects.create(typetable=ys["typetable"], relatedid=ys["relatedid"],event=curprojectevent)

            # 关联空间
            if selectedKJ != 'model' and selectedKJ:
                kjty,kjid=TransRelateInfo("空间", selectedKJ) 
                newacc = ProjecteventElement.objects.create(typetable=kjty, relatedid=int(kjid),
                         event=curprojectevent)

            # 更新流程
            curEventStepOperation = updateEventStepOper(
                request.user, curprojectevent.curflowstep_id, curprojectevent, None, qdescribe)

            # 保存表单
            curEventstep = curEventStepOperation.eventstep
            if bdid:
                curEventstep.relatedform_id = int(bdid)
                curEventstep.save()

            # 关联附件
            if len(RelateFileList) > 0:
                print RelateFileList
                dir = getTypeDirectory('quality',curprojectevent)
                for FileId in RelateFileList[:-1].split(","):
                    print FileId
                    docId = int(FileId)
                    Doc2Relate.objects.create(relatetype='事件步骤操作', relateid=curEventStepOperation.id,
                                              creator=request.user, document_id=docId, createtime=datetime.datetime.now())
                    if dir:
                        doc = Document.objects.get(id=docId)
                        doc.docdirectory.add(dir)
                        movefiletoDir(doc,dir)

            # 发送通知
            #addNewEventMessage(curprojectevent, request.user)

            response_data["issuc"] = "true"
            break

    except:
        traceback.print_exc()

        response_data["error"] = "发起问题异常！"
        response_data["issuc"] = "false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def issuecreate_auto(request):
    response_data = {}
    try:
        issuetype = request.POST.get('issuetype', '')
        autotype = request.POST.get('autotype', '')
        autotypeId = request.POST.get('autotypeId', None)
        RelateFileList = request.POST.get('RelateFileList', '')  # 附件列表
        issuePriority = int(request.POST.get('issuePriority', '1'))  # 优先级

        qdescribe = ""
        MajorId = None
        selectedGJs = []
        selectedKJ = None
        if autotype == "weixianyuan":
            ha = Hazardevent.objects.get(id  = autotypeId)
            kha = KnowledgeHazardlist.objects.get(hazard_code=ha.hazard_code)
            qdescribe = u"危险源:"+kha.hazard_name + GetRelateTypeInfo(ha.relatedspace_type, ha.relatedspace_id) +u"不受控发起安全问题"
            MajorId = kha.major_id
            selectedGJs.append({"typetable":"危险源","relatedid":autotypeId});

        deadline = datetime.date.today() + datetime.timedelta(7)
        issuetype = transIssueType(issuetype)
        FlowTemplateList = getUserFlowTempList(request.user,issuetype,MajorId)
        if not FlowTemplateList:
            raise Exception('没有对应用户安全问题流程！')


        qnumber = getEventNumber(issuetype)

        curFlowTemplate = FlowTemplateList[0]
        curflowstep = FlowTemplateStep.objects.filter( Q(template=curFlowTemplate) & Q(isstartstep=True))[0]


        curprojectevent = projectevent.objects.create(template=curFlowTemplate, number=qnumber,
                                                      describe=qdescribe, deadline=deadline,
                                                      priority=issuePriority, curflowstep=curflowstep, createuser=request.user)

        # 保存关联元素
        for ys in selectedGJs:
            ProjecteventElement.objects.create(typetable=ys["typetable"], relatedid=ys["relatedid"],
                                             event=curprojectevent)

        # 关联空间
        if selectedKJ != 'model' and selectedKJ:
            kjys = selectedKJ.split('_')
            kjty = kjys[0]
            kjid = kjys[1]
            if kjty == 'unitprj':
                kjty = u'单位工程'
            elif kjty == 'floor':
                kjty = u'楼层'
            elif 'zone' in kjty:
                kjty = u'分区'
            ProjecteventElement.objects.create(typetable=kjty, relatedid=int(kjid), event=curprojectevent)

        # 更新流程
        curEventStepOperation = updateEventStepOper(
            request.user, curprojectevent.curflowstep_id, curprojectevent, None, qdescribe)

        # 保存表单
        # curEventstep = curEventStepOperation.eventstep
        # if bdid:
        #     curEventstep.relatedform_id = int(bdid)
        #     curEventstep.save()

        # 关联附件
        if len(RelateFileList) > 0:
            print RelateFileList
            dir = getTypeDirectory('quality',curprojectevent)
            for FileId in RelateFileList[:-1].split(","):
                print FileId
                docId = int(FileId)
                Doc2Relate.objects.create(relatetype='事件步骤操作', relateid=curEventStepOperation.id,
                                          creator=request.user, document_id=docId, createtime=datetime.datetime.now())
                if dir:
                    doc = Document.objects.get(id=docId)
                    doc.docdirectory.add(dir)
                    movefiletoDir(doc,dir)

        response_data["issuc"] = "true"

    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["issuc"] = "false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def create_projectevent(request):
    if request.method == "POST":
        form = projecteventForm(request.POST)
        response_data={}
        color_code="blue"
        try:
            if form.is_valid() and checkEventRight(request.user, form.cleaned_data["curflowstep"]):
                if projectevent.objects.filter(number=form.cleaned_data["number"]).count()>0:
                    raise Exception(u'问题编号重复')

                voiceList = request.POST.get("voiceid").split(",")
                newEvent = form.save()
                newEvent.createuser = request.user
                if request.POST.get("createtype") == "save":
                    newEvent.issave = True
                    newEvent.saveuser = request.user
                    newEvent.savecomment = form.cleaned_data["describe"]
                newEvent.save()

                # 关联元素
                print form.cleaned_data["relateNum"]
                elelist = []
                if form.cleaned_data["relateNum"]:
                    elelist = eval(form.cleaned_data["relateNum"])

                for ele in elelist:
                    if ele["typetable"]=="空间":
                        kjtype,kjid = TransRelateInfo(ele["typetable"],ele["relatedid"])
                        ProjecteventElement.objects.create(typetable=kjtype, relatedid=kjid, event=newEvent)
                    else:
                        ProjecteventElement.objects.create(typetable=ele["typetable"], relatedid=ele["relatedid"], event=newEvent)

                if not newEvent.issave:
                    newOpera = updateEventStepOper(
                        request.user, newEvent.curflowstep_id, newEvent, None, form.cleaned_data["describe"])

                    imgInfo = form.cleaned_data['photoUrl']
                    if ':' in imgInfo:
                        imgList = imgInfo.split(':')[1].split(';')

                        if uploadfile_weixin(imgList, form.cleaned_data['number'], 'quality', '事件步骤操作', request.user, newOpera.id,newEvent):
                            msg = "问题提交,图片上传失败！"
                            color_code = "red"

                    if not voiceList == ['']:
                        if fetchVoice_weixin(voiceList, form.cleaned_data['number'], 'quality', '事件步骤操作', request.user, newOpera.id,newEvent):
                            msg = "问题提交,语音上传失败！"
                            color_code = "red"

                    status = 'success'
                    msg = "创建成功！"
                    # # 发送通知
                    # try:
                    #     addNewEventMessage(newEvent, request.user)
                    # except:
                    #     traceback.print_exc()
                    #     msg = "创建成功，通知发送失败！"
                else:
                    imgInfo = form.cleaned_data['photoUrl']
                    if ':' in imgInfo:
                        imgList = imgInfo.split(':')[1].split(';')

                        if uploadfile_weixin(imgList, form.cleaned_data['number'], 'quality', '事件保存', request.user, newEvent.id,newEvent):
                            msg = "问题提交,图片上传失败！"
                            color_code = "red"

                    if not voiceList == ['']:
                        if fetchVoice_weixin(voiceList, form.cleaned_data['number'], 'quality', '事件保存', request.user, newEvent.id,newEvent):
                            msg = "问题提交,语音上传失败！"
                            color_code = "red"

                    status = 'success'
                    msg = "保存成功！"
            else:
                status = 'fail'
                msg = "事件信息不完整，创建失败！"
        except Exception, e:
            traceback.print_exc()
            msg = '%s' % e
            color_code = "red"
            status = 'fail'

            #traceback.print_exc()

        response_data["color_code"] = color_code
        response_data["msg"] = msg
        return  HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        title = getTitleFromUrl(request,request.get_full_path())
        havesheshi,havejixie,haverenwu = checkMonitorType()
        gojian = ""
        describe = ""
        relatedflowtemplate = 0
        if request.method == "GET":
            gojian = "" if request.GET.get("gojian") in ["", None] else request.GET.get("gojian")
            describe = "" if request.GET.get("describe") in ["", None] else request.GET.get("describe")
            relatedflowtemplate = 0 if request.GET.get("relatedflowtemplate") in ["", None] else int(request.GET.get("relatedflowtemplate"))

        userflowtemplist = getUserFlowTempList(request.user)
        majorList = getMajorList()
        if majorList:
            curMajorId = majorList[0].id

        eventType = u"质量问题"
        if relatedflowtemplate == 0:
             if len(userflowtemplist)>0:
                relatedflowtemplate=userflowtemplist[0].id
                eventType = userflowtemplist[0].flowtype.name
                curMajorId = userflowtemplist[0].major_id
        else:
            tmp = FlowTemplate.objects.get(id=relatedflowtemplate)
            eventType = tmp.flowtype.name
        form = projecteventForm(request.POST or None,
                                    initial={
                                        "number": getEventNumber(eventType),
                                        "relateNum": gojian,
                                        "describe": describe,
                                        #"template": relatedflowtemplate
                                    }
                                    )

        form.fields['template'].choices = [(r.id,r.name) for r in userflowtemplist]

        if checkMobile(request):
            config = {}
            ticket, appid, _ = fetch_ticket()

            sign = Sign(ticket, "http://" +
                        request.META["HTTP_HOST"] + request.path)

            config = sign.sign()
            config["appid"] = appid
            t = get_template(
                'TaskAndFlow/flowtemplate_mobile/create_projectevent_mobile.html')
        else:
            t = get_template('TaskAndFlow/create_projectevent.html')
        c = RequestContext(request, locals())
        return HttpResponse(t.render(c))


@login_required(login_url="/login/")
def progress_problem(request):
    isMobile = checkMobile(request)
    list_types = ["待处理问题","可编辑问题", "可浏览问题"]

    if isMobile:
        return render_to_response('TaskAndFlow/flowtemplate_mobile/progress_problem_mobile.html', RequestContext(request, locals()))
    # else:
    #     return render_to_response('TaskAndFlow/anquan_list.html', RequestContext(request, locals()))


@csrf_exempt
@login_required(login_url="/login/")
def progress_problem_load_table(request):
    try:
        response_data = {'status': 1}
        filterKey = int(request.POST.get("filterCode", 1))

        list_items = []
        list_items_head = []
        titles = []
        index = 0

        dataTableList = ['zhiliang', 'anquan']
        prjeventlist = projectevent.objects.filter(issave=False)
        for each in dataTableList:
            list_items.append([])
            list_items_head.append([])
            list_items_set = []

            flowtypename = "质量问题"
            # list_items_head[index]=('编号',"描述","等级","状态")
            list_items_head[index] = ('编号', "发起人", "当前步骤")
            sortKey = "等级"

            if each == 'zhiliang':
                flowtypename = "质量问题"
                titles.append("质量整改单")

            elif each == "anquan":
                flowtypename = "安全问题"
                titles.append("安全整改单")

            if filterKey == 1:
                list_items_all = prjeventlist.filter(
                    template__flowtype__name=flowtypename, curflowstep__isendstep=False).order_by("deadline")
                for each in list_items_all:
                    if checkEventNeedDeal(each, request.user):
                        list_items_set.append(each)

            elif filterKey == 2:
                list_items_all = prjeventlist.filter(
                    template__flowtype__name=flowtypename, curflowstep__isendstep=False).order_by("deadline")
                for each in list_items_all:
                    eventoprlist = EventStepOperation.objects.filter(Q(eventstep__projectevent=each.id)).order_by("-oprtime")
                    if eventoprlist and eventoprlist[0].actor==request.user:
                        list_items_set.append(each)
            elif filterKey == 3:
                list_items_all = prjeventlist.filter(
                    template__flowtype__name=flowtypename, curflowstep__isendstep=False).order_by("deadline")
                for each in list_items_all:
                    if not checkEventNeedDeal(each, request.user):
                        if checkEventNeedWatch(each, request.user):
                            list_items_set.append(each)
            else:
                list_items_set = prjeventlist.filter(
                    template__flowtype__name=flowtypename, curflowstep__isendstep=False).order_by("deadline")

            for each in list_items_set:
                tmpObj = {}
                tmpObj["id"] = each.id
                tmpObj["编号"] = each.number
                tmpObj["发起人"] = each.createuser.truename
                # tmpObj["等级"]=each.priority
                tmpObj["当前步骤"] = each.curflowstep.name
                list_items[index].append(tmpObj)

            #list_items[index] = sorted(list_items[index], key=lambda x : x[sortKey], reverse=True)
            index += 1

        response_data["titles"] = titles
        response_data["list_items"] = list_items
        response_data["list_items_head"] = list_items_head
    except:
        traceback.print_exc()
        response_data['status'] = 0
        response_data['error'] = "数据读取出错！"

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def progress_problem_trace(request, id):
    projectevent_instance = projectevent.objects.get(id=id)

    glyss = ProjecteventElement.objects.filter(event_id=id)
    guanlianyuansudis=""
    for glys in glyss:
        s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
        guanlianyuansudis +=s+","
    guanlianyuansudis=guanlianyuansudis[:-1]

    lastOpr = None
    if EventStepOperation.objects.filter(eventstep__projectevent=projectevent_instance):
        lastOpr = EventStepOperation.objects.filter(eventstep__projectevent=projectevent_instance).order_by('-oprtime')[0]

    operaList = []
    if FlowStepOperation.objects.filter(Q(flowstep=projectevent_instance.curflowstep)).count() > 0:
        StepOperation = FlowStepOperation.objects.filter(
            Q(flowstep=projectevent_instance.curflowstep))
        for step in StepOperation:
            tmpObj = {}
            tmpObj["id"] = step.id
            tmpObj["name"] = step.name
            operaList.append(tmpObj)
    else:
        tmpObj = {}
        tmpObj["id"] = 0
        tmpObj["name"] = projectevent_instance.curflowstep.name
        operaList.append(tmpObj)

    if checkEventRight(request.user, projectevent_instance.curflowstep.id):
        if projectevent_instance.curflowstep.isautotransfer:
            if FlowStepOperation.objects.filter(flowstep=projectevent_instance.curflowstep):
                enableStatus = projectevent_instance.curflowstep
                operaList = FlowStepOperation.objects.filter(
                    flowstep=projectevent_instance.curflowstep)
            else:
                if Eventstep.objects.filter(projectevent=projectevent_instance, flowstep=projectevent_instance.curflowstep, endtime=None):
                    enableStatus = projectevent_instance.curflowstep
                else:
                    enableStatus = {"name": "已结束"}
        else:
            if projectevent_instance.curflowstep.sequence < FlowTemplateStep.objects.filter(template=projectevent_instance.template).latest("sequence").sequence:
                enableStatus = FlowTemplateStep.objects.get(
                    template=projectevent_instance.template, sequence=projectevent_instance.curflowstep.sequence + 1)
            else:
                enableStatus = {"name": "已结束"}
    else:
        enableStatus = {"name": "无权限"}

    eventStepsRecord = Eventstep.objects.filter(
        projectevent=projectevent_instance).order_by("starttime").values()
    for each in eventStepsRecord:
        each["stepName"] = FlowTemplateStep.objects.get(
            id=each['flowstep_id']).name
        each["operationRecord"] = EventStepOperation.objects.filter(
            eventstep_id=each["id"]).values()
        for each in each["operationRecord"]:
            each["actorName"] = User.objects.get(id=each["actor_id"]).truename
            if each["flowstepoper_id"]:
                each["operaName"] = FlowStepOperation.objects.get(
                    id=each["flowstepoper_id"]).name

            doclist = Doc2Relate.objects.filter(relatetype=u"事件步骤操作", relateid=each["id"],  document__filetype__contains="image")
            if len(doclist)> 0:
                each["docList"] = doclist[0:3]

            voicelist = Doc2Relate.objects.filter(relatetype=u"事件步骤操作", relateid=each["id"],  document__filetype__contains="audio")
            if len(voicelist)>0:
                each["voiceList"] = voicelist

    if request.method == "POST":
        response_data = {"status": 1}
        if form.is_valid():
            form.save()
        else:
            response_data["status"] = 0
            response_data["msg"] = "序号信息有误！"

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        if checkMobile(request):
            config={}
            ticket, appid, _ = fetch_ticket()

            sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.path)

            config = sign.sign()
            config["appid"] = appid

            # print config
            t = get_template('TaskAndFlow/flowtemplate_mobile/progress_problem_trace.html')
        else:
            t = get_template(
                'TaskAndFlow/flowtemplate_mobile/progress_problem_trace.html')
        c = RequestContext(request, locals())
        return HttpResponse(t.render(c))

@csrf_exempt
@login_required(login_url="/login/")
def progress_problem_edit(request):
    if request.method == "POST":
        operId = int(request.POST.get("operId",None))
        comment = request.POST.get("comment","")
        imgList = request.POST.get("imgList", '').split(';')
        voiceList = request.POST.get("voiceId", '').split(';')

        response_data = {}
        response_data["status"] = 0
        try:
            newOpera = EventStepOperation.objects.get(id=operId)
            newOpera.comment = comment
            newOpera.save()

            curprojectevent = newOpera.eventstep.projectevent

            if len(imgList) > 0 and "" not in imgList:
                if uploadfile_weixin(imgList, curprojectevent.number, 'quality', '事件步骤操作', request.user, newOpera.id,curprojectevent):
                    raise Exception(u"问题修改,图片上传失败！")

            if not voiceList == ['']:
                if fetchVoice_weixin(voiceList,  curprojectevent.number, 'quality', '事件步骤操作', request.user, newOpera.id,curprojectevent):
                    raise Exception(u"问题修改,语音上传失败！")

            response_data["status"] = 1
            response_data["msg"] = "修改问题成功！"
        except Exception, e:
            msg = '%s' % e
            response_data["msg"] = msg
            response_data["status"] = 0
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        eventId = int(request.GET.get("eventId",None))
        projectevent_instance = projectevent.objects.get(id=eventId)

        lastOpr = None
        if EventStepOperation.objects.filter(eventstep__projectevent=projectevent_instance):
            lastOpr = EventStepOperation.objects.filter(eventstep__projectevent=projectevent_instance).order_by('-oprtime')[0]

            doclist = Doc2Relate.objects.filter(relatetype=u"事件步骤操作", relateid=lastOpr.id)

        if checkMobile(request):
            print "http://" + request.META["HTTP_HOST"] + request.get_full_path()
            config={}
            ticket, appid, _ = fetch_ticket()

            sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.get_full_path())

            config = sign.sign()
            config["appid"] = appid

            # print config
            t = get_template('TaskAndFlow/flowtemplate_mobile/progress_problem_edit.html')
        else:
            t = get_template('TaskAndFlow/flowtemplate_mobile/progress_problem_edit.html')
        c = RequestContext(request, locals())
        return HttpResponse(t.render(c))

@login_required(login_url="/login/")
def progress_problem_watch(request, id):
    projectevent_instance = projectevent.objects.get(id=id)

    glyss = ProjecteventElement.objects.filter(event_id=id)
    guanlianyuansudis=""
    for glys in glyss:
        s = GetRelateTypeInfo(glys.typetable, glys.relatedid)
        guanlianyuansudis +=s+","
    guanlianyuansudis=guanlianyuansudis[:-1]

    eventStepsRecord = Eventstep.objects.filter(
        projectevent=projectevent_instance).order_by("starttime").values()
    for each in eventStepsRecord:
        each["stepName"] = FlowTemplateStep.objects.get(
            id=each['flowstep_id']).name
        each["operationRecord"] = EventStepOperation.objects.filter(
            eventstep_id=each["id"]).values()
        for each in each["operationRecord"]:
            each["actorName"] = User.objects.get(id=each["actor_id"]).truename
            if each["flowstepoper_id"]:
                each["operaName"] = FlowStepOperation.objects.get(
                    id=each["flowstepoper_id"]).name

            doclist = Doc2Relate.objects.filter(relatetype=u"事件步骤操作", relateid=each["id"],  document__filetype__contains="image")
            if len(doclist) >0:
                each["docList"] = doclist[0:3]

            voicelist = Doc2Relate.objects.filter(relatetype=u"事件步骤操作", relateid=each["id"],  document__filetype__contains="audio")
            if len(voicelist)>0:
                each["voiceList"] = voicelist

    if checkMobile(request):
        t = get_template(
            'TaskAndFlow/flowtemplate_mobile/progress_problem_watch.html')
    else:
        t = get_template(
            'TaskAndFlow/flowtemplate_mobile/progress_problem_watch.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


@csrf_exempt
@login_required(login_url="/login/")
def progress_problem_update(request, id):
    result_string="处理失败"
    try:
        response_data = {'status': 1}
        comment = request.POST.get("comment", '')
        curEventId = int(request.POST.get("curEventId", 0))
        operId = request.POST.get("operId", "0")
        imgList = request.POST.get("imgList", '').split(';')
        voiceList = request.POST.get("voiceId", '').split(';')

        curprojectevent = projectevent.objects.get(id=curEventId)

        if operId != "save":
            operId = int(operId)
            operObj = None
            if operId != 0:
                operObj = FlowStepOperation.objects.get(id=operId)
            else:
                operObj = None

            newOpera = updateEventStepOper(
                request.user, curprojectevent.curflowstep_id, curprojectevent,  operObj,  comment)

            result_string = "处理成功！"
            if len(imgList) > 0 and "" not in imgList:
                if uploadfile_weixin(imgList, curprojectevent.number, 'quality', '事件步骤操作', request.user, newOpera.id,curprojectevent):
                    result_string = "状态提交,质检失败！"
                    response_data["status"] = 0

            if not voiceList == ['']:
                if fetchVoice_weixin(voiceList,  curprojectevent.number, 'quality', '事件步骤操作', request.user, newOpera.id,curprojectevent):
                    result_string = "问题提交,语音上传失败！"
                    response_data["status"] = 0
        else:
            curprojectevent.issave = True
            curprojectevent.saveuser = request.user
            curprojectevent.savecomment = comment
            curprojectevent.save()

            result_string = "保存成功！"
            if len(imgList) > 0 and "" not in imgList:
                if uploadfile_weixin(imgList, curprojectevent.number, 'quality', '事件保存', request.user, curprojectevent.id,curprojectevent):
                    result_string = "状态提交,质检失败！"
                    response_data["status"] = 0

            if not voiceList == ['']:
                if fetchVoice_weixin(voiceList,  curprojectevent.number, 'quality', '事件保存', request.user, curprojectevent.id,curprojectevent):
                    result_string = "问题提交,语音上传失败！"
                    response_data["status"] = 0

        #结束归档文件
        if curprojectevent.curflowstep.isendstep:
            archiveEventDoc(curprojectevent)
            updateRelateType(curprojectevent)
    except:
        traceback.print_exc()
        response_data["status"] = -1
        result_string = "数据上传出错！"

    response_data['msg'] = result_string
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
@login_required(login_url="/login/")
def typemanager(request):
    try:
        if request.method=='GET':
            mubanlist = BiaoDanMuBan.objects.all()
            majorlist = UserMajor.objects.all()
            return render_to_response('TaskAndFlow/flowtemplate/typemanager.html', RequestContext(request, locals()))
        elif request.method=='POST':
            response_data={"issuc":"true"}
            response_data['data']=[]
            opt = request.POST.get('opt',None)
            ptype = request.POST.get('type',None)
            if ptype=='guanjiandian':
                if opt=='cha':
                    response_data['data']=[{'id':each.id,'typename':each.acceptancetype.name,'formname':each.formtpl.name if each.formtpl else '空','major':each.acceptancetype.major.name} for each in AcceptancetypeFormtmp.objects.all()]
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                elif opt=='add':
                    typename = request.POST.get('typename',None)
                    major = request.POST.get('major',None)
                    newa = Acceptancetype.objects.create(name=typename,major_id=int(major))
                    bdmb = request.POST.get('bdmb',None)
                    if(bdmb=='null'):
                        AcceptancetypeFormtmp.objects.create(acceptancetype=newa)
                    else:
                        AcceptancetypeFormtmp.objects.create(acceptancetype=newa,formtpl_id=int(bdmb))
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                elif opt=='del':
                    idp = request.POST.get('id',None)
                    atft = AcceptancetypeFormtmp.objects.get(id=int(idp))
                    at = Acceptancetype.objects.get(id=atft.acceptancetype_id)
                    atft.delete()
                    at.delete()
                    return HttpResponse(json.dumps(response_data), content_type="application/json")


    except:
        traceback.print_exc()
