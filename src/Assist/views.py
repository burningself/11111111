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
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from TaskAndFlow.utility import *
from TaskAndFlow.utility_flowtemplate import *
from UserAndPrj.models import *
from TaskAndFlow.models import *
from Admin.models import *
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
import uuid
from Scc4PM.settings import CURRENT_PROJECT_ID
from Assist.utility import *
from UserPrjConfig.permissions import *


def viewpdf(request):
  # Create a URL of our project and go to the template route
    options = {
        'page-size': 'A4',
    }
    url  = request.GET.get('url','')
    projectUrl = request.get_host() + url
    pdf = pdfkit.from_url(projectUrl, False,options=options)
    # Generate download
    response = HttpResponse(pdf,content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="ourcodeworld.pdf"'

    return response


def shigongriji(request):
    return render_to_response('TaskAndFlow/taskmanager/shigongriji.html', RequestContext(request,locals()))


def baidumap(request):
    return render_to_response('common/baidumap.html', RequestContext(request,locals()))


@login_required(login_url="/login/")
@check_permission
def builddiary_create(request):
    majorList = UserMajor.objects.all()
    return render_to_response('TaskAndFlow/taskmanager/createbuilddiary.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
@check_permission
def builddiaryform(request):
    formbuilddiary = BiaoDanMuBan.objects.filter(formtype__name=u"施工日记")
    rijimb  = None
    if len(formbuilddiary)>0:
        rijimb = formbuilddiary[0]

    return render_to_response('TaskAndFlow/taskmanager/builddiarycreate.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
def builddiary_print(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        list_items = Constructiondiary.objects.all().order_by("-diary_date")

        timerange = request.GET.get("timerange",None)
        if timerange:
            startdate, enddate = GetDateRange(timerange)
            list_items = list_items.filter(Q(diary_date__gte=startdate)&Q(diary_date__lte=enddate))

        mergefile = MergeDiaryPdf(list_items)
        if mergefile:
            response_data["mergefile"] = "/upload/"+mergefile
            response_data["issuc"]="true"
    except Exception, e:
        print e
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
@login_required(login_url="/login/")
def builddiary_save(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        builddiary_name = request.POST.get('builddiary_name', None)
        builddiary_date = request.POST.get('builddiary_date', None)
        bdid =  request.POST.get('bdid', None)

        if builddiary_name and builddiary_date and bdid:
            builddiary_date=datetime.datetime.strptime(builddiary_date,'%Y-%m-%d')
            if  Constructiondiary.objects.filter(diary_date=builddiary_date).count()==0:
                bda = BiaoDan.objects.get(id=int(bdid))
                bdid = bda.id

                retCode,doc = Form2File(u"施工日记",bda.content,request.user,builddiary_name,builddiary_date)
                if retCode=="suc" and doc:
                    builddiary = Constructiondiary.objects.create(name =builddiary_name ,diary_date=builddiary_date,user=request.user,file=doc,related_form_id=bdid)
                    response_data["issuc"]="true"
                else:
                    response_data['error'] = u"归档失败"
            else:
                response_data['error'] = u"日记重复创建！"
        else:
            response_data['error'] = u"信息不完整"

    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
@login_required(login_url="/login/")
def builddiary_edit(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        diaryid = request.POST.get('diaryid', None)
        content = request.POST.get('content', None)

        diary = Constructiondiary.objects.get(id=int(diaryid))
        bda = BiaoDan.objects.get(id=diary.related_form_id)
        bda.content=content
        bda.save()

        retCode,doc = Form2File(u"施工日记",content,request.user,diary.name,diary.diary_date)
        if retCode=="suc" and doc:
            diary.file=doc
            diary.save()
            response_data["issuc"]="true"
        else:
            response_data['error'] = u"归档失败"

    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
@login_required(login_url="/login/")
def todolist(request):
    response_data = {}
    response_data["issuc"]="false"
    response_data["todolist"] = []
    try:
        print request.user.name
        start = float(request.POST.get('start', None))
        end = float(request.POST.get('end', None))

        time_local = time.localtime(start)
        starttime = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        time_local = time.localtime(end)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

        daycur=datetime.date.today()
        print starttime,endtime
        #公告
        noticelist = Notice.objects.filter(expire__gte=datetime.datetime.now())
        for each in noticelist:
            tmpObj = {}
            tmpObj['title']=u"公告:" + each.message
            tmpObj['start']= datetime.date.today().strftime("%Y-%m-%d")
            tmpObj['end']= each.expire.strftime("%Y-%m-%d")
            tmpObj['allDay']= 'true'
            tmpObj['color']=getToDoEeventColor("公告")
            tmpObj['type']="公告"
            tmpObj['contant']=each.message
            response_data["todolist"].append(tmpObj)
        #会议
        meetingids = MeetingUser.objects.filter(user=request.user).values_list('meeting', flat=True)
        meetinglist = Meeting.objects.filter(Q(begin_time__gte=starttime)&Q(end_time__lte=endtime)&(Q(hostuser=request.user)|Q(id__in=meetingids)))
        for each in meetinglist:
            tmpObj = {}
            tmpObj['title']= u"会议:"+each.name
            tmpObj['start']= each.begin_time.strftime("%Y-%m-%d %H:%M:%S")
            tmpObj['end']= each.end_time.strftime("%Y-%m-%d %H:%M:%S")
            tmpObj['color']=getToDoEeventColor("例会")
            tmpObj['type']="会议"
            tmpObj['id']=each.id
            tmpObj['contant']=each.description
            if not checkMobile(request):
                tmpObj['url']="/assist/huiyi/?nowshow=1&showid="+str(each.id)
            else:
                 tmpObj['url']="/assist/meetnotice/?status=0&meetid="+str(each.id)

            response_data["todolist"].append(tmpObj)

        searchtime = datetime.datetime.utcfromtimestamp(end)
        year = searchtime.strftime("%Y")
        month = searchtime.strftime("%m")
        date_list = []
        nextday = datetime.datetime.now()+datetime.timedelta(days = 1)#从第二天开始
        currtime = str(nextday.strftime("%Y-%m-%d"))
        currmonth_days = calendar.monthrange(int(year),int(month))[1]
        begin_date = datetime.datetime.strptime(currtime, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(year+'-'+month+'-'+str(currmonth_days), "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        week_day_dict = {
            0 : u'星期一',
            1 : u'星期二',
            2 : u'星期三',
            3 : u'星期四',
            4 : u'星期五',
            5 : u'星期六',
            6 : u'星期天',
        }
        # print date_list
        zhouqimeetingids = MeetingZhouqiUser.objects.filter(user_id=request.user.id).values_list('meeting', flat=True)
        zhouqilist = MeetingZhouqi.objects.filter(Q(hostuser=request.user)|Q(id__in=zhouqimeetingids))
        if len(zhouqilist)>0:
            for meetingmodel in zhouqilist:
                for predate in date_list:
                    time_pre = year+'-'+predate
            
                    if datetime.datetime.strptime(time_pre+" 00:00:00","%Y-%m-%d %H:%M:%S")>datetime.datetime.strptime(endtime,"%Y-%m-%d %H:%M:%S"):
                        break
                 
                    weekday = week_day_dict[datetime.datetime.strptime(time_pre,"%Y-%m-%d").weekday()]
                    createtimearr = meetingmodel.create_time.split(',')
                    currdaynum = time_pre[-2:]
                    needadd = False
                    if meetingmodel.zhouqitype==1:#日会议
                        needadd = True
                    elif meetingmodel.zhouqitype==2:#周会议
                        if weekday in meetingmodel.create_time:
                            needadd = True
                    elif meetingmodel.zhouqitype==3:#月会议
                        if currdaynum in createtimearr:
                            needadd = True
                    if needadd:
                        tempobj = {}
                        tempobj['title'] = meetingmodel.name
                        tempobj['start'] = time_pre+' '+meetingmodel.begin_time+':00'
                        tempobj['end'] = time_pre+' '+meetingmodel.end_time+':00'
                        tempobj['canupdate'] = 0
                        tempobj['color']=getToDoEeventColor("例会")
                        tempobj['type']="会议"
                        tempobj['contant'] = meetingmodel.description
                        if not checkMobile(request):
                            tempobj['url']="/assist/huiyi/?nowshow=1&huiyitype=1&showid="+str(meetingmodel.id)+"&time_pre="+time_pre

                        response_data["todolist"].append(tempobj)

        starttime=datetime.datetime.strptime(starttime,'%Y-%m-%d %H:%M:%S')
        endtime=datetime.datetime.strptime(endtime,'%Y-%m-%d %H:%M:%S')
        #工序验收
        userstatuslist = User2PBStatus.objects.filter(user=request.user).values_list('status_id', flat=True)
        acceptancelist = Acceptance.objects.filter(deadline__gte=starttime,deadline__lte=endtime,is_finished=False).order_by("status_id")
        mapacccount = {}
        MAX_ACC_COUNT = 3
        order = 0
        for each in acceptancelist:
            if each.status_id not in userstatuslist:
                continue

            if mapacccount.has_key(each.status_id) and mapacccount[each.status_id]>MAX_ACC_COUNT:
                continue
            else:
                if mapacccount.has_key(each.status_id):
                    mapacccount[each.status_id]+=1
                else:
                    mapacccount[each.status_id]=1
                tmpObj = {}
               
                if each.monitoring.typetable == u"构件":
                    pbObj = PrecastBeam.objects.get(id=each.monitoring.relatedid)
                    tmpObj['title']= each.status.pbtype.name+":"+pbObj.drawnumber+each.name
                else:
                    tmpObj['title']= each.status.pbtype.name+":"+each.monitoring.qrcode+each.name
                if daycur<each.deadline.date():
                    tmpObj['start']= each.deadline.strftime("%Y-%m-%d")
                    tmpObj['end']= each.deadline.strftime("%Y-%m-%d")
                else:
                    tmpObj['start']= daycur.strftime("%Y-%m-%d")
                    tmpObj['end']= daycur.strftime("%Y-%m-%d")
                tmpObj['color']=getToDoEeventColor("提醒")
                tmpObj['type']="提醒"
                tmpObj['allDay']= 'true'
                order+=1
                tmpObj['order']= order
                if not checkMobile(request):
                    tmpObj['url']="/task/projecttask/lurujindu/?gxid="+str(each.id)

                if mapacccount[each.status_id]>MAX_ACC_COUNT:
                    if not checkMobile(request):
                        tmpObj['url'] = "/task/gongxuyanshou/"
                    tmpObj['title'] = "点击获取更多："+each.status.pbtype.name+each.name+"工序验收"
                    tmpObj['color']=getToDoEeventColor("分组")
                response_data["todolist"].append(tmpObj)

         #质量关键点
        index = 0
        order = 100
        MAX_YANSHOU_COUNT=5
        if request.user.has_perm("编辑质量验收"):
            acceptanceinfolist = Acceptanceinfo.objects.exclude(status=3)
            for each in acceptanceinfolist:
                if index>MAX_YANSHOU_COUNT:
                    break

                tmpObj = {}
                tmpObj['title']= u"质量验收:"+each.acceptancetype.name
                if daycur<each.finiishedtime.date():
                    tmpObj['start']= each.finiishedtime.strftime("%Y-%m-%d %H:%M:%S")
                    tmpObj['end']= each.finiishedtime.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    tmpObj['start']= daycur.strftime("%Y-%m-%d")
                    tmpObj['end']= daycur.strftime("%Y-%m-%d")
                tmpObj['color']=getToDoEeventColor("提醒")
                tmpObj['type']="提醒"
                tmpObj['contant']=each.comment
                tmpObj['allDay']= 'true'
                index+=1
                tmpObj['order']= order+index
                if not checkMobile(request):
                    tmpObj['url']="/task/zhiliangyanshou/yanshou/"+str(each.id)+"/"
                    if index>MAX_YANSHOU_COUNT:
                        tmpObj['url'] = "/task/zhiliangyanshou/"
                        tmpObj['title'] = "点击查看更多质量验收"
                        tmpObj['color']=getToDoEeventColor("分组")
                else:
                    tmpObj['url']="/task/zhiliangyanshou/yanshou/"+str(each.id)+"/"
                response_data["todolist"].append(tmpObj)

        #安全检查
        if request.user.has_perm("编辑安全检查"):
            jianchalist = Pbtypetimedcheck.objects.filter(status_reset_time__gte=starttime,status_reset_time__lte=endtime,isneedcheck=True)
            for each in jianchalist:
                tmpObj = {}
                tmpObj['title']= u"安全检查:"+each.pbtype.name+u"-"+each.name
                if daycur<each.status_reset_time.date():
                    tmpObj['start']= each.status_reset_time.strftime("%Y-%m-%d %H:%M:%S")
                    tmpObj['end']= each.status_reset_time.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    tmpObj['start']= daycur.strftime("%Y-%m-%d")
                    tmpObj['end']= daycur.strftime("%Y-%m-%d")
                tmpObj['color']=getToDoEeventColor("提醒")
                tmpObj['type']="提醒"
                tmpObj['contant']=each.pbtype.name+u":"+each.name
                tmpObj['allDay']= 'true'
                tmpObj['url']="/task/anquan/jianchajiancha/?jianchaId="+str(each.id)

                response_data["todolist"].append(tmpObj)

        #质量整改单 message
        index = 0
        order = 200
        list_items = projectevent.objects.filter(template__flowtype__name="质量问题",curflowstep__isendstep=False)
        for each in list_items:
            if index>MAX_ACC_COUNT:
                break

            if each.issave and request.user != each.saveuser:
                continue

            # 当前用户没有权限
            if not checkEventNeedWatch(each,request.user):
                continue

            tmpObj = {}
            tmpObj['title']= u"质量问题:"+each.number
            if daycur<each.deadline.date():
                tmpObj['start']= each.updatetime.strftime("%Y-%m-%d")
                tmpObj['end']= each.deadline.strftime("%Y-%m-%d")
            else:
                tmpObj['start']= daycur.strftime("%Y-%m-%d")
                tmpObj['end']= daycur.strftime("%Y-%m-%d")
            tmpObj['color']=getToDoEeventColor("整改单")
            tmpObj['type']="整改单"
            tmpObj['id']=each.id
            tmpObj['contant']=each.describe
            tmpObj['allDay']= 'true'
            index+=1
            tmpObj['order']= order+index
            tmpObj['needdeal'] = checkEventRight(request.user,each.curflowstep.id)
            if checkMobile(request):
                tmpObj['url']="/task/progress/problem/"+str(each.id)
                if  not tmpObj['needdeal']:
                    tmpObj['url']="/task/progress/problem/watch/"+str(each.id)
                if index>MAX_ACC_COUNT:
                    tmpObj['url'] = "/task/progress/problem/"
                    tmpObj['title'] = "点击查看更多整改单"
                    tmpObj['color']=getToDoEeventColor("分组")
            else:
                tmpObj['url']="/task/issue/issuedeal/"+str(each.id)
                if  not tmpObj['needdeal'] :
                    tmpObj['url']="/task/issue/read/"+str(each.id)
                if index>MAX_ACC_COUNT:
                    tmpObj['url'] = "/task/issue/list/?issuetype=zhiliang"
                    tmpObj['title'] = "点击查看更多质量问题"
                    tmpObj['color']=getToDoEeventColor("分组")
            response_data["todolist"].append(tmpObj)

        #安全整改单 message
        index = 0
        order = 300
        list_items = projectevent.objects.filter(template__flowtype__name="安全问题",curflowstep__isendstep=False)
        for each in list_items:
            if index>MAX_ACC_COUNT:
                break

            if each.issave and request.user != each.saveuser:
                continue

            # 当前用户没有权限
            if not checkEventNeedWatch(each,request.user):
                continue

            tmpObj = {}
            tmpObj['title']= u"安全问题:"+each.number
            if daycur<each.deadline.date():
                tmpObj['start']= each.updatetime.strftime("%Y-%m-%d")
                tmpObj['end']= each.deadline.strftime("%Y-%m-%d")
            else:
                tmpObj['start']= daycur.strftime("%Y-%m-%d")
                tmpObj['end']= daycur.strftime("%Y-%m-%d")
            tmpObj['color']=getToDoEeventColor("整改单")
            tmpObj['type']="整改单"
            tmpObj['id']=each.id
            tmpObj['contant']=each.describe
            tmpObj['allDay']= 'true'
            tmpObj['className'] = "testtest"
            index+=1
            tmpObj['order']= order+index
            tmpObj['needdeal'] = checkEventRight(request.user,each.curflowstep.id)
            if checkMobile(request):
                tmpObj['url']="/task/progress/problem/"+str(each.id)
                if  not tmpObj['needdeal']:
                    tmpObj['url']="/task/progress/problem/watch/"+str(each.id)
                if index>MAX_ACC_COUNT:
                    tmpObj['url'] = "/task/progress/problem/"
                    tmpObj['title'] = "点击查看更多整改单"
                    tmpObj['color']=getToDoEeventColor("分组")
            else:
                tmpObj['url']="/task/issue/issuedeal/"+str(each.id)
                if  not tmpObj['needdeal'] :
                    tmpObj['url']="/task/issue/read/"+str(each.id)
                if index>MAX_ACC_COUNT:
                    tmpObj['url'] = "/task/issue/list/?issuetype=anquan"
                    tmpObj['title'] = "点击查看更多安全问题"
                    tmpObj['color']=getToDoEeventColor("分组")
            response_data["todolist"].append(tmpObj)


        if request.user.has_perm("编辑月度计划"):
            #月度计划提醒 pgb(todo 先写死每月25号，后续看配置)
            datemonth=datetime.datetime.strptime(daycur.strftime("%Y-%m-25"),'%Y-%m-%d')
            tmpObj = {}
            tmpObj['title']= u"月度计划提交"
            tmpObj['start']= datemonth.strftime("%Y-%m-%d")
            tmpObj['end']= datemonth.strftime("%Y-%m-%d")
            tmpObj['color']=getToDoEeventColor("提醒")
            tmpObj['type']="提醒"
            tmpObj['contant']=u"月度计划提交提醒"
            tmpObj['allDay']= 'true'
            if not checkMobile(request):
                tmpObj['url']="/task/projecttask/monthplan/"
            response_data["todolist"].append(tmpObj)

            #周报提醒 pgb(todo 先写死每周2，后续看配置)
        if request.user.has_perm("编辑工程周报"):
            for i in range((endtime - starttime).days+1):
                day = starttime + datetime.timedelta(days=i)
                if 1==day.weekday():
                    tmpObj = {}
                    tmpObj['title']= u"周报提交"
                    tmpObj['start']= day.strftime("%Y-%m-%d")
                    tmpObj['end']= day.strftime("%Y-%m-%d")
                    tmpObj['color']=getToDoEeventColor("提醒")
                    tmpObj['type']="提醒"
                    tmpObj['contant']=u"周报提交提醒"
                    tmpObj['allDay']= 'true'
                    if not checkMobile(request):
                        tmpObj['url']="/task/projecttask/buildweekly/"
                    response_data["todolist"].append(tmpObj)

        response_data["issuc"]="true"
    except:
        traceback.print_exc()
        response_data['error'] = '获取数据异常'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def shortcut_getcategorylist(request):
    response_data = {}
    response_data["issuc"]="false"
    response_data["categorylist"]=[]
    try:
        categorylist = AdminFunctionCategory.objects.filter(isrecord=True)
        for each in categorylist:
            print each
            tmpObj = {}
            tmpObj['categoryname']=each.name
            tmpObj['icon']=each.icon
            tmpObj['color']=each.color
            response_data["categorylist"].append(tmpObj)

        response_data["issuc"]="true"
    except Exception, e:
        print e
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def shortcut_getcategoryfunction(request):
    response_data = {}
    response_data["issuc"]="false"
    response_data["functionlist"]=[]
    try:
        category = request.GET.get('categoryname', None)

        if category:
            functionlist = AdminFunction.objects.filter(category__name=category,isrecord=True)
        else:
            functionlist = AdminFunction.objects.filter(isrecord=True).order_by("category_id")

        shortcutlist = Usershortcut.objects.filter(user=request.user).values_list('function_id', flat=True)
        for each in functionlist:
            tmpObj = {}
            tmpObj['name']=each.name
            tmpObj['icon']=each.icon
            tmpObj['categoryname']=each.category.name
            tmpObj['color']=each.category.color
            tmpObj['url']=each.url
            tmpObj['param']=each.param
            tmpObj['isselect']="true" if each.id in shortcutlist else "false"

            response_data["functionlist"].append(tmpObj)

        response_data["issuc"]="true"

    except Exception, e:
        print e
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url="/login/")
def shortcut_getusershortcutlist(request):
    response_data = {}
    response_data["issuc"]="false"
    response_data["shortcutlist"]=[]
    try:

        shortcutlist = Usershortcut.objects.filter(user=request.user,function__isrecord=True)

        for each in shortcutlist:
            tmpObj = {}
            tmpObj['name']=each.function.name
            tmpObj['icon']=each.function.icon
            tmpObj['categoryname']=each.function.category.name
            tmpObj['categoryid']=each.function.category.id
            tmpObj['color']=each.function.category.color
            tmpObj['url']=each.function.url
            tmpObj['param']=each.function.param
            tmpObj['seq']=each.seq

            response_data["shortcutlist"].append(tmpObj)

        response_data["shortcutlist"] = sorted(response_data["shortcutlist"], key=lambda x : x['categoryid'])

        response_data["issuc"]="true"

    except Exception, e:
        print e
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/")
def shortcut_setusershortcut(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        functionname = request.GET.get('functionname', None)
        ischeck = request.GET.get('ischeck', None)
        if functionname:
            fun = AdminFunction.objects.get(name=functionname)
            if ischeck and int(ischeck):
                if not Usershortcut.objects.filter(user=request.user,function=fun):
                    Usershortcut.objects.create(user=request.user,function=fun)
            else:
                Usershortcut.objects.filter(user=request.user,function=fun).delete()

            response_data["issuc"]="true"
        else:
            response_data['error']='缺少参数'

    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def shortcut_saveshortcutseq(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        shortcutlist =eval(request.GET.get('shortcutlist', '[]'))
        for each in shortcutlist:
            shortcut=Usershortcut.objects.get(user=request.user,function__name=each.function)
            shortcut.seq= each.seq
            shortcut.save()

        response_data["issuc"]="true"


    except Exception, e:
        print e
        response_data['error'] = '%s' % e
    return HttpResponse(json.dumps(response_data), content_type="application/json")
