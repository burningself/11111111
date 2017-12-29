# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from TaskAndFlow.utility import *
from TaskAndFlow.utility_flowtemplate import *
from TaskAndFlow.models import *
from TaskAndFlow.config import *
from Scc4PM.settings import CURRENT_PROJECT_ID
from UserAndPrj.models import *
from top.config import DXObject

text_msg_list = []
news_msg_list = ['事件','事件查看','会议','会议即将开始','会议修改','不参加会议','文件夹通知','公告']

class message_template(object):

    event_template = u'{0}{1}<a href="{2}/task/progress/problem/{3}/">点击查看！</a>'
    event_template_watch = u'{0}{1}<a href="{2}/task/progress/problem/watch/{3}/">点击查看！</a>'
    event_template_huiyi = u'{0}发起{1}<a href="{2}/assist/meetnotice/?status=1&meetid={3}">点击确认是否参加！</a>'
    event_template_edithuiyi = u'{0}<a href="{1}/assist/meetnotice/?status=0&meetid={2}">点击查看！</a>'
    event_template_filenotify = u'{0}在目录"{1}"下：{2}'
    notice_template = u'{0}于{1}<span style="color:red">发布公告：</span>{2}'

def getNewsContentAndUrls(msgObj):
    content=""
    url=""
    picurl=""
    if Project.objects.filter(id=CURRENT_PROJECT_ID):
        projecturl = Project.objects.get(id=CURRENT_PROJECT_ID).projecturl
    try:
        if msgObj.relatetype == "事件":
            content = "%s%s" % ("" if not msgObj.fromuser else msgObj.fromuser.truename, msgObj.message)
            url =  "%s/task/progress/problem/%d/" % (projecturl,msgObj.relateid)
            oprlist =  EventStepOperation.objects.filter(eventstep__projectevent_id=msgObj.relateid).order_by('-oprtime')
            if oprlist:
                lastestOpr = oprlist[0]
                relatelist = Doc2Relate.objects.filter(relatetype='事件步骤操作',relateid=lastestOpr.id,document__filetype__contains ="image")
                if relatelist:
                    picurl = "%s/%s%s" % (projecturl,str(relatelist[0].document.filepath),relatelist[0].document.name)
        elif msgObj.relatetype == "事件查看":
            content = "%s%s" % ("" if not msgObj.fromuser else msgObj.fromuser.truename, msgObj.message)
            url =  "%s/task/progress/problem/watch/%d/" % (projecturl,msgObj.relateid)
            oprlist =  EventStepOperation.objects.filter(eventstep__projectevent_id=msgObj.relateid).order_by('-oprtime')
            if oprlist:
                lastestOpr = oprlist[0]
                relatelist = Doc2Relate.objects.filter(relatetype='事件步骤操作',relateid=lastestOpr.id,document__filetype__contains ="image")
                if relatelist:
                    picurl = "%s/%s%s" % (projecturl,str(relatelist[0].document.filepath),relatelist[0].document.name)
        elif msgObj.relatetype == "会议":
            meeting = Meeting.objects.get(id=msgObj.relateid)
            content = "%s发起会议%s(%s),点击确认是否参加" % ("" if not msgObj.fromuser else msgObj.fromuser.truename,meeting.name,meeting.description)
            url =  "%s/assist/meetnotice/?meetid=%d" % (projecturl,msgObj.relateid)
            # relatelist = Meetingrelatedfile.objects.filter(meeting=meeting,file__filetype__contains ="image")
            # if relatelist:
            #     picurl = "%s/%s%s" % (projecturl,str(relatelist[0].file.filepath),relatelist[0].file.name)
        elif msgObj.relatetype == "会议即将开始":
            meeting = Meeting.objects.get(id=msgObj.relateid)
            timeremind = 1 
            content = "会议%s(%s)即将在%d小时后开始,点击确认是否参加" % (meeting.name,meeting.description, timeremind)
            url =  "%s/assist/meetnotice/?meetid=%d" % (projecturl,msgObj.relateid)
            # relatelist = Meetingrelatedfile.objects.filter(meeting=meeting,file__filetype__contains ="image")
            # if relatelist:
            #     picurl = "%s/%s%s" % (projecturl,str(relatelist[0].file.filepath),relatelist[0].file.name)
        elif msgObj.relatetype == "会议修改":
            meeting = Meeting.objects.get(id=msgObj.relateid)
            content = "%s,点击查看" % (msgObj.message)
            url =  "%s/assist/meetnotice/?meetid=%d" % (projecturl,msgObj.relateid)
            # relatelist = Meetingrelatedfile.objects.filter(meeting=meeting,file__filetype__contains ="image")
            # if relatelist:
            #     picurl = "%s/%s%s" % (projecturl,str(relatelist[0].file.filepath),relatelist[0].file.name)
        elif msgObj.relatetype == "不参加会议":
            meeting = Meeting.objects.get(id=msgObj.relateid)
            content = "%s,点击查看" % (msgObj.message)
            url =  "%s/assist/meetnotice/?meetid=%d" % (projecturl,msgObj.relateid)
        elif msgObj.relatetype == "公告":
            content = "%s于%s发布公告：%s" % (msgObj.fromuser.truename,msgObj.createtime.strftime("%Y/%m/%d"),msgObj.message)
        elif msgObj.relatetype == "文件夹通知":
            content = "%s在目录%s下：%s" % (msgObj.fromuser.truename,Directory.objects.get(id=msgObj.relateid).name,msgObj.message)

    except Exception as e:
        print e
    return content,url,picurl


