# -*- coding: utf-8 -*-
#import logging
#logging.basicConfig(filename='/www/log/myapp.log',filemode='w')
import os,time,random, sys, datetime, calendar, traceback
import memcache
import urllib2,json
from Scc4PM import settings
from TaskAndFlow.models import *
from UserPrjConfig.models import *
from django.db.models import Q
from django.db.models import Sum
from uuid import uuid1
from TaskAndFlow.utility_filemanager import *

import top.api

def createWXUser(name,contract,company):
    try:
        access_token = fetch_wxContract_token()
        print name,contract,company
        depId = getDepartment(access_token,company,1)    
        print depId    
        createWXAccount(access_token, contract, name, depId)
        
    except:
        traceback.print_exc()

def createWXAccount(access_token, contract, name, depId):
    try:
        tkUrl = "https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token=" + access_token
        data = {
            "userid": contract,
            "name": name,
            "mobile": contract,
            "department": [depId],
            "enable":1,
        }

        data = json.dumps(data, ensure_ascii=False).encode('UTF-8')
        req = urllib2.Request(tkUrl)
        res_data = urllib2.urlopen(req, data)
        jsonDic = json.load(res_data)
        print jsonDic
        if not jsonDic['errcode']:
            return True
        else:
            print jsonDic
    except:
        return False

def getDepartment(access_token,company,parent=1):
    try:
        tkUrl = "https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=" + access_token
        tkReq = urllib2.Request(tkUrl)
        res_data = urllib2.urlopen(tkReq)
        jsonDic = json.load(res_data)
        print jsonDic
        if not jsonDic['errcode']:
            departmentList = jsonDic['department']
            depId=0
            for each in departmentList:
                if each['name'] == company:
                    depId = each['id']
            
            if depId == 0:
                depId = createDepartment(access_token,company,parent)

        return depId
    except:
        return 1

def createDepartment(access_token,company,parent):
    try:
        tkUrl = "https://qyapi.weixin.qq.com/cgi-bin/department/create?access_token=" + access_token
        
        data = {
           "name": company,
           "parentid": parent,
        }

        data = json.dumps(data, ensure_ascii=False).encode('UTF-8')
        req = urllib2.Request(tkUrl)
        res_data = urllib2.urlopen(req, data)
        jsonDic = json.load(res_data)
        print jsonDic
        if not jsonDic['errcode']:
            return jsonDic['id']
        else:
            return 1
    except:
        return 1
    

def fetch_wxContract_token():
    pjobj = Project.objects.get(id=settings.CURRENT_PROJECT_ID)
    mc=memcache.Client(['127.0.0.1:11211'],debug=0)
    access_token = mc.get(pjobj.corpid+'_qiye_wxtoken')
    if not access_token:
        tkUrl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + pjobj.corpid + '&corpsecret=' + pjobj.wxsecret
        
        tkReq = urllib2.Request(tkUrl)
        res_data = urllib2.urlopen(tkReq)
        access_token = json.load(res_data)['access_token']
        mc.set(pjobj.corpid+'_qiye_wxtoken',access_token,4000)
    
    return access_token
            
def checkMobile(request):
    import re
    userAgent = request.META['HTTP_USER_AGENT']
 
    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
    _short_matches = re.compile(_short_matches, re.IGNORECASE)
 
    if _long_matches.search(userAgent) != None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) != None:
        return True
    return False     

def getMobileConfig(request):
    config={}
    ticket, appid, _ = fetch_ticket()
    
    sign = Sign(ticket, "http://" + request.META["HTTP_HOST"] + request.get_full_path())
    
    config = sign.sign()
    config["appid"] = appid

    return config

def getCoprInfo():
    pjobj = Project.objects.get(id=settings.CURRENT_PROJECT_ID)

    return pjobj.corpid, pjobj.secretid, "prj"+str(pjobj.id)

def fetch_ticket():
    corp_id, secret, corp_info = getCoprInfo()
  
    mc=memcache.Client(['127.0.0.1:11211'],debug=0)
    ticket=mc.get(corp_info+'_api_ticket')
    appid = ''
    access_token = mc.get(corp_info+'_qiye_token')
#    if access_token:
#        sys.stderr.write((access_token+"\n").encode('utf-8'))
    if settings.IS_LOCAL_DEBUG:
        print "loacl debug no need access_token"
        return ticket, appid, access_token

    if not ticket or not access_token:
        tkUrl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corp_id + '&corpsecret=' + secret
        
        tkReq = urllib2.Request(tkUrl)
        res_data = urllib2.urlopen(tkReq)
        access_token = json.load(res_data)['access_token']
        mc.set(corp_info+'_qiye_token',access_token,4000)
        
        ticketUrl = 'https://qyapi.weixin.qq.com/cgi-bin/get_jsapi_ticket?access_token=' + access_token
        
        ticketReq = urllib2.Request(ticketUrl)
        res_data = urllib2.urlopen(ticketReq)
        ticket = json.load(res_data)['ticket']
        
        mc.set(corp_info+"_api_ticket",ticket,4000)
    
    return ticket, corp_id, access_token

def fetch_qiye_token():
    corp_id, secret, corp_info = getCoprInfo()
    
    mc=memcache.Client(['127.0.0.1:11211'],debug=0)
    access_token=mc.get(corp_info+'_qiye_token')
#    if access_token:
#        sys.stderr.write((access_token+"\n").encode('utf-8'))
    
    if settings.IS_LOCAL_DEBUG:
        print "loacl debug no need access_token"
        return access_token

    if not access_token:
        tkUrl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (corp_id, secret)
        
        tkReq = urllib2.Request(tkUrl)
        res_data = urllib2.urlopen(tkReq)
        access_token = json.load(res_data).get('access_token',False)
        if access_token:
            mc.set(corp_info+"_qiye_token",access_token,5000)
    
    return access_token


