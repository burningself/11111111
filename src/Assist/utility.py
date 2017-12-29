# -*- coding: utf-8 -*-

import pdfkit
from django.conf import settings
from TaskAndFlow.models import *
from TaskAndFlow.utility import *
from uuid import uuid1
import os,traceback
import os.path
from pyPdf import PdfFileReader,PdfFileWriter
from Scc4PM import settings
from TaskAndFlow.utility_filemanager import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def Form2File(formtype,content,user,customname="",relateddate=None):
	retCode = "suc"
	filepath = settings.UPLOAD_DIR
	if not os.path.exists(filepath):
		os.makedirs(filepath)
	
	filename = None
	file_ext = ".pdf"
	file_type = "application/pdf"
	
	attachHtml = '<head><meta charset="UTF-8"></head><style>table{border:1px solid #000;border-collapse: collapse} table td{border:1px solid #000;}</style>'

	doc = None
	dir = None

	try:
		while True:
			if formtype==u"施工日记":
				if relateddate:
					filename = customname+file_ext
					if len(Directory.objects.filter(name=formtype,islock=True))>0:
						dir = Directory.objects.filter(name=formtype,islock=True)[0]
			elif formtype=="质量整改单":
				pase
			else:
				retCode = u"未知表单类型"
				break

			if 	not filename:
				retCode = u"生成文件名失败"
				break

			if not dir:
				retCode = u"没有对应归档目录"
				break

			filenamewithpaht = filepath+filename
			content = attachHtml+content

			uuid_file_name=str(uuid1())+file_ext
			tmp_file_name = filepath+uuid_file_name
			pdfkit.from_string(content, tmp_file_name) # file_name中文会乱码，所以通过英文名来中转 pgb
			# if os.path.exists(filenamewithpaht):
			# 	os.remove()
			# os.rename(tmp_file_name, filenamewithpaht)


			doc = Document()
			doc.name = uuid_file_name
			doc.shortname = filename
			doc.filepath = u"upload/"
			doc.creator=user
			doc.filesize = len(content)
			doc.filetype = file_type
			doc.doctype='normal'
			doc.save()
			
			if dir:
				doc.docdirectory.add(dir)
				movefiletoDir(doc,dir)

			break
	except Exception, e:
		traceback.print_exc()
		retCode = '%s' % e
		print e

	return retCode,doc

def Form2FileEvent(proeventObj):
	retCode = "suc"
	filepath = settings.UPLOAD_DIR
	if not os.path.exists(filepath):
		os.makedirs(filepath)
	
	filename = None
	file_ext = ".pdf"
	file_type = "application/pdf"
	
	attachHtml = '<head><meta charset="UTF-8"></head><style>table{border:1px solid #000;border-collapse: collapse} table td{border:1px solid #000;}</style>'

	doc = None
	acdir = None

	user = User.objects.get(id=1)
	eventNum = proeventObj.number

	acdir = getTypeDirectory('quality',proeventObj)
	print "11111111111111111111111111111"
	print acdir

	curEventsteplist = Eventstep.objects.filter(projectevent=proeventObj)

	for EventStepObj in curEventsteplist:
		if EventStepObj.relatedform:
			try:
				filename = eventNum+"_"+EventStepObj.relatedform.name+file_ext

				filenamewithpaht = filepath+filename
				content = attachHtml+EventStepObj.relatedform.content

				tmp_file_name = filepath+str(uuid1())
				pdfkit.from_string(content, tmp_file_name) # file_name中文会乱码，所以通过英文名来中转 pgb
				os.rename(tmp_file_name, filenamewithpaht)

				doc = Document()
				doc.name = filename
				doc.shortname = filename
				doc.filepath = u"upload/"
				doc.creator=user
				doc.filesize = len(content)
				doc.filetype = file_type
				doc.doctype='normal'
				doc.save()
				
				EventStepObj.formfile=doc
				if acdir:
					doc.docdirectory.add(acdir)
					movefiletoDir(doc,acdir)

			except Exception, e:
				retCode = '%s' % e
				print e

	return retCode,acdir

