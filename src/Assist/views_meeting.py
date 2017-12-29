# -*- coding: utf-8 -*-
'''

@author: pgb
'''
import traceback,datetime,array,calendar
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
from Assist.models import *
from Assist.commonUtil import *
from Assist.utility import *
from TaskAndFlow.utility_filemanager import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
from Scc4PM.settings import CURRENT_PROJECT_ID
from UserPrjConfig.permissions import *
import uuid


@login_required(login_url="/login/")
@check_permission
def huiyi(request):
    meetingtype_list = Meetingtype.objects.all()

    templateName = 'MeetingManager/huiyi.html'
    return render_to_response(templateName, RequestContext(request, locals()))

@login_required(login_url="/login/")
@check_permission_ajax
def createhuiyi(request):
    response_data = {}
    meetname = request.GET.get('meetname')
    documents = eval(request.GET.get('documents','[]'))
    meetingtype = request.GET.get('meetingtype')
    meetroom = request.GET.get('meetroom')
    hyzt = request.GET.get('hyzt')
    meetingusers = eval(request.GET.get('meetingusers','[]'))
    hysrq = request.GET.get('hysrq')
    hyerq = request.GET.get('hyerq')
    response_data['issuc'] = 'true'
    try:
        mettingmodel = Meeting.objects.create(hostuser_id=request.user.id,name=meetname,description=hyzt,meetingtype_id=meetingtype,begin_time=datetime.datetime.strptime(hysrq,'%Y-%m-%d %H:%M:%S'),end_time=datetime.datetime.strptime(hyerq,'%Y-%m-%d %H:%M:%S'),roomname=meetroom)

        queryList = []
        for mid in meetingusers:
            queryList.append(MeetingUser(user_id=mid,meeting_id=mettingmodel.id))
        MeetingUser.objects.bulk_create(queryList)

        if documents:
            doclist=[]
            destdir=getTypeDirectory('meeting',mettingmodel)
            for docid in documents:
                if Document.objects.filter(id=docid).count()==1:
                    tar = Document.objects.get(id=docid)
                    if destdir:
                        tar.docdirectory.add(destdir)
                        movefiletoDir(tar,destdir)
                else:
                    raise Exception(u'文件不存在！')
                doclist.append(Meetingrelatedfile(meeting_id=mettingmodel.id,file_id=docid))
            Meetingrelatedfile.objects.bulk_create(doclist)

        AddNewMeetingMsg(mettingmodel, "会议")
    except Exception as e:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data,encoding="UTF-8"), content_type="application/json")

@login_required(login_url="/login/")
@check_permission_ajax
def createzhouqihuiyi(request):
    response_data = {}
    meetname = request.GET.get('meetname')
    zhouqitype = request.GET.get('zhouqitype')
    createtime = request.GET.get('createtime','')
    documents = request.GET.get('documents','')
    issuePriority = request.GET.get('issuePriority')
    meetroom = request.GET.get('meetroom')
    hyzt = request.GET.get('hyzt')
    selectedValues = request.GET.get('selectedValues')
    hysrq = request.GET.get('hysrq')
    hyerq = request.GET.get('hyerq')
    response_data['issuc'] = 'true'
    try:
        mettingmodel = MeetingZhouqi.objects.create(create_time=createtime,zhouqitype=zhouqitype,hostuser_id=request.user.id,name=meetname,description=hyzt,meetingtype_id=issuePriority,begin_time=hysrq,end_time=hyerq,roomname=meetroom)
        print mettingmodel.id
        meetingusers = selectedValues.split("#")
        queryList = []
        for mid in meetingusers:
            queryList.append(MeetingZhouqiUser(user_id=mid,meeting_id=mettingmodel.id))
        MeetingZhouqiUser.objects.bulk_create(queryList)
        if docs!='':
            destdir=getTypeDirectory('meeting',mettingmodel)
            doclist = []
            docsarr = docs.split("#")
            for docid in docsarr:
                doclist.append(MeetingZhouqirelatedfile(meeting_id=mettingmodel.id,file_id=docid))
            MeetingZhouqirelatedfile.objects.bulk_create(doclist)
    except Exception as e:
        print e
    return HttpResponse(json.dumps(response_data,encoding="UTF-8"), content_type="application/json")