def send_mobile_msg(name, content, number, type=''):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo('24656980','e87c693c4588919338164c256112f1a4'))
     
    req.extend = ""
    req.sms_type = "normal"
    req.sms_free_sign_name = "智慧建造平台"
    req.sms_param = "{name:'" + name + "',content:'" + content + "'}"
    req.rec_num = number
    req.sms_template_code = type
    try :
        resp = req.getResponse()
        print (resp)
        return True
    except Exception,e:
        print (e)
        return False




import string
import hashlib
class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret   

def refreshPbstatus(pbObj):
    if PBStatusRecord.objects.filter(precastbeam=pbObj, isactive=1):
        latestStatus = PBStatusRecord.objects.filter(precastbeam=pbObj, isactive=1).order_by("-status__sequence")[0]
        pbObj.curstatus_id = latestStatus.status_id
        pbObj.curfactoryposition_id = latestStatus.factoryposition_id
        pbObj.save()

def fetchStatusList(MoteleObj, user=None):
    statuslist = None
    statuslist_zhijian = None
    if MoteleObj.typetable == u"构件":
        pbObj = PrecastBeam.objects.get(id=MoteleObj.relatedid)
        if user:
            if user.is_admin:
                if PBStatus.objects.filter(pbtype=pbObj.pbtype): 
                    statuslist = PBStatus.objects.filter(pbtype=pbObj.pbtype)
                else:
                    statuslist = PBStatus.objects.filter(pbtype=None)
            else:
                if PBStatus.objects.filter(pbtype=pbObj.pbtype): 
                    statuslist = PBStatus.objects.filter(Q(pbtype=pbObj.pbtype) & Q(user2pbstatus__user=user))
                else:
                    statuslist = PBStatus.objects.filter(Q(pbtype=None) & Q(user2pbstatus__user=user))

        else:
            if PBStatus.objects.filter(pbtype=pbObj.pbtype):   
                statuslist = PBStatus.objects.filter(pbtype=pbObj.pbtype)
            else:
                statuslist = PBStatus.objects.filter(pbtype=None)
        
    elif MoteleObj.typetable == u"构件组":
        pbObj = Pbgroup.objects.get(id=MoteleObj.relatedid)
        if user:
            if user.is_admin:
                if PBStatus.objects.filter(pbtype=pbObj.pbtype): 
                    statuslist = PBStatus.objects.filter(pbtype=pbObj.pbtype)
                else:
                    statuslist = PBStatus.objects.filter(pbtype=None)
            else:
                if PBStatus.objects.filter(pbtype=pbObj.pbtype): 
                    statuslist = PBStatus.objects.filter(Q(pbtype=pbObj.pbtype) & Q(user2pbstatus__user=user))
                else:
                    statuslist = PBStatus.objects.filter(Q(pbtype=None) & Q(user2pbstatus__user=user))

        else:
            if PBStatus.objects.filter(pbtype=pbObj.pbtype):   
                statuslist = PBStatus.objects.filter(pbtype=pbObj.pbtype)
            else:
                statuslist = PBStatus.objects.filter(pbtype=None)
        
    elif MoteleObj.typetable == u"施工机械":
        pass
    elif MoteleObj.typetable == u"任务":
        pass
    else:
        pass

    return statuslist

def fetchZhiJianStatusList(MoteleObj):
    statuslist_zhijian = None
    if MoteleObj.typetable == u"构件":
        statuslist_zhijian=[each[0] for each in PBStatusRecord.objects.filter(precastbeam_id=MoteleObj.relatedid).values_list("status").distinct().order_by("status_id")]
    elif MoteleObj.typetable == u"构件组":
        pbgrp = Pbgroup.objects.get(id=MoteleObj.relatedid)
        if Pbgrouprelation.objects.filter(pbgroup = pbgrp).count()>0:
            pb = Pbgrouprelation.objects.filter(pbgroup = pbgrp)[0].pb
            statuslist_zhijian=[each[0] for each in PBStatusRecord.objects.filter(precastbeam=pb).values_list("status").distinct().order_by("status_id")]
    elif MoteleObj.typetable == u"施工机械":
        pass
    elif MoteleObj.typetable == u"任务":
        pass
    else:
        pass

    return statuslist_zhijian

def getCurStatus(MoteleObj):
    curstatus = None
    if MoteleObj.typetable == u"构件":
        curstatus = PrecastBeam.objects.get(id=MoteleObj.relatedid).curstatus
    elif MoteleObj.typetable == u"构件组":
        curstatus = Pbgroup.objects.get(id=MoteleObj.relatedid).curstatus
    elif MoteleObj.typetable == u"施工机械":
        pass
    elif MoteleObj.typetable == u"任务":
        pass
    else:
        pass

    return curstatus

def getStatusObj(MoteleObj,statusId):
    statusObj = None
    isqualify = False
    if MoteleObj.typetable == u"构件":
        statusObj = PBStatus.objects.get(id=statusId)
        isqualify = statusObj.isqualify
    elif MoteleObj.typetable == u"构件组":
        statusObj = PBStatus.objects.get(id=statusId)
        isqualify = statusObj.isqualify
    elif MoteleObj.typetable == u"安全设施":
        statusObj = PBStatus.objects.get(id=statusId)
        isqualify = statusObj.isqualify
    elif MoteleObj.typetable == u"施工机械":
        pass
    elif MoteleObj.typetable == u"任务":
        pass
    else:
        pass

    return statusObj,isqualify