def Form2FileAcceptance(accObj):
	retCode = "suc"
	filepath = settings.UPLOAD_DIR
	if not os.path.exists(filepath):
		os.makedirs(filepath)
	
	filename = None
	file_ext = ".pdf"
	file_type = "application/pdf"
	
	attachHtml = '<head><meta charset="UTF-8"></head><style>table{border:1px solid #000;border-collapse: collapse} table td{border:1px solid #000;}</style>'

	doc = None
	acdir = None

	user = User.objects.get(id=1)

	if len(Directory.objects.filter(name='质量验收',islock=True))>0:
		acdir = Directory.objects.filter(name='质量验收',islock=True)[0]
	else:
		retCode = u"获取归档目录失败"
		return retCode,acdir

	formlist = AcceptanceinfoForm.objects.filter(acceptanceinfo=accObj)

	for each in formlist:
		if each.form:
			try:
				filename = each.form.name + str(each.id)+file_ext

				filenamewithpaht = filepath+filename
				content = attachHtml+each.form.content

				tmp_file_name = filepath+str(uuid1())
				pdfkit.from_string(content, tmp_file_name) # file_name中文会乱码，所以通过英文名来中转 pgb
				os.rename(tmp_file_name, filenamewithpaht)

				doc = Document()
				doc.name = filename
				doc.shortname = filename
				doc.filepath = u"upload/"
				doc.creator=user
				doc.filesize = len(content)
				doc.filetype = file_type
				doc.doctype='normal'
				doc.save()
				
				each.formfile=doc
				if acdir:
					doc.docdirectory.add(acdir)
					movefiletoDir(doc,acdir)

			except Exception, e:
				retCode = '%s' % e
				print e

	return retCode,acdir

def getToDoEeventColor(type):
	if type=="公告":
		color='#257e4a'
	elif type=="整改单":
		color='#FF0000'
	elif type=="提醒":
		color='#FF7400'
	elif type=="例会":
		color='#3016B0'
	else:
		color='#009999'
	return color



def get_week_day(date):
  week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期天',
  }
  day = date.weekday()
  return week_day_dict[day]


def setZhouqiMeeting(eachdate,meetingmodel):
    tempobj = {}
    tempobj['mid'] = meetingmodel.id
    tempobj['meetingtype'] = meetingmodel.meetingtype_id
    tempobj['meetingtypename'] = meetingmodel.meetingtype.name
    tempobj['roomname'] = meetingmodel.roomname
    tempobj['title'] = meetingmodel.name
    tempobj['start'] = str(eachdate)+' '+meetingmodel.begin_time+':00'
    tempobj['end'] = str(eachdate)+' '+meetingmodel.end_time+':00'
    tempobj['huiyitype'] = 1
    tempobj['canupdate'] = 0
    tempobj['contant'] = meetingmodel.description
    return tempobj

class MergePDF():
	def __init__(self):
		self.pdf_name = ""
		self.pdf_list = []

	def Merge(self):
		out = PdfFileWriter()

		for i in range(len(self.pdf_list)):
			src_pdf = self.pdf_list[i]
			if not os.path.exists(src_pdf):
				continue

			pdf = PdfFileReader(file(src_pdf, 'rb'))

			for page in pdf.pages:
				out.addPage(page)

		ous = file(self.pdf_name,'wb')
		out.write(ous)
		ous.close()


def MergeDiaryPdf(diarylist):
	try:
		m = MergePDF()
		filepath = settings.UPLOAD_DIR
		tmp_file_name = str(uuid1())+".pdf"
		m.pdf_name = filepath+tmp_file_name
		for each in diarylist:
			eachpath = filepath + '/'.join(str(each.file.filepath).split('/')[1:])
			m.pdf_list.append(eachpath+each.file.name)
		m.Merge()
	except:
		traceback.print_exc()
		return ""
	return tmp_file_name

def canEditMeeting(user,meeting):
	if user==meeting.hostuser or user.has_perm("编辑会议"):
		return True
	else:
		return False
	return False