@login_required(login_url="/login/")
@check_permission_ajax
def editzhouqihuiyi(request):
    response_data = {}
    meetid = request.GET.get('meetid')
    meetname = request.GET.get('meetname')
    zhouqitype = request.GET.get('zhouqitype')
    createtime = request.GET.get('createtime','')
    docs = request.GET.get('documents','')
    issuePriority = request.GET.get('issuePriority')
    meetroom = request.GET.get('meetroom')
    hyzt = request.GET.get('hyzt')
    selectedValues = request.GET.get('selectedValues')
    hysrq = request.GET.get('hysrq')
    hyerq = request.GET.get('hyerq')
    response_data['issuc'] = 'true'
    try:
        mettingmodel = MeetingZhouqi.objects.get(id=meetid)
        # print mettingmodel.name
        #MeetingZhouqi.objects.create(create_time=createtime,zhouqitype=zhouqitype,hostuser_id=request.user.id,name=meetname,description=hyzt,meetingtype_id=issuePriority,begin_time=hysrq,end_time=hyerq,roomname=meetroom)
        mettingmodel.create_time = createtime
        mettingmodel.zhouqitype=zhouqitype
        mettingmodel.hostuser_id=request.user.id
        mettingmodel.name=meetname
        mettingmodel.description=hyzt
        mettingmodel.meetingtype_id=issuePriority
        mettingmodel.begin_time=hysrq
        mettingmodel.end_time=hyerq
        mettingmodel.roomname=meetroom
        mettingmodel.save()
        meetingusers = selectedValues.split("#")
        MeetingZhouqiUser.objects.filter(meeting_id=meetid).delete()
        queryList = []
        for mid in meetingusers:
            queryList.append(MeetingZhouqiUser(user_id=mid,meeting_id=mettingmodel.id))
        MeetingZhouqiUser.objects.bulk_create(queryList)

        if docs!='':
            doclist = []
            docsarr = docs.split("#")
            for docid in docsarr:
                doclist.append(MeetingZhouqirelatedfile(meeting_id=mettingmodel.id,file_id=docid))
            MeetingZhouqirelatedfile.objects.bulk_create(doclist)
    except Exception as e:
        print e
    return HttpResponse(json.dumps(response_data,encoding="UTF-8"), content_type="application/json")