def updateAcceptance(MoteleObj,statusObj,curdatetime):
    #根据状态提醒，发起工序验收 pgb       
    if Pbstatusremind.objects.filter(pbstatus=statusObj).count()>0:
        reminder = Pbstatusremind.objects.filter(pbstatus=statusObj)[0]
        if not Acceptance.objects.filter(status=reminder.next_status,monitoring=MoteleObj):
            Acceptance.objects.create(name= reminder.next_status.statusname,warntime=curdatetime,deadline=curdatetime+datetime.timedelta(hours=reminder.time_span), \
                                  status=reminder.next_status, monitoring=MoteleObj)  
        
    #根据状态，是否有工序验收需要结束
    if Acceptance.objects.filter(status=statusObj,monitoring=MoteleObj).count()>0:
        Acceptance.objects.filter(status=statusObj,monitoring=MoteleObj).update(is_finished = True)

def updateAcceptanceInfo(MoteleObj,statusObj,curdatetime,actoruser):
    #根据质量验收提醒，发起质量验收 pgb       
    if AcceptanceRemind.objects.filter(pbstatus=statusObj).count()>0:
        reminder = AcceptanceRemind.objects.filter(pbstatus=statusObj)[0]
        Acceptanceinfo.objects.create(acceptancetype= reminder.acceptancetype,finiishedtime=curdatetime+datetime.timedelta(hours=reminder.time_span), status=1,\
                                  acceptuser=actoruser, relatedspace_type=MoteleObj.typetable, relatedspace_id=MoteleObj.relatedid,comment=statusObj.statusname)  
    

def updateMoteleObjStatus(MoteleObj,statusObj,actoruser,duichangObj,beizhu,percent,latitude=None,longitude=None,curdatetime=None):
     #update status
    color_code="blue"
    result_string = "扫码验收成功！"
    pbrecordid = None
    if not curdatetime:
        curdatetime = datetime.datetime.now()

    if MoteleObj.typetable == u"构件":
        try:
            goujianObj = PrecastBeam.objects.get(id=MoteleObj.relatedid)
            sumPercentage = PBStatusRecord.objects.filter(status= statusObj,precastbeam=goujianObj,isactive=True,
                                          percentage__isnull=False).aggregate(Sum('percentage'))["percentage__sum"]
            if not sumPercentage:
                sumPercentage = 0

            if sumPercentage==100:
                color_code="red"
                result_string="该状态已扫码验收！"
                return color_code,result_string,pbrecordid
            
            isAddBefore = False #是否补录之前的状态
            if not statusObj.isqualify and goujianObj.curstatus and goujianObj.curstatus.sequence>statusObj.sequence:
                isAddBefore = True
                if not actoruser.has_perm("补录扫码进度"):
                    color_code="red"
                    result_string=goujianObj.curstatus.statusname+"已扫码，不允许扫码"+statusObj.statusname
                    return color_code,result_string,pbrecordid

            if sumPercentage+float(percent)>100:
                color_code="red"
                result_string="累计完成工作量已超出100%"
                return color_code,result_string,pbrecordid

            if not isAddBefore:
                goujianObj.curstatus = statusObj
                goujianObj.curfactoryposition = duichangObj
                goujianObj.curstatustime = curdatetime
                goujianObj.curstatuspercent = sumPercentage+float(percent)
                goujianObj.curstatusdesc = beizhu
                goujianObj.save()
            
            #构件分组扫码的代码先去掉 pgb
            newRecord=PBStatusRecord.objects.create(status= statusObj,precastbeam=goujianObj,actor=actoruser,factoryposition=duichangObj, \
                                                    description=beizhu,percentage=percent, latitude=latitude, longitude=longitude,time=curdatetime)  
            

            result_string=  "扫码验收成功！" 

            pbrecordid = newRecord.id
            
            #扫码不合格发起流程 pgb     
            if statusObj.isqualify:
                if statusObj.relatedflowtemplate:
                    result_string="扫码成功，已发起整改流程。" 
                else:
                    result_string="扫码成功，不合格状态未关联整改流程。" 
            else:
                result_string=  "扫码验收成功！" 

            #更新上一个状态工作量为100
            if statusObj.sequence>=1:
                beforStatus = PBStatus.objects.filter(pbtype=statusObj.pbtype,sequence=statusObj.sequence-1)[0]
                sumbeforePercentage = PBStatusRecord.objects.filter(status= beforStatus,precastbeam=goujianObj,isactive=True,
                                              percentage__isnull=False).aggregate(Sum('percentage'))["percentage__sum"]
                if sumbeforePercentage and sumbeforePercentage!=100:
                    PBStatusRecord.objects.create(status= beforStatus,precastbeam=goujianObj,actor=actoruser,description="",percentage=(100-sumbeforePercentage), time=curdatetime)  

            #工序验收
            updateAcceptance(MoteleObj,statusObj,curdatetime)

            updateAcceptanceInfo(MoteleObj,statusObj,curdatetime,actoruser)

            #注释掉，如果出现问题，再强制更新 pgb
            #refreshPbstatus(goujianObj)
            
            statusId = statusObj.id
            if duichangObj: 
                duichangId = duichangObj.id 
            
        except Exception as e :
            traceback.print_exc()
            color_code="red"
            result_string="数据错误，上传失败！"
    elif  MoteleObj.typetable == u"构件组":
        color_code="red"
        result_string = "构件组扫码已经被弃用，你怎么进来的？"
    elif MoteleObj.typetable == u"任务":
        color_code="red"
        result_string = "暂不支任务扫码验收！"
    elif  MoteleObj.typetable == u"施工机械":
        color_code="red"
        result_string = "暂不支持施工机械扫码验收！"
    else:
        color_code="red"
        result_string = "未知扫码元素类型！"

    return color_code,result_string,pbrecordid