def zhouqiHuiyiCreate():
    #周期会议
    curdate = datetime.date.today()
    createdate = curdate +datetime.timedelta(days = 1)#从第二天开始
    zhouqilist = MeetingZhouqi.objects.all()
    for meetingmodel in zhouqilist:
        if meetingmodel.zhouqitype==1:#日会议
            createhuiyiFromZhouqi(createdate,meetingmodel)
        elif meetingmodel.zhouqitype==2:#周会议
            weekday =get_week_day(createdate)
            weeklist = meetingmodel.create_time.split(',')
            if weekday in weeklist:
                createhuiyiFromZhouqi(createdate,meetingmodel)
        elif meetingmodel.zhouqitype==3:#月会议
            monthday = "%02d" % createdate.day
            if monthday in meetingmodel.create_time.split(','):
                createhuiyiFromZhouqi(createdate,meetingmodel)


def createhuiyiFromZhouqi(createdate,hyobj):
    meetname = hyobj.name
    meetingtype_id = hyobj.meetingtype_id
    meetroom = hyobj.roomname
    hyzt = hyobj.description
    hostuser_id = hyobj.hostuser_id
    begin_time = str(createdate)+' '+str(hyobj.begin_time)+':00'
    end_time = str(createdate)+' '+str(hyobj.end_time)+':00'
    mettingmodel = Meeting.objects.create(hostuser_id=hostuser_id,name=meetname,description=hyzt,meetingtype_id=meetingtype_id,begin_time=datetime.datetime.strptime(begin_time,'%Y-%m-%d %H:%M:%S'),end_time=datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S'),roomname=meetroom)

    #获取参会人员列表
    meetingusers = MeetingZhouqiUser.objects.filter(meeting_id=hyobj.id)

    queryList = []
    for mid in meetingusers:
        queryList.append(MeetingUser(user_id=mid.user_id,meeting_id=mettingmodel.id))
     
    MeetingUser.objects.bulk_create(queryList)
       

    #获取文件列表
    docs = MeetingZhouqirelatedfile.objects.filter(meeting_id=hyobj.id)
    if len(docs)>0:
        destdir=getTypeDirectory('meeting',mettingmodel)
        doclist = []
        for docid in docs:
            if Document.objects.filter(id=docid.file_id).count()==1:
                tar = Document.objects.get(id=docid.file_id)
                if destdir:
                    tar.docdirectory.add(destdir)
                    movefiletoDir(tar,destdir)
            else:
                raise Exception(u'文件不存在！')
            doclist.append(Meetingrelatedfile(meeting_id=mettingmodel.id,file_id=docid.file_id))
        Meetingrelatedfile.objects.bulk_create(doclist)

    #创建推送消息
    AddNewMeetingMsg(mettingmodel, "会议")


def AddNewMeetingMsg(meetingObj,msgType):
    pushmsgList = []
    curPrj = Project.objects.get(id=CURRENT_PROJECT_ID)
    meetingUsers = MeetingUser.objects.filter(meeting=meetingObj)
    if msgType=="会议":
        for each in meetingUsers:
            pushmsgList.append(PushMessage(status=0, relatetype=msgType, relateid=meetingObj.id,
                                        agentid= curPrj.appid,fromuser_id=meetingObj.hostuser_id, touser_id=each.user_id, message=meetingObj.name))

            #大于2小时候的话，则推送会议开始1小时提醒
            if (meetingObj.begin_time-datetime.datetime.now()).days>=0 and (meetingObj.begin_time-datetime.datetime.now()).seconds>60*60*2:
                pushtime = meetingObj.begin_time+datetime.timedelta(hours=-1)
                pushmsgList.append(PushMessage(status=0, relatetype="会议即将开始", relateid=meetingObj.id,
                                        agentid= Project.objects.get(id=CURRENT_PROJECT_ID).appid,
                                        fromuser_id=meetingObj.hostuser_id, touser_id=each.user_id, message=meetingObj.name,pushtime=pushtime))
    else:
        pass

    PushMessage.objects.bulk_create(pushmsgList)