@login_required(login_url="/login/")
@check_permission_ajax
def edithuiyi(request):
    response_data = {}
    meetname = request.GET.get('meetname')
    issuePriority = request.GET.get('issuePriority')
    meetroom = request.GET.get('meetroom')
    hyzt = request.GET.get('hyzt')
    selectedValues = request.GET.get('selectedValues')
    hysrq = request.GET.get('hysrq')
    hyerq = request.GET.get('hyerq')
    docs = request.GET.get('documents','')
    meetid = request.GET.get('meetid')
    removedocs = request.GET.get('removedocuments','')

    response_data['issuc'] = 'true'
    pushmsg = ''
    try:
        meetmodel = Meeting.objects.get(id=meetid)
        meetmodel.name = meetname
        meetmodel.meetingtype_id = issuePriority
        meetmodel.description = hyzt
        if meetroom!=meetmodel.roomname:
            meetmodel.roomname = meetroom
            pushmsg = ("%s将会议%s(%s)的地点改成：%s") % (request.user.truename,meetmodel.name,meetmodel.description,meetroom)

        if datetime.datetime.strptime(hysrq,'%Y-%m-%d %H:%M:%S')!=meetmodel.begin_time:
            meetmodel.begin_time = datetime.datetime.strptime(hysrq,'%Y-%m-%d %H:%M:%S')
            if pushmsg=='':
                pushmsg = ("%s将会议%s(%s)的时间改成：%s") % (request.user.truename,meetmodel.name,meetmodel.description,hysrq)
            else:
                pushmsg = pushmsg+',时间改成：'+hysrq
        meetmodel.end_time = datetime.datetime.strptime(hyerq,'%Y-%m-%d %H:%M:%S')
        meetmodel.save()
        oldusers = map(str,MeetingUser.objects.filter(meeting_id=meetid).values_list('user_id',flat=True))
        print '================================================='
        # oldusers = map(eval,oldusers)
        # print oldusers
        meetingusers = map(str,selectedValues.split("#"))
        # print meetingusers
        # print set(oldusers) & set(meetingusers)
        jiaoji_users = set(oldusers) & set(meetingusers)
        add_users = set(meetingusers) - jiaoji_users
        reduce_users = set(oldusers) - jiaoji_users

        MeetingUser.objects.filter(meeting_id=meetmodel.id,user_id__in=reduce_users).delete()
        queryList = []
        pushmsgList = []
        for mid in jiaoji_users:
            if pushmsg!='':
                pushmsgList.append(PushMessage(status=0, relatetype="会议修改", relateid=meetmodel.id,
                                    agentid= Project.objects.get(id=CURRENT_PROJECT_ID).appid,
                                    fromuser_id=request.user.id, touser_id=mid, message=pushmsg))
        PushMessage.objects.bulk_create(pushmsgList)

        queryList = []
        pushmsgList = []
        for mid in add_users:
            queryList.append(MeetingUser(user_id=mid,meeting_id=meetmodel.id))
            pushmsgList.append(PushMessage(status=0, relatetype="会议", relateid=meetmodel.id,
                                    agentid= Project.objects.get(id=CURRENT_PROJECT_ID).appid,
                                    fromuser_id=request.user.id, touser_id=mid, message=meetmodel.name))
        MeetingUser.objects.bulk_create(queryList)
        PushMessage.objects.bulk_create(pushmsgList)

        if docs!='':
            destdir = getTypeDirectory('meeting',meetmodel)
            doclist = []
            docsarr = docs.split("#")
            for docid in docsarr:
                if Document.objects.filter(id=docid).count()==1:
                    tar = Document.objects.get(id=docid)
                    tar.docdirectory.add(destdir)
                    movefiletoDir(tar,destdir)
                else:
                    raise Exception(u'文件不存在！')
                doclist.append(Meetingrelatedfile(meeting_id=meetid,file_id=docid))
            Meetingrelatedfile.objects.bulk_create(doclist)

        if removedocs!='':
            deldocs = removedocs.split("#")
            Meetingrelatedfile.objects.filter(meeting_id=meetid,file_id__in=deldocs).delete()


    except Exception as e:
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data,encoding="UTF-8"), content_type="application/json")

@login_required(login_url="/login/")
@check_permission_ajax
def deleteMeeting(request):
    response_data = {}
    try:
        meetid = request.GET.get('meetid')
        response_data['issuc'] = True
        meetmodel =  Meeting.objects.get(id=meetid)
        destdir = getTypeDirectory('meeting',meetmodel)
        if destdir:
            destdir.delete()
        Meeting.objects.filter(id=meetid).delete()

    except Exception as e:
        response_data['issuc']=False
        traceback.print_exc()
    return HttpResponse(json.dumps(response_data,encoding="UTF-8"), content_type="application/json")