def updateMoteleObjStatusAppend(MoteleObj,status,beizhu,latitude=None,longitude=None):
    #update status
    retstatus="Succeed"
    result_string = "扫码验收成功！"
    msg = "验收信息补充成功！"
    pbrecordid = None
    if MoteleObj.typetable == u"构件":
        try:
            if PBStatusRecord.objects.filter(status_id= status,precastbeam_id=MoteleObj.relatedid, isactive=1):
                pbrecordObj=PBStatusRecord.objects.filter(status_id= status,precastbeam=MoteleObj.relatedid, isactive=1).order_by('-time')[0]
                pbrecordObj.description=beizhu
                pbrecordObj.save()
                pbrecordid = pbrecordObj.id
            else:
                retstatus = "Fail"
                msg="无扫码记录,提交失败！"
        except Exception as e :
            traceback.print_exc()
            retstatus = "Fail"
            msg="数据错误，上传失败！"
    elif  MoteleObj.typetable == u"构件组":
        try:
            pblist = [each.pb.id for each in Pbgrouprelation.objects.filter(pbgroup_id=MoteleObj.relatedid)]
            PBStatusRecord.objects.filter(precastbeam_id__in=pblist,status_id= status, isactive=1).update(description=beizhu)
        except Exception as e :
            traceback.print_exc()
            retstatus = "Fail"
            msg="数据错误，上传失败！"
    elif MoteleObj.typetable == u"任务":
        retstatus = "Fail"
        msg = "暂不支任务扫码验收！"
    elif  MoteleObj.typetable == u"施工机械":
        retstatus = "Fail"
        msg = "暂不支持施工机械扫码验收！"
    else:
        retstatus = "Fail"
        msg = "未知扫码元素类型！"

    return retstatus,msg,pbrecordid

def getTypeDirectory(docType,relateObj=None):
    dir = None
    if docType=='jishufangan':
        if Directory.objects.filter(name="方案管理",islock=True).count()>0:
            dir = Directory.objects.get(name="方案管理",islock=True)
    elif docType=='anquanjiancha':
        if Directory.objects.filter(name="安全检查",islock=True).count()>0:
            dir = Directory.objects.get(name="安全检查",islock=True)
    elif docType=='hazardevent':
        if Directory.objects.filter(name="危险源",islock=True).count()>0:
            dir = Directory.objects.get(name="危险源",islock=True)
    elif docType=='zhiliangyanshou':
        if Directory.objects.filter(name="质量验收",islock=True).count()>0:
            dir = Directory.objects.get(name="质量验收",islock=True)
    elif docType=='weekly':
        if Directory.objects.filter(name="工程周报",islock=True).count()>0:
            dir = Directory.objects.get(name="工程周报",islock=True)
    elif docType=='quality':
        if relateObj.template.flowtype.name=='质量问题':
            if Directory.objects.filter(name="质量整改单",islock=True).count()>0:
                parentdir = Directory.objects.get(name="质量整改单",islock=True)
                if Directory.objects.filter(name=relateObj.number,parent=parentdir).count()>0:
                    dir = Directory.objects.filter(name=relateObj.number,parent=parentdir)[0]
                else:
                    dir = Directory.objects.create(name=relateObj.number,parent=parentdir,creator_id=1,islock=True)
        elif relateObj.template.flowtype.name=='安全问题':
            if Directory.objects.filter(name="安全整改单",islock=True).count()>0:
                parentdir = Directory.objects.get(name="安全整改单",islock=True)
                if Directory.objects.filter(name=relateObj.number,parent=parentdir).count()>0:
                    dir = Directory.objects.filter(name=relateObj.number,parent=parentdir)[0]
                else:
                    dir = Directory.objects.create(name=relateObj.number,parent=parentdir,creator_id=1,islock=True)
        elif relateObj.template.flowtype.name=='现场签证':
            if Directory.objects.filter(name="现场签证",islock=True).count()>0:
                parentdir = Directory.objects.get(name="现场签证",islock=True)
                dirname = ("%s_%s") % (relateObj.number,relateObj.title)
                if Directory.objects.filter(name=dirname,parent=parentdir).count()>0:
                    dir = Directory.objects.filter(name=dirname,parent=parentdir)[0]
                else:
                    dir = Directory.objects.create(name=dirname,parent=parentdir,creator_id=1,islock=True)
        elif relateObj.template.flowtype.name=='工程进度款申请':
            if Directory.objects.filter(name="工程进度款申请",islock=True).count()>0:
                parentdir = Directory.objects.get(name="工程进度款申请",islock=True)
                dirname = ("%s_%s") % (relateObj.number,relateObj.title)
                if Directory.objects.filter(name=dirname,parent=parentdir).count()>0:
                    dir = Directory.objects.filter(name=dirname,parent=parentdir)[0]
                else:
                    dir = Directory.objects.create(name=dirname,parent=parentdir,creator_id=1,islock=True)
        elif relateObj.template.flowtype.name=='设计变更通知':
            if Directory.objects.filter(name="设计变更",islock=True).count()>0:
                topdir = Directory.objects.get(name='设计变更',islock=True)
                extenddict = eval(relateObj.extend)
                if extenddict.has_key("category"):
                    parentname = extenddict["category"]
                    if Directory.objects.filter(name=parentname,parent=topdir).count()>0:
                        parentdir = Directory.objects.filter(name=parentname,parent=topdir)[0]
                    else:
                        parentdir = Directory.objects.create(name=parentname,parent=topdir,creator_id=1,islock=True)
                else:
                    parentdir = topdir
                dirname = ("%s_%s") % (relateObj.number,relateObj.title)
                if Directory.objects.filter(name=dirname,parent=parentdir).count()>0:
                    dir = Directory.objects.filter(name=dirname,parent=parentdir)[0]
                else:
                    dir = Directory.objects.create(name=dirname,parent=parentdir,creator_id=1,islock=True)
        elif relateObj.template.flowtype.name=='变更设计备案':
            if Directory.objects.filter(name="技术核定单",islock=True).count()>0:
                topdir = Directory.objects.get(name='技术核定单',islock=True)
                extenddict = eval(relateObj.extend)
                if extenddict.has_key("category"):
                    parentname = extenddict["category"]
                    if Directory.objects.filter(name=parentname,parent=topdir).count()>0:
                        parentdir = Directory.objects.filter(name=parentname,parent=topdir)[0]
                    else:
                        parentdir = Directory.objects.create(name=parentname,parent=topdir,creator_id=1,islock=True)
                else:
                    parentdir = topdir
                dirname = ("%s_%s") % (relateObj.number,relateObj.title)
                if Directory.objects.filter(name=dirname,parent=parentdir).count()>0:
                    dir = Directory.objects.filter(name=dirname,parent=parentdir)[0]
                else:
                    dir = Directory.objects.create(name=dirname,parent=parentdir,creator_id=1,islock=True)
        elif relateObj.template.flowtype.name=='图纸会审':
            rootdir = Directory.objects.get(parent__name='根目录',name='技术管理',islock=True)
            if Directory.objects.filter(parent=rootdir,name="05_图纸会审",islock=True).count()>0:
                topdir = Directory.objects.get(parent=rootdir,name='05_图纸会审',islock=True)
            else:
                topdir = Directory.objects.create(parent=rootdir,name='05_图纸会审',creator_id=1,islock=True)
            extenddict = eval(relateObj.extend)
            if extenddict.has_key("category"):
                parentname = extenddict["category"]
                if Directory.objects.filter(name=parentname,parent=topdir).count()>0:
                    parentdir = Directory.objects.filter(name=parentname,parent=topdir)[0]
                else:
                    parentdir = Directory.objects.create(name=parentname,parent=topdir,creator_id=1,islock=True)
            else:
                parentdir = topdir
            dirname = ("%s_%s") % (relateObj.number,relateObj.title)
            if Directory.objects.filter(name=dirname,parent=parentdir).count()>0:
                dir = Directory.objects.filter(name=dirname,parent=parentdir)[0]
            else:
                dir = Directory.objects.create(name=dirname,parent=parentdir,creator_id=1,islock=True)
        elif relateObj.template.flowtype.name=='BIM深化':
            rootdir = Directory.objects.get(parent__name='根目录',name='技术管理',islock=True)
            if Directory.objects.filter(parent=rootdir,name="06_BIM深化",islock=True).count()>0:
                parentdir = Directory.objects.get(parent=rootdir,name='06_BIM深化',islock=True)
            else:
                parentdir = Directory.objects.create(parent=rootdir,name='06_BIM深化',creator_id=1,islock=True)
                
            dirname = ("%s_%s") % (relateObj.number,relateObj.title)
            if Directory.objects.filter(name=dirname,parent=parentdir).count()>0:
                dir = Directory.objects.filter(name=dirname,parent=parentdir)[0]
            else:
                dir = Directory.objects.create(name=dirname,parent=parentdir,creator_id=1,islock=True)
        else:
            pass
    elif docType=='meeting':
        if Directory.objects.filter(name='会议中心',islock=True):
            topdir = Directory.objects.get(name='会议中心',islock=True)
            parentname = relateObj.meetingtype.name
            if Directory.objects.filter(name=parentname,parent=topdir).count()>0:
                parentdir = Directory.objects.filter(name=parentname,parent=topdir)[0]
            else:
                parentdir = Directory.objects.create(name=parentname,parent=topdir,creator_id=1,islock=True)
            dirname = relateObj.begin_time.strftime("%Y.%m.%d_") + relateObj.name
            if Directory.objects.filter(name=dirname,parent=parentdir).count()>0:
                dir = Directory.objects.filter(name=dirname,parent=parentdir)[0]
            else:
                dir = Directory.objects.create(name=dirname,parent=parentdir,creator_id=1,islock=True)


    return dir

    
