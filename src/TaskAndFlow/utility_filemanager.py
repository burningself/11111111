# -*- coding: utf-8 -*-
#import logging
#logging.basicConfig(filename='/www/log/myapp.log',filemode='w')
import os,time,random, sys, datetime, calendar, traceback,zipfile
import shutil
import memcache
import urllib2,json
from Scc4PM import settings
from TaskAndFlow.models import *
from django.db.models import Q
from uuid import uuid1
from thread import *
import socket   #for sockets
import urllib
import base64

def getdirtree(basedir):
    treelist = ""
    if Directory.objects.filter(id=basedir).count()>0:
        treedir = Directory.objects.filter(id=basedir)[0]
        treelist=treedir.name+"/"
        while treedir.parent:
            treedir = Directory.objects.get(id=treedir.parent.id)
            treelist = treedir.name + "/" + treelist
        treelist = "/"+treelist
    return treelist

def makevirtualdir_p(parentdir,dirs,user):
    pdir = Directory.objects.get(id=parentdir)
    for each in dirs.split('/'):
        try:
            if Directory.objects.filter(parent=pdir,name=each).count()>0:
                pdir = Directory.objects.filter(parent=pdir,name=each)[0]
            else:
                pdir = Directory.objects.create(name=each,parent=pdir,creator=user)
        except:
            traceback.print_exc()
            break
    return pdir

def mkdir_p(basepath,newpath):
    rootpath=settings.UPLOAD_DIR[:-1]
    path = rootpath+basepath+newpath
    try:
        os.makedirs(path)
    except:
        traceback.print_exc()

    return path

def movefilefromroot(newpath,filename):
    rootpath=settings.UPLOAD_DIR
    try:
        shutil.move(rootpath+filename, newpath+filename)
    except:
        traceback.print_exc()

    return newpath

def getfilerealname(filename):
    realname = filename
    try:
        if "_" in filename:
            realname = filename.split("_")[0]+"."+filename.split(".")[-1]
    except:
        traceback.print_exc()
    return realname

def getfiletype(fileinfo):
    filetype = fileinfo.content_type
    try:
        print filetype
        if filetype=="application/octet-stream":
            ext = os.path.splitext(fileinfo.name)[1]
            if ext.upper()==".exe".upper():
                filetype="application/exe"
            elif ext.upper()==".dwg".upper():
                filetype="application/dwg"
            elif ext.upper()==".mpp".upper():
                filetype="application/mpp"
            elif ext.upper()==".rvt".upper():
                filetype="application/rvt"
            elif ext.upper()==".rfa".upper():
                filetype="application/rfa"
            elif ext.upper()==".nwc".upper():
                filetype="application/nwc"
    except:
        traceback.print_exc()
    return filetype

#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
  zipf = zipfile.ZipFile(output_filename, 'w')
  pre_len = len(os.path.dirname(source_dir))
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
      zipf.write(pathfile, arcname)
  zipf.close()

def movefiletoDir(doc,acdir):
    try:
        relatepath = ''
        basepath = getdirtree(acdir.id)
        newpath = mkdir_p(basepath, relatepath)
        print newpath
        movefilefromroot(newpath,doc.name)
        doc.filepath = u"upload"+basepath+relatepath
        doc.save()
    except:
        traceback.print_exc()
        pass

def getNotifyUserList(uploaddir):
    notifyuserlist = []
    try:   
        notifyuserlist=[each.notifyuser for each in DirectoryNotifyuser.objects.filter(directory_id=uploaddir)]
        if len(notifyuserlist)==0:
            treedir = Directory.objects.filter(id=uploaddir)[0]
            while treedir.parent:
                notifyuserlist=[each.notifyuser for each in DirectoryNotifyuser.objects.filter(directory_id=treedir.parent_id)]
                if len(notifyuserlist)>0:
                    break
                treedir = Directory.objects.get(id=treedir.parent.id)
    except:
        traceback.print_exc()
        pass
    return notifyuserlist