@login_required(login_url="/login/")
def loadMeetingDatas(request):
    response_data = {}
    response_data['issuc'] = 'true'
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')

    startdate=datetime.datetime.strptime(startdate+" 00:00:00",'%Y-%m-%d %H:%M:%S')
    enddate=datetime.datetime.strptime(enddate+" 23:59:59",'%Y-%m-%d %H:%M:%S')

    meetings = Meeting.objects.filter(begin_time__range=(startdate,enddate))
    meetinglist = []
    for meetingmodel in meetings:
        tempobj = {}
        tempobj['mid'] = meetingmodel.id
        tempobj['meetingtype'] = meetingmodel.meetingtype_id
        tempobj['meetingtypename'] = meetingmodel.meetingtype.name if meetingmodel.meetingtype else ""
        tempobj['roomname'] = meetingmodel.roomname
        tempobj['title'] = meetingmodel.name
        tempobj['start'] = meetingmodel.begin_time
        tempobj['end'] = meetingmodel.end_time
        tempobj['huiyitype'] = 0
        tempobj['canupdate'] = 1
        tempobj['contant'] = meetingmodel.description
        meetinglist.append(tempobj)

    #周期会议
    curdate = datetime.date.today()
    if startdate.date()>curdate:
        if curdate.month== startdate.month:
            begin_date = curdate +datetime.timedelta(days = 2)#从第二天开始
        else:
            begin_date = startdate.date()
        if begin_date.month==startdate.month:
            end_date = enddate.date()
            zhouqilist = MeetingZhouqi.objects.all()
            for meetingmodel in zhouqilist:
                for i in range((end_date - begin_date).days+1):
                    eachdate = begin_date + datetime.timedelta(days=i)
                    if meetingmodel.zhouqitype==1:#日会议
                        tempobj = setZhouqiMeeting(eachdate,meetingmodel)
                        meetinglist.append(tempobj)
                    elif meetingmodel.zhouqitype==2:#周会议
                        weekday =get_week_day(eachdate)
                        weeklist = meetingmodel.create_time.split(',')
                        if weekday in weeklist:
                            tempobj = setZhouqiMeeting(eachdate,meetingmodel)
                            meetinglist.append(tempobj)
                    elif meetingmodel.zhouqitype==3:#月会议
                        monthday = "%02d" % eachdate.day
                        if monthday in meetingmodel.create_time.split(','):
                            tempobj = setZhouqiMeeting(eachdate,meetingmodel)
                            meetinglist.append(tempobj)

    response_data['meetings'] = meetinglist
    return HttpResponse(json.dumps(response_data,encoding="UTF-8",cls=CJsonEncoder,ensure_ascii=False), content_type="application/json")

@login_required(login_url="/login/")
def getMeetingMember(request):
    response_data = {}
    meetid = request.GET.get("meetid")
    huiyitype = int(request.GET.get('huiyitype',0))#1：取周期会议，0：普通会议
    if huiyitype==1:
        meetingusers = MeetingZhouqiUser.objects.filter(meeting_id=meetid)
    else:
        meetingusers = MeetingUser.objects.filter(meeting_id=meetid)
    userlist = []
    for usermodel in meetingusers:
        tempobj = {}
        tempobj['meeting_id'] = usermodel.meeting_id
        if huiyitype!=1:
            tempobj['isattend'] = usermodel.isattend
            tempobj['reason'] = usermodel.reason
        tempobj['user_id'] = usermodel.user_id
        tempobj['truename'] = usermodel.user.truename
        userlist.append(tempobj)
    response_data['issuc'] = 'true'
    response_data['meetingusers'] = userlist
    return HttpResponse(json.dumps(response_data,encoding="UTF-8",ensure_ascii=False),content_type="application/json")

@login_required(login_url="/login/")
def getMeetingFile(request):
    response_data = {}
    meetid = request.GET.get("meetid")
    huiyitype = int(request.GET.get('huiyitype',0))#1：取周期会议，0：普通会议
    if huiyitype==1:
        meeting_files = MeetingZhouqirelatedfile.objects.filter(meeting_id=meetid)
    else:
        meeting_files = Meetingrelatedfile.objects.filter(meeting_id=meetid)
    file_list = []
    for fileitem in meeting_files:
        item = {}
        item['fileid'] = str(fileitem.file.id)
        item['filename'] = str(fileitem.file.shortname)
        item['filepath'] = str(fileitem.file.filepath)+str(fileitem.file.name)
        item['isrecord'] = fileitem.isrecord
        file_list.append(item)
    response_data['issuc'] = 'true'
    response_data['meetingfiles'] = file_list
    return HttpResponse(json.dumps(response_data,encoding="UTF-8",ensure_ascii=False),content_type="application/json")