def uploadfile_weixin(mediaList, name, doctype, relatetype, user, relateid,relateObj=None ):
    try:
        codeRes=0
        userid = user.id
        path=settings.UPLOAD_DIR

        if not os.path.exists(path):
            os.makedirs(path)
            
        tgtLink = []
        _, _, tk = fetch_ticket()
        
        for each in mediaList:
            tgtLink.append('https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token=' + tk + '&media_id=' + each)
        
        dir = getTypeDirectory(doctype,relateObj) 
        index = 1
        for each in tgtLink:
            try:
                f = urllib2.urlopen(each) 
                data = f.read() 
                flag = time.strftime('%Y%m%d%H%M%S')
                # fn = "_" + '_%d' % relateid + '_%d' % index
                fn = "_%d_%s_%d"%(relateid,flag,index)
                index +=1
                filename = str(name) + fn + ".jpg"
                uuid_file_name = str(uuid1())+ ".jpg"

                full_file_name = path + uuid_file_name
#                sys.stderr.write(full_file_name.encode('utf-8'))

                with open(full_file_name, "wb") as code:     
                    code.write(data)
                doc = Document()
                doc.name = uuid_file_name
                doc.shortname = filename
                doc.filepath = path
                doc.doctype= doctype
                doc.creator_id=userid
                doc.createtime=datetime.datetime.now()
                doc.filesize = f.headers['content-length']
                doc.filetype = f.headers['content-type']
                doc.save()   
                
                Doc2Relate.objects.create(relatetype=relatetype, relateid=relateid, creator_id=user.id, document_id=doc.id, createtime=datetime.datetime.now())
                
                if dir:
                    doc.docdirectory.add(dir)
                    movefiletoDir(doc,dir)
                
            except Exception as e:
                traceback.print_exc()
                codeRes=1
            
    except PrecastBeam.DoesNotExist:
        traceback.print_exc()
        codeRes=2
    
    except Exception as e :
        traceback.print_exc()
        codeRes=3
      
    return codeRes