def getDirAuth(dir,user):
    auth=7
    try:   
        if(DirectoryUser.objects.filter(directory=dir,user=user).count()>0):
            auth=DirectoryUser.objects.filter(directory=dir,user=user)[0].auth
            return auth
        else:
            treedir = dir
            while treedir.parent:
                if(DirectoryUser.objects.filter(directory=treedir.parent,user=user).count()>0):
                    auth=DirectoryUser.objects.filter(directory=treedir.parent,user=user)[0].auth
                    return auth
                treedir = Directory.objects.get(id=treedir.parent.id)
    except:
        traceback.print_exc()
        pass
    
        
    return auth

def createFileNotify(oprdir,opruser,newfilelist,updatefilelist,deletefilelist):
     #发送文件通知
    notifyuserlist = getNotifyUserList(oprdir)
    message = ''
    if notifyuserlist:
        if updatefilelist:
            message+=u"更新了文件"
            for doc in updatefilelist:
                message=message+u"《"+doc.shortname+u"》,"
            message = message[:-1]
            message+=";"
        if newfilelist:
            message+="新增了文件"
            for doc in newfilelist:
                message=message+u"《"+doc.shortname+u"》,"
            message = message[:-1]
            message+=";"
        if deletefilelist:
            message+="删除了文件"
            for doc in deletefilelist:
                message=message+u"《"+doc.shortname+u"》,"
            message = message[:-1]
            message+=";"

    print message
    pushmsgList = []
    dir = Directory.objects.get(id=oprdir)
    if opruser.userdivisions.all():
        fromname = opruser.userdivisions.all()[0].division.name
    else:
        fromname = opruser.company.name
    title = ("%s更新了%s") % (fromname,dir.name)
    for each in notifyuserlist:
        pushmsgList.append(PushMessage(status=0, title=title,relatetype="文件夹通知", relateid=oprdir,
                        agentid= Project.objects.get(id=settings.CURRENT_PROJECT_ID).appid,
                        fromuser_id=opruser.id, touser_id=each.id, message=message))

    PushMessage.objects.bulk_create(pushmsgList)

def transdwg2ocfthread(request,doc):
    try:
        port = 9999
        #remote_ip = "127.0.0.1"
        remote_ip = "139.196.166.127";
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((remote_ip , port))
        
        fileurl = urllib.quote_plus((u"http://%s/%s/%s" % (request.get_host(),str(doc.filepath),doc.name)).encode('utf8'))
        task = {
        'fileurl':fileurl,
        'host':request.get_host(),
        'fileid':doc.id
        }
        task =  base64.b64encode(json.dumps(task))
    
        s.sendall(task)
         
        reply = s.recv(4096)
        print reply     
             
        s.close()
        
        
    except Exception, e:
        traceback.print_exc()
        print  '%s' % e

def transdwg2ocf(request,doc):
    start_new_thread(transdwg2ocfthread ,(request,doc))


def transdwg2ocfdiarythread(host,doc):
    try:
        port = 9999
        #remote_ip = "127.0.0.1"
        remote_ip = "139.196.166.127";
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((remote_ip , port))

        fileurl = urllib.quote_plus((u"%s/%s/%s" % (host,str(doc.filepath),doc.name)).encode('utf8'))
        task = {
        'fileurl':fileurl,
        'host':'/'.join(host.split("/")[2:]),
        'fileid':doc.id
        }
        task =  base64.b64encode(json.dumps(task))
    
        s.sendall(task)
         
        reply = s.recv(4096)
        print reply     
             
        s.close()
        
        
    except Exception, e:
        traceback.print_exc()
        print  '%s' % e

def transdwg2ocfdiary():
    host = Project.objects.get(id=settings.CURRENT_PROJECT_ID).projecturl
    print host
    doclist = Document.objects.filter(filetype='application/dwg',previewfile__isnull=True)
    for doc in doclist:
        start_new_thread(transdwg2ocfdiarythread,(host,doc))