@login_required(login_url="/login/")
def meetnotice(request):
    if checkMobile(request):
        meet_id = request.GET.get('meetid','')
        status = int(request.GET.get('status',0))
        if meet_id!='':
            meetitem = Meeting.objects.get(id=meet_id)
            meetingusers = MeetingUser.objects.filter(meeting_id=meet_id)
            if MeetingUser.objects.filter(meeting_id=meet_id,user=request.user):
                status=MeetingUser.objects.filter(meeting_id=meet_id,user=request.user)[0].isattend
        templateName = 'MeetingManager/assist_meetnotice_mobile.html'
    return render_to_response(templateName, RequestContext(request, locals()))

def managerattend(request):
    response_data = {}
    response_data['issuc'] = True
    meetid = request.GET.get('meetid','')
    isattend = int(request.GET.get('status',0))
    reason = request.GET.get('reason','')
    try:
        datalist = MeetingUser.objects.filter(user_id=request.user.id,meeting_id=meetid)
        if len(datalist)>0:
            meetuser = datalist[0]
            meetuser.isattend = isattend
            meetuser.reason = reason
            meetuser.save()
            if isattend==2:
                meetmodal = Meeting.objects.get(id=meetid)
                pushmsg = ("%s不参加会议%s(%s),原因：%s") % (meetuser.user.truename,meetmodal.name,meetmodal.description,reason if reason else "未知" )
                PushMessage.objects.create(status=0, relatetype="不参加会议", relateid=meetid,
                                    agentid= Project.objects.get(id=CURRENT_PROJECT_ID).appid,
                                    fromuser_id=request.user.id, touser_id=meetmodal.hostuser.id, message=pushmsg)
        else:
            response_data['issuc'] = False
            response_data['msg'] = '没有对应记录'
    except Exception as e:
        raise


    return HttpResponse(json.dumps(response_data,encoding="UTF-8",ensure_ascii=False),content_type="application/json")

@login_required(login_url="/login/")
def loadHuiyiInfo(request):
    response_data = {}
    meetid = request.GET.get("meetid",'')
    if meetid:
        info = {}
        meetinfo = Meeting.objects.get(id=meetid)
        info['meetid'] = meetid
        info['name'] = meetinfo.name
        info['meetingtypeid'] = meetinfo.meetingtype_id
        info['meetingtypename'] = meetinfo.meetingtype.name
        info['roomname'] = meetinfo.roomname
        info['start'] = meetinfo.begin_time
        info['end'] = meetinfo.end_time
        info['hostuserid'] = meetinfo.hostuser_id
        info['hostusername'] = meetinfo.hostuser.truename
        info['description'] = meetinfo.description
        meetingusers = MeetingUser.objects.filter(meeting_id=meetid)
        userlist = []
        for usermodel in meetingusers:
            tmp = {}
            tmp["id"]=usermodel.user_id
            tmp["name"]=usermodel.user.truename
            userlist.append(tmp)
        info['members'] = userlist
        meeting_files = Meetingrelatedfile.objects.filter(meeting_id=meetid).order_by("isrecord")
        file_list = []
        for fileitem in meeting_files:
            item = {}
            item['fileid'] = fileitem.file.id
            item['filename'] = str(fileitem.file.shortname)
            item['filepath'] = str(fileitem.file.filepath)+str(fileitem.file.name)
            item['isrecord'] = fileitem.isrecord
            file_list.append(item)
        info['files'] = file_list
        response_data['issuc'] = 'true'
        response_data['meetinginfo'] = info
    else :
        response_data['issuc'] = 'false'
    return HttpResponse(json.dumps(response_data,encoding="UTF-8",cls=CJsonEncoder,ensure_ascii=False), content_type="application/json")