def MoteleObjDirectory(MoteleObj):
    dir = None
    if Directory.objects.filter(name="构件状态",islock=True).count()>0:
        parentdir = Directory.objects.get(name="构件状态",islock=True)
        if Directory.objects.filter(name=MoteleObj.qrcode,parent=parentdir).count()>0:
            dir = Directory.objects.filter(name=MoteleObj.qrcode,parent=parentdir)[0]
        else:
            dir = Directory.objects.create(name=MoteleObj.qrcode,parent=parentdir,creator_id=1,islock=True)
    return dir

def MoteleObjDoc2Relate(relatetype,relateid,user,doc,MoteleObj):
    if MoteleObj.typetable == u"构件" or MoteleObj.typetable == u"安全设施":
        Doc2Relate.objects.create(relatetype=relatetype, relateid=relateid, creator_id=user.id, document_id=doc.id, createtime=datetime.datetime.now())
    elif MoteleObj.typetable == u"构件组":
        pblist = [each.pb for each in Pbgrouprelation.objects.filter(pbgroup_id=MoteleObj.relatedid)]
        if len(pblist)>0:
            stat = pblist[0].curstatus
        statusRecordList = PBStatusRecord.objects.filter(status= stat,precastbeam__in=pblist,isactive=True).values_list('id', flat=True)
        docrelate_list_to_insert = []
        for each in statusRecordList:
            docrelate_list_to_insert.append(Doc2Relate(relatetype=relatetype, relateid=each, creator_id=user.id, 
                                            document_id=doc.id, createtime=datetime.datetime.now()))
        Doc2Relate.objects.bulk_create(docrelate_list_to_insert)
    elif MoteleObj.typetable == u"施工机械":
        pass
    elif MoteleObj.typetable == u"任务":
        pass
    else:
        pass

def uploadfile_weixinstatus(mediaList, name, doctype, relatetype, user, relateid ,MoteleObj):
    try:
        codeRes=0
        userid = user.id
        path=settings.UPLOAD_DIR

        if not os.path.exists(path):
            os.makedirs(path)
            
        tgtLink = []
        _, _, tk = fetch_ticket()
        
        for each in mediaList:
            tgtLink.append('https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token=' + tk + '&media_id=' + each)

        dir = MoteleObjDirectory(MoteleObj)

        index = 1   
        for each in tgtLink:
            try:
                f = urllib2.urlopen(each) 
                data = f.read() 
                
                fn = time.strftime('%Y%m%d%H%M%S')
                fn = "_" + fn + '_%d' % index
                index = index + 1
                
                filename = str(name) + fn + ".jpg"
                full_file_name = path + filename
#                sys.stderr.write(full_file_name.encode('utf-8'))

                with open(full_file_name, "wb") as code:     
                    code.write(data)
                doc = Document()
                doc.name = filename
                doc.shortname = filename
                doc.filepath = path
                doc.doctype= doctype
                doc.creator_id=userid
                doc.createtime=datetime.datetime.now()
                doc.filesize = f.headers['content-length']
                doc.filetype = f.headers['content-type']
                doc.save()   
        
                MoteleObjDoc2Relate(relatetype, relateid, user, doc, MoteleObj)

                if dir:
                    doc.docdirectory.add(dir)
                    movefiletoDir(doc,dir)
            except Exception as e:
                traceback.print_exc()
                codeRes=1
            
    except PrecastBeam.DoesNotExist:
        traceback.print_exc()
        codeRes=2
    
    except Exception as e :
        traceback.print_exc()
        codeRes=3
      
    return codeRes

def fetchVoice_weixin(mediaList, name, doctype, relatetype, user, relateid,relateObj=None  ):
    try:
        codeRes=0
        userid = user.id
        path=settings.UPLOAD_DIR

        if not os.path.exists(path):
            os.makedirs(path)
            
        tgtLink = []
        _, _, tk = fetch_ticket()
        
        for each in mediaList:
            tgtLink.append('https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token=' + tk + '&media_id=' + each)
          
        dir = getTypeDirectory(doctype,relateObj) 

        index=1
        for each in tgtLink:
            try:
                f = urllib2.urlopen(each) 
                data = f.read() 
                flag =time.strftime('%Y%m%d%H%M%S')
                fn = "_%d_%s_%d"%(relateid,flag,index)
                index +=1

                filename = str(name) + fn + ".mp3"
                uuid_file_name = str(uuid1())

                full_file_name = path + uuid_file_name + ".amr"
                
                with open(full_file_name, "wb") as code:     
                    code.write(data)
                converToMP3(full_file_name)
                
                doc = Document()
                doc.name = uuid_file_name + ".mp3"
                doc.shortname = filename
                doc.filepath = path
                doc.doctype= doctype
                doc.creator_id=userid
                doc.createtime=datetime.datetime.now()
                doc.filesize = f.headers['content-length']
                doc.filetype = f.headers['content-type'].replace("amr","mp3")
                doc.save()   
                
                Doc2Relate.objects.create(relatetype=relatetype, relateid=relateid, creator_id=userid, document_id=doc.id, createtime=datetime.datetime.now())
                
                if dir:
                    doc.docdirectory.add(dir)
                    movefiletoDir(doc,dir)
                
            except Exception as e:
                traceback.print_exc()
                codeRes=1
            
    except PrecastBeam.DoesNotExist:
        traceback.print_exc()
        codeRes=2
    
    except Exception as e :
        traceback.print_exc()
        codeRes=3
      
    return codeRes