def getTextcardContentAndUrls(msgObj):
    content=""
    url=""
    picurl=""
    if Project.objects.filter(id=CURRENT_PROJECT_ID):
        projecturl = Project.objects.get(id=CURRENT_PROJECT_ID).projecturl

    if msgObj.relatetype == "事件":
        event = projectevent.objects.get(id=msgObj.relateid)
        desc = "%s%s" % ("" if not msgObj.fromuser else msgObj.fromuser.truename, msgObj.message)
        content = "<div class=\"gray\">%s</div><div class=\"highlight\">%s</div><div class=\"normal\">问题编号： %s</div><div class=\"normal\">关联元素： %s</div><div class=\"normal\">截止时间： %s</div><div class=\"normal\">问题描述： %s</div>" % (datetime.date.today().strftime("%Y年%m月%d日"),desc,event.number,getEventRelateDesc(event),event.deadline.strftime("%Y年%m月%d日"),event.describe)
        url =  "%s/task/progress/problem/%d/" % (projecturl,msgObj.relateid)
    elif msgObj.relatetype == "事件查看":
        content = "%s%s" % ("" if not msgObj.fromuser else msgObj.fromuser.truename, msgObj.message)
        url =  "%s/task/progress/problem/watch/%d/" % (projecturl,msgObj.relateid)
        oprlist =  EventStepOperation.objects.filter(eventstep__projectevent_id=msgObj.relateid).order_by('-oprtime')
        if oprlist:
            lastestOpr = oprlist[0]
            relatelist = Doc2Relate.objects.filter(relatetype='事件步骤操作',relateid=lastestOpr.id,document__filetype__contains ="image")
            if relatelist:
                picurl = "%s/%s%s" % (projecturl,str(relatelist[0].document.filepath),relatelist[0].document.name)
    return content,url

class Command(BaseCommand):
    def handle(self, *args, **options):
        for each in PushMessage.objects.filter(status=0):
            bSendSuc = False
            if each.pushtime and datetime.datetime.now()<each.pushtime:
                continue

            if each.relatetype in text_msg_list:
                if send_txt_msg(convertMessage(each) , "" if not each.touser else each.touser.contract, "" if not each.toparty else str(each.toparty) ,\
                                "" if not each.totag else str(each.totag), each.agentid):
                    bSendSuc = True
                else:
                    print "消息发送失败！"
            else:
                content,url,picurl = getNewsContentAndUrls(each)
                title = each.relatetype+"通知"
                if each.title:
                    title = each.title
                if send_news_msg(title,content,url ,picurl, "" if not each.touser else each.touser.contract, "" if not each.toparty else str(each.toparty) ,\
                                "" if not each.totag else str(each.totag), each.agentid):
                    bSendSuc = True
                else:
                    print "消息发送失败！"

            if bSendSuc:
                each.status=1
                each.save()
        return

def convertMessage(msgObj):
    msg = "不支持的消息"
    try:
        if Project.objects.filter(id=CURRENT_PROJECT_ID):
            projecturl = Project.objects.get(id=CURRENT_PROJECT_ID).projecturl

        if msgObj.relatetype == "事件":
            msg = message_template.event_template
            msg = msg.format("" if not msgObj.fromuser else msgObj.fromuser.truename, msgObj.message,projecturl,str(msgObj.relateid))
        elif msgObj.relatetype == "事件查看":
            msg = message_template.event_template_watch
            msg = msg.format("" if not msgObj.fromuser else msgObj.fromuser.truename, msgObj.message,projecturl,str(msgObj.relateid))
        elif msgObj.relatetype == "会议":
            msg = message_template.event_template_huiyi
            msg = msg.format("" if not msgObj.fromuser else msgObj.fromuser.truename,msgObj.message,projecturl,str(msgObj.relateid))
        elif msgObj.relatetype == "会议修改":
            msg = message_template.event_template_edithuiyi
            msg = msg.format(msgObj.message,projecturl,str(msgObj.relateid))
        elif msgObj.relatetype == "不参加会议":
            msg = message_template.event_template_edithuiyi
            msg = msg.format(msgObj.message,projecturl,str(msgObj.relateid))
        elif msgObj.relatetype == "文件夹通知":
            msg = message_template.event_template_filenotify
            msg = msg.format(msgObj.fromuser.truename,Directory.objects.get(id=msgObj.relateid).name,msgObj.message)
        elif msgObj.relatetype == "公告":
            msg = message_template.notice_template
            msg = msg.format(msgObj.fromuser.truename,msgObj.createtime.strftime("%Y/%m/%d"),msgObj.message)
        else:
            msg = "不支持的消息"
    except:
        pass

    return msg