@login_required(login_url="/login/")
def uploadJiyao(request):
    response_data = {}
    meetid = request.GET.get('meetid')
    docs = request.GET.get('documents','')
    response_data['issuc'] = 'true'
    print docs
    try:
        mettingmodel = Meeting.objects.get(id=meetid)
        if docs!='':
            destdir = getTypeDirectory('meeting',mettingmodel)
            doclist = []
            docsarr = docs.split(",")
            for docid in docsarr:
                if Document.objects.filter(id=docid).count()==1:
                    tar = Document.objects.get(id=docid)
                    if destdir:
                        tar.docdirectory.add(destdir)
                        movefiletoDir(tar,destdir)
                else:
                    raise Exception(u'文件不存在！')
                doclist.append(Meetingrelatedfile(meeting_id=meetid,file_id=docid,isrecord=1))
            Meetingrelatedfile.objects.bulk_create(doclist)
    except Exception as e:
        print e
    return HttpResponse(json.dumps(response_data,encoding="UTF-8"), content_type="application/json")

@login_required(login_url="/login/")
@check_permission
def zhouqihuiyi(request):
    try:
        meetingtype_list = Meetingtype.objects.all()
        meetingroom_list = Meetingroom.objects.all()
        meetinglist = MeetingZhouqi.objects.filter().order_by('-id')
        issuelist = []
        for meetitem in meetinglist:
            tempobj = {}
            tempobj['id'] = meetitem.id
            tempobj['title'] = meetitem.name
            tempobj['hostuser'] = meetitem.hostuser.truename
            # print meetitem.begin_time
            tempobj['begin'] = meetitem.begin_time
            tempobj['end'] = meetitem.end_time
            tempobj['docsnum'] = MeetingZhouqirelatedfile.objects.filter(meeting_id=meetitem.id).count()
            tempobj['tishi'] = 0
            tempobj['room'] = meetitem.roomname
            tempobj['zhouqitype'] = meetitem.zhouqitype
            tempobj['create_time'] = meetitem.create_time
            tempobj['meetingtype'] = meetitem.meetingtype.name
            tempobj['canupdate'] = 1
            issuelist.append(tempobj)

        paginator = Paginator(issuelist, 10)
        listcount = len(issuelist)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            issuelist = paginator.page(page)
        except:
            issuelist = paginator.page(paginator.num_pages)
    except Exception as e:
        raise e
    return render_to_response('MeetingManager/huiyi_zhouqi.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
@check_permission_ajax
def deleteMeetingZhouqi(request):
    response_data = {}
    try:
        meetid = request.GET.get('meetid')
        response_data['issuc'] = 'true'
        MeetingZhouqiUser.objects.filter(meeting_id=meetid).delete()
        MeetingZhouqirelatedfile.objects.filter(meeting_id=meetid).delete()
        MeetingZhouqi.objects.filter(id=meetid).delete()
    except Exception as e:
        raise e
    return HttpResponse(json.dumps(response_data,encoding="UTF-8"), content_type="application/json")

@login_required(login_url="/login/")
def loadHuiyiZhouqiInfo(request):
    response_data = {}
    meetid = request.GET.get("meetid",'')
    if meetid:
        info = {}
        meetinfo = MeetingZhouqi.objects.get(id=meetid)
        info['meetid'] = meetid
        info['name'] = meetinfo.name
        info['meetingtype'] = meetinfo.meetingtype.id
        info['roomname'] = meetinfo.roomname
        info['start'] = meetinfo.begin_time
        info['end'] = meetinfo.end_time
        info['zhouqitype'] = meetinfo.zhouqitype
        info['create_time'] = meetinfo.create_time
        info['hostuser'] = meetinfo.hostuser.truename
        info['description'] = meetinfo.description
        meetingusers = MeetingZhouqiUser.objects.filter(meeting_id=meetid)
        userlist = []
        for usermodel in meetingusers:
            userlist.append(usermodel.user.truename)
        info['members'] = ','.join(userlist)
        meeting_files = MeetingZhouqirelatedfile.objects.filter(meeting_id=meetid).order_by("isrecord")
        file_list = []
        for fileitem in meeting_files:
            item = {}
            item['filename'] = str(fileitem.file.name)
            item['filepath'] = str(fileitem.file.filepath)+str(fileitem.file.name)
            item['isrecord'] = fileitem.isrecord
            file_list.append(item)
        info['files'] = file_list
        response_data['issuc'] = 'true'
        response_data['meetinginfo'] = info
    else :
        response_data['issuc'] = 'false'
    return HttpResponse(json.dumps(response_data,encoding="UTF-8",cls=CJsonEncoder,ensure_ascii=False), content_type="application/json")

@login_required(login_url="/login/")
def getMeetingZhouqiMember(request):
    response_data = {}
    meetid = request.GET.get("meetid")
    meetingusers = MeetingZhouqiUser.objects.filter(meeting_id=meetid)
    userlist = []
    for usermodel in meetingusers:
        tempobj = {}
        tempobj['meeting_id'] = usermodel.meeting_id
        tempobj['user_id'] = usermodel.user_id
        tempobj['truename'] = usermodel.user.truename
        userlist.append(tempobj)
    response_data['issuc'] = 'true'
    response_data['meetingusers'] = userlist
    return HttpResponse(json.dumps(response_data,encoding="UTF-8",ensure_ascii=False),content_type="application/json")


@login_required(login_url="/login/")
def zhilianglihui(request):
    try:
        meetingtype = request.GET.get('meetingtype', 'zhilianglihui')
        meetingroom = request.GET.get('meetingroom', '')
        createtTimerange = request.GET.get('createtTimerange', '')
        print createtTimerange
        meetingtype_list = Meetingtype.objects.all()
        meetingroom_list = Meetingroom.objects.all()

        meetinglist = Meeting.objects.filter(meetingtype__name="质量例会").order_by("-begin_time")
        if createtTimerange !="":
            startdate=datetime.datetime.strptime(createtTimerange+" 00:00:00",'%Y-%m-%d %H:%M:%S')
            enddate=datetime.datetime.strptime(createtTimerange+" 23:59:59",'%Y-%m-%d %H:%M:%S')
            print startdate
            meetinglist = meetinglist.filter(begin_time__range=(startdate,enddate))

        if meetingroom!='':
            meetinglist = meetinglist.filter(roomname__contains=meetingroom)

        issuelist = []
        currtime = Curr_time("%Y-%m-%d %H:%M:%S")
        for meetitem in meetinglist:
            tempobj = {}
            tempobj['id'] = meetitem.id
            tempobj['description'] = meetitem.description
            tempobj['hostuser'] = meetitem.hostuser.truename
            tempobj['begin'] = meetitem.begin_time
            tempobj['end'] = meetitem.end_time
            tempobj['docsnum'] = Meetingrelatedfile.objects.filter(meeting_id=meetitem.id).count()
            tempobj['tishi'] = 0
            if Meetingrelatedfile.objects.filter(meeting_id=meetitem.id,isrecord=1).count()==0:
                ct = CaltimeDay(str(meetitem.end_time),currtime)
                if int(ct)>7:
                    tempobj['tishi'] = 1
            tempobj['room'] = meetitem.roomname
            tempobj['meetingtype'] = meetitem.meetingtype.name
            if canEditMeeting(request.user,meetitem):
                tempobj['canupdate'] = 1
            else:
                tempobj['canupdate'] = 0
            issuelist.append(tempobj)

        paginator = Paginator(issuelist, 15)
        listcount = len(issuelist)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        try:
            issuelist = paginator.page(page)
        except:
            issuelist = paginator.page(paginator.num_pages)
    except Exception as e:
        raise e
    return render_to_response('MeetingManager/zhiliang_huiyi_list.html', RequestContext(request,locals()))