def converToMP3(fileFullPath,tgtPath=""):
    try:
        import subprocess, traceback
        if tgtPath == "":
            subprocess.call(["sox",fileFullPath,fileFullPath.replace(".amr",".mp3")])
        else:
            subprocess.call(["sox",fileFullPath,fileFullPath])
    except:
        traceback.print_exc()
        return False
    return True   
    
def translateWeather(str):
    skyconsName= ""
    
    if "云" in str or "风" in str:
        skyconsName = "PARTLY_CLOUDY_DAY"
    
    elif "晴" in str:
        skyconsName = "CLEAR_DAY"
        
    elif "大雨" in str or "暴雨" in str:
        skyconsName = "SLEET"
        
    elif "小雨" in str:
        skyconsName = "RAIN"
    elif "雨" in str:
        skyconsName = "SLEET"
       
    elif "雪" in str:
        skyconsName = "SNOW"
    
    else:
        skyconsName = "CLEAR_DAY"
        
    
    return skyconsName

def fetchWeather(index=5):
    weatherList = []
    try:
        #暂时注释掉，修改为直接在客户端获取 pgb
        # url = "http://api.k780.com/?app=weather.future&weaid=45&appkey=25189&sign=4ec9d0f8b383507c3e6e7054302d9ea6&format=json"
        # req=urllib2.Request(url)  
        # resp = urllib2.urlopen(req)
        # weatherInfomation = resp.read()
        # obj = json.loads(weatherInfomation)
        # #print obj
        # for each in obj["result"]:
        #     paraDic = {}
            
        #     paraDic["date"] = each["days"]
        #     paraDic["weather"] = translateWeather(each["weather"]) 
        #     paraDic["temp"] = each["temperature"]
            
        #     if index == 0:
        #         paraDic["weather"] = each["weather"]
        #         return paraDic
            
        #     weatherList.append(paraDic) 
        pass
    except Exception as e:
        return []
        
    return weatherList

def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if(n<0):
        n = abs(n)
        return datetime.date.today()-datetime.timedelta(days=n)
    else:
        return datetime.date.today()+datetime.timedelta(days=n)
    