def send_txt_msg(content, to_user="", to_party="", to_tag="", application_id=0, safe=0):
    try:
        if not to_user and not to_party and not to_tag:
            return True
        
        data = {
            "touser": to_user,
            "toparty": to_party,
            "totag": to_tag,
            "msgtype": "text",
            "agentid": application_id,
            "text": {"content": content},
            "safe": safe
        }

        data = json.dumps(data, ensure_ascii=False).encode('UTF-8')
        token = fetch_qiye_token()

        if token:
            req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (token,))
            resp = urllib2.urlopen(req, data)
            res = eval(resp.read()) 
            print res
            if res["errcode"]!=0:
                raise Exception('send msg error: %s' % res["errmsg"])

    except Exception, ex:

        print ex
        return False
    
    return True

def send_news_msg(title,content, url,picurl,to_user="", to_party="", to_tag="", application_id=0, safe=0):
    try:
        if not to_user and not to_party and not to_tag:
            return True
            
        data = {
            "touser": to_user,
            "toparty": to_party,
            "totag": to_tag,
            "msgtype": "news",
            "agentid": application_id,
            "news": {
               "articles":[
                    {
                       "title": title,
                       "description": content,
                       "url": url,
                       "picurl":picurl
                    }
                ]
           },
           "safe": safe
        }

        data = json.dumps(data, ensure_ascii=False).encode('UTF-8')
        token = fetch_qiye_token()

        if token:
            req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (token,))
            resp = urllib2.urlopen(req, data)
            res = eval(resp.read()) 
            print res
            if res["errcode"]!=0:
                raise Exception('send msg error: %s' % res["errmsg"])
    except Exception, ex:
        print ex
        return False
    
    return True

def send_textcard_msg(title,content, url,to_user="", to_party="", to_tag="", application_id=0, safe=0):
    try:
        if not to_user and not to_party and not to_tag:
            return True
            
        data = {
            "touser": to_user,
            "toparty": to_party,
            "totag": to_tag,
            "msgtype": "textcard",
            "agentid": application_id,
            "textcard": {
                       "title": title,
                       "description": content,
                       "url": url,
                       "btntxt":"点击查看详情"
             },
           "safe": safe
        }

        data = json.dumps(data, ensure_ascii=False).encode('UTF-8')
        token = fetch_qiye_token()

        if token:
            req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (token,))
            resp = urllib2.urlopen(req, data)
            res = eval(resp.read()) 
            print res
            if res["errcode"]!=0:
                raise Exception('send msg error: %s' % res["errmsg"])
    except Exception, ex:
        print ex
        return False
    
    return True


def getMsgInfo(msgObj):
    msgType,msgContent="",""
    if msgObj.relatetype == "会议":
        msgType = DXObject.DXID_huiyi
        msgContent = msgObj.message[:20]
        
    elif msgObj.relatetype == "会议修改":
        msgType = DXObject.DXID_huiyixiugai
        msgContent = msgObj.message[:20]
        
    elif msgObj.relatetype == "公告":
        msgType = DXObject.DXID_gonggao
        msgContent = msgObj.message[:20]
         
    elif "事件" in msgObj.relatetype and "发起安全" in msgObj.message:
        msgType = DXObject.DXID_anquan 
        try:
            msgContent = ": "+ msgObj.message[6:]
        except:
            msgContent = msgObj.message[:20]
        
    elif "事件" in msgObj.relatetype and "发起质量" in msgObj.message:
        msgType = DXObject.DXID_zhiliang 
        try:
            msgContent = ": "+ msgObj.message[6:]
        except:
            msgContent = msgObj.message[:20]
        
    elif "事件" in msgObj.relatetype and "问题" in msgObj.message:
        msgType = DXObject.DXID_wentiupdate
        try:
            msgContent = ": "+ msgObj.message[6:]
        except:
            msgContent = msgObj.message[:20]
    
    try:
        if Project.objects.filter(id=CURRENT_PROJECT_ID):
                projectName = Project.objects.get(id=CURRENT_PROJECT_ID).acronym
    except:
        projectName = ""
    
    return msgContent+"(" + projectName + ")", msgType    
        
        