def get_date_of_day(date,n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if(n<0):
        n = abs(n)
        return date-datetime.timedelta(days=n)
    else:
        return date+datetime.timedelta(days=n)

def add_months(dt,months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = calendar.monthrange(year,month)[1]
    return dt.replace(year=year, month=month, day=day)

def del_months(dt,months):
    month = dt.month - 1 - months-12
    
    year = dt.year - (-month) / 12
    if month==-12:
        year = dt.year
    
    month = month % 12 + 1
    day = calendar.monthrange(year,month)[1]
    return dt.replace(year=year, month=month, day=day)

def calDate(cur, previous):
    if cur.month > previous:
        tgtYear = cur.year
        tgtMon = cur.month - previous
    else:
        tgtYear = cur.year - 1
        tgtMon = cur.month + 12 - previous
        
    tgtDay = calendar.monthrange(tgtYear, tgtMon)[1]
    tgtStart = datetime.date(tgtYear, tgtMon, 1)
    tgtEnd = datetime.date(tgtYear, tgtMon, tgtDay)
    
    return tgtStart, tgtEnd

def fetchWeatherStat(monthNum=1):
    weatherStat = []
    dateToday = datetime.date.today()
    for each in xrange(monthNum):
        statIns = {}
        statIns["qing"], statIns["xiaoyu"], statIns["yuxue"]= 0, 0, 0
        tgtDateStart, tgtDateEnd = calDate(dateToday, each)
        
        objList = Weather.objects.filter(created__gte=tgtDateStart,created__lte=tgtDateEnd)
        for each in objList:
            weaIns = translateWeather(each.weather)
            if weaIns == 'PARTLY_CLOUDY_DAY' or weaIns == 'CLEAR_DAY':
                statIns["qing"] += 1
            elif weaIns == 'RAIN' :
                statIns["xiaoyu"] += 1
            elif weaIns == 'SLEET' or weaIns == 'SNOW':
                statIns["yuxue"] += 1

        statIns[tgtDateStart] = statIns
        weatherStat.append(statIns)
        
        if monthNum==1:
            return statIns[tgtDateStart]
        
    return weatherStat   

def checkLocate(proAddress):
    if "上海" in proAddress:
        city='上海'
    elif "广州" in proAddress:
        city='广州'
    else:
        city='其他'
        
    if "长宁" in proAddress:
        area='长宁'
    elif "嘉定" in proAddress:
        area='嘉定'
    elif "静安" in proAddress:
        area='静安'
    else:
        area='其他'
        
    return city+"."+area
          
def GetRelateTypeInfo(type,typeId):
    info=u"无相关信息"
    try:
        if type == u"构件":
            pb = PrecastBeam.objects.get(id=typeId)
            info = u"构件:"+pb.drawnumber
        elif type == u"任务":
            task = ProjectTask.objects.get(id=typeId)
            info = u"任务:"+task.name
        elif type==u"安全设施":
            pb = PrecastBeam.objects.get(id=typeId)
            info = u"安全设施:"+pb.drawnumber
        elif type == u"单位工程":
            info=UnitProject.objects.get(id=typeId).name
        elif type == u"楼层":
            lc = Elevation.objects.get(id=typeId)
            info = UnitProject.objects.get(id=lc.unitproject_id).name + lc.name + u'层'
        elif type == u"分区":
            info = Zone.objects.get(id=typeId).name
        elif type == u"构件组":
            info = Pbgroup.objects.get(id=typeId).name
        elif type == u"危险源":
            ha = Hazardevent.objects.get(id=typeId)
            kha = KnowledgeHazardlist.objects.get(hazard_code=ha.hazard_code)
            info = u"危险源:"+kha.hazard_name
        elif type == u"专业":
            major = UserMajor.objects.get(id=typeId)
            info = u"专业:"+major.name
        elif type == u"构件类型":
            pb = PBType.objects.get(id=typeId)
            info = u"构件类型:"+pb.name
        elif type == u"施工机械":
            info=u"无相关信息"
        elif type == u"流程步骤":
            info=u"无相关信息"
        elif type == u"重大危险源修改记录":
            info=u"无相关信息"
        elif type == u"施工机械状态修改记录":
            info=u"无相关信息"
        elif type == u"构件状态修改记录":
            info=u"无相关信息"
        elif type == u"任务状态修改记录":
            info=u"无相关信息"
        else:
            info=u"无相关信息"
    except:
            pass
    return info        

def updateStepQueue(templateid,):
    pass

        


def GetDateRange(timerange):
    startdate=datetime.datetime.strptime(timerange.split('-')[0].strip()+" 00:00:00",'%Y/%m/%d %H:%M:%S')
    enddate=datetime.datetime.strptime(timerange.split('-')[1].strip()+" 23:59:59",'%Y/%m/%d %H:%M:%S')  
    return  startdate,enddate

def GetDateRange2(timerange):
    startdate=datetime.datetime.strptime(timerange.split('-')[0].strip(),'%Y/%m/%d')
    enddate=datetime.datetime.strptime(timerange.split('-')[1].strip(),'%Y/%m/%d')  
    return  startdate,enddate

def GetDateRangeArray(timerange):
    startdate=datetime.datetime.strptime(timerange[0].strip()+" 00:00:00",'%Y/%m/%d %H:%M:%S')
    enddate=datetime.datetime.strptime(timerange[1].strip()+" 23:59:59",'%Y/%m/%d %H:%M:%S')  
    return  startdate,enddate

def getweekdayofdate(inDate,weekindex):
    n = datetime.datetime.weekday(inDate)

    outDate=inDate + datetime.timedelta(0-n+weekindex)
        
    return outDate

def getUserMajor(user):
    major = user.major_id
    if major in [11,16,18,19]:
        major=1
    return major

def getOtherUserlist():
    prjMemberlist = UserRoles.objects.all().values_list("user_id", flat=True).distinct()
    memberList = User.objects.exclude(id__in=list(prjMemberlist))
    return memberList

def getPrjUserlist():
    prjMemberlist = UserRoles.objects.all().values_list("user_id", flat=True).distinct()
    memberList = User.objects.filter(id__in=list(prjMemberlist)).extra(select={'new_true_name': 'CONVERT(truename USING gbk)'}).extra(order_by = ['new_true_name'])
    return memberList

def getTitleFromUrl(request,url,defaulttitle=''):
    title=defaulttitle
    if checkMobile(request):
        if ProjectmenuMobile.objects.filter(url=url,parent_id__isnull=False).count()>0:
            title = ProjectmenuMobile.objects.filter(url=url,parent_id__isnull=False)[0].name
        elif ProjectmenuMobile.objects.filter(url=url).count()>0:
            title = ProjectmenuMobile.objects.filter(url=url)[0].name
    else:
        if Projectmenu.objects.filter(url=url,parent_id__isnull=False).count()>0:
            title = Projectmenu.objects.filter(url=url,parent_id__isnull=False)[0].name
        elif Projectmenu.objects.filter(url=url).count()>0:
            title = Projectmenu.objects.filter(url=url)[0].name
    return title

def checkMonitorType():
    setele = set(Monitoringelement.objects.filter(typetable="构件").values_list('relatedid', flat=True))
    setsheshi = set(PrecastBeam.objects.filter(pbtype__major_id=17).values_list('id', flat=True))

    havesheshi = True if len(setele&setsheshi)>0 else False
    havejixie = True if Monitoringelement.objects.filter(typetable="施工机械").count()>0 else False
    haverenwu = True if Monitoringelement.objects.filter(typetable="任务").count()>0 else False

    return havesheshi,havejixie,haverenwu

def filterMonitorType(list_items,type):
    setpbgrp =([each.relatedid for each in Monitoringelement.objects.filter(typetable=type)])
    listtmp=[]
    for each in list_items:
        if each.id in setpbgrp:
            listtmp.append(each)

    return listtmp

def getMajorList():
    majorlist = PBType.objects.values('major_id').distinct().values_list('major_id', flat=True)
    return UserMajor.objects.filter(id__in=list(majorlist))

def getWeekDateRange(index=0):
    weekday=0
    try:
        weekday=int(CustomInfo.objects.get(infotype="weekly_index").custominfo)
    except:
        pass

    curdate = datetime.date.today()
    weekly_begindate = getweekdayofdate(curdate ,0+(index*7))
    weekly_enddate = getweekdayofdate(curdate ,6+(index*7))
    
    weekly_begindate=datetime.datetime.strptime(weekly_begindate.strftime("%Y/%m/%d")+" 00:00:00",'%Y/%m/%d %H:%M:%S')
    weekly_enddate=datetime.datetime.strptime(weekly_enddate.strftime("%Y/%m/%d")+" 23:59:59",'%Y/%m/%d %H:%M:%S')  
    return weekly_begindate,weekly_enddate

def TransRelateInfo(type,info):
    relatetype = type
    relateid = info
    if type=="空间":
        RelateInfo = info.split('_')
        relatetype = RelateInfo[0]
        relateid = RelateInfo[1]
        if relatetype == 'unitprj':
            relatetype = u'单位工程'
        elif relatetype == 'floor':
            relatetype = u'楼层'
        elif 'zone' in relatetype:
            relatetype = u'分区'

    return relatetype,relateid

