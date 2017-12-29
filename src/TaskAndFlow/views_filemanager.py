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
from UserAndPrj.models import *
from TaskAndFlow.models import *
from Assist.commonUtil import *
from TaskAndFlow.utility_filemanager import *
from TaskAndFlow.connector import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q,F
from django.core import serializers
from _mysql import NULL
from uuid import uuid1
from Scc4PM import settings
from dss.Serializer import serializer as objtojson
from django.views.decorators.clickjacking import xframe_options_exempt
# Create your views here.

@xframe_options_exempt
@login_required(login_url="/login/")
def ziliao_list(request):
    title="资料管理"
    issuetypeList = FlowType.objects.all()
    majorList = UserMajor.objects.all()
    return render_to_response('TaskAndFlow/filemanager/filemanager.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
def ziliao_filemanager_mobile(request):
    return render_to_response('TaskAndFlow/filemanager/filemanager_mobile.html', RequestContext(request,locals()))


@login_required(login_url="/login/")
def connector_view(request):
    """ Handles requests for the elFinder connector.
    """

    finder = ElFinderConnector()
    finder.run(request)

    # Some commands (e.g. read file) will return a Django View - if it
    # is set, return it directly instead of building a response
    if finder.return_view:
        return finder.return_view

    response = HttpResponse(content_type=finder.httpHeader['Content-type'])
    response.status_code = finder.httpStatusCode
    if finder.httpHeader['Content-type'] == 'application/json':
        response.content = json.dumps(finder.httpResponse)
    else:
        response.content = finder.httpResponse

    return response

@login_required(login_url="/login/")
@csrf_exempt
def connector_view_upload(request):
    """ Handles requests for the elFinder connector.
    """
    finder = ElFinderConnector()
    finder.run(request)

    # Some commands (e.g. read file) will return a Django View - if it
    # is set, return it directly instead of building a response
    if finder.return_view:
        return finder.return_view

    response = HttpResponse(content_type=finder.httpHeader['Content-type'])
    response.status_code = finder.httpStatusCode
    if finder.httpHeader['Content-type'] == 'application/json':
        response.content = json.dumps(finder.httpResponse)
    else:
        response.content = finder.httpResponse

    return response

@csrf_exempt
@login_required(login_url="/login/")
def ziliao_uploadview(request):
    if request.method == 'GET':
        try:
            uploaddir=request.GET.get('uploaddir', None)
            if not uploaddir:
                uploaddir = Directory.objects.filter(parent_id__isnull=True)[0].id
            treelist = getdirtree(uploaddir)
        except Exception, e:
            traceback.print_exc()
            print e
        majorList=getMajorList()
        curMajorId = getUserMajor(request.user)
        return render_to_response('TaskAndFlow/filemanager/uploadview.html', RequestContext(request,locals()))
    elif request.method == 'POST':
        response_data={}
        response_data["issuc"]="false"
        try:
            uploaddir=request.POST.get('uploaddir', 1)
            docs = eval(request.POST.get('docs', '[]'))
            selectedGJs = eval(request.POST.get('selectedGJs', '[]'))  # 关联元素
            docsRelatedir = eval(request.POST.get('docsRelatedir', '{}'))
            remark=request.POST.get('remark', '')
            print docsRelatedir
            print docs
            print remark

            basepath = getdirtree(uploaddir)
            savedir = Directory.objects.get(id=uploaddir)

            Doc2Relate_list_to_insert = []

            
            updatefilelist = []
            newfilelist = []
            for FileId in docs:
                docId = int(FileId)
                for ys in selectedGJs:
                    if ys["typetable"]=='空间结构':
                        kjys = ys["relatedid"].split('_')
                        kjty = kjys[0]
                        kjid = kjys[1]
                        if kjty == 'unitprj':
                            kjty = u'单位工程'
                        elif kjty == 'floor':
                            kjty = u'楼层'
                        elif 'zone' in kjty:
                            kjty = u'分区'
                        Doc2Relate_list_to_insert.append(Doc2Relate(relatetype=kjty, relateid=int(kjid),creator=request.user, document_id=docId))
                    elif ys["typetable"]=='分类信息':
                        kjys = ys["relatedid"].split('_')
                        kjty = kjys[0]
                        kjid = kjys[1]
                        if kjty == 'major':
                            kjty = u'专业'
                        elif kjty == 'type':
                            kjty = u'构件类型'
                        Doc2Relate_list_to_insert.append(Doc2Relate(relatetype=kjty, relateid=int(kjid),creator=request.user, document_id=docId))
                    else:
                        Doc2Relate_list_to_insert.append(Doc2Relate(relatetype=ys["typetable"], relateid=ys["relatedid"],creator=request.user, document_id=docId))

                doc = Document.objects.get(id=docId)
                newdir = savedir
                relatepath=''
                if  docsRelatedir.has_key(str(FileId)):
                    newdir = makevirtualdir_p(uploaddir, docsRelatedir[str(FileId)], request.user)
                    relatepath = docsRelatedir[str(FileId)]+"/"

                newpath = mkdir_p(basepath, relatepath)   
      
                movefilefromroot(newpath,doc.name)
                doc.filepath = u"upload"+basepath+relatepath
                doc.docdirectory.add(newdir)
                doc.remark = remark
                doc.save()

                #更新历史版本
                if Document.objects.filter(shortname=doc.shortname,docdirectory=newdir,version__isnull=True).exclude(id=docId).count()>0:
                    Document.objects.filter(shortname=doc.shortname,docdirectory=newdir,version__isnull=True).exclude(id=docId).update(version=F('createtime'))
                    updatefilelist.append(doc)
                else:
                    newfilelist.append(doc)

                #图纸转换
                if doc.filetype  == "application/dwg":
                    transdwg2ocf(request,doc)

            Doc2Relate.objects.bulk_create(Doc2Relate_list_to_insert)

            #发送文件通知
            createFileNotify(uploaddir,request.user,newfilelist, updatefilelist, None)

            response_data["issuc"]="true"

        except:
            traceback.print_exc()
            response_data["error"] = "保存失败！"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def ziliao_cloudfilerelate(request):
    majorList=UserMajor.objects.all()
    curMajorId = getUserMajor(request.user)
    return render_to_response('TaskAndFlow/filemanager/cloudfilerelate.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
def ziliao_getfiletree(request):
    id=request.GET.get('id', '')

    if id=='#':
        response_data = {}
        child_list=[]
        rootdir = Directory.objects.get(parent__isnull=True)
        response_data["id"]="dir_"+str(rootdir.id)
        response_data["text"]="所有文件"
        response_data["state"]= {'opened':True }

        dirlist = Directory.objects.filter(parent=rootdir)
        for unit in dirlist:
            child_data = {}
            child_data["id"]="dir_"+str(unit.id)
            child_data["text"]=unit.name
            child_data["children"]=True

            child_list.append(child_data)

        filelist = Document.objects.filter(docdirectory=rootdir)
        for unit in filelist:
            child_data = {}
            child_data["id"]="file_"+str(unit.id)
            child_data["text"]=unit.shortname
            child_data["icon"]="/img/file.png"
            child_list.append(child_data)

        response_data["children"]=child_list
    else:
        child_list=[]
        dirId = int(id[4:])
        dirlist = Directory.objects.filter(parent_id=dirId)
        for unit in dirlist:
            child_data = {}
            child_data["id"]="dir_"+str(unit.id)
            child_data["text"]=unit.name
            child_data["children"]=True

            child_list.append(child_data)

        rootdir = Directory.objects.get(id=dirId)
        filelist = Document.objects.filter(docdirectory=rootdir)
        for unit in filelist:
            child_data = {}
            child_data["id"]="file_"+str(unit.id)
            child_data["text"]=unit.shortname
            child_data["icon"]="/img/file.png"
            child_list.append(child_data)

        response_data=child_list

    #print json.dumps(response_data)

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def ziliao_getdirtree(request):
    id=request.GET.get('id', '')

    if id=='#':
        response_data = {}
        child_list=[]
        rootdir = Directory.objects.get(parent__isnull=True)
        response_data["id"]=str(rootdir.id)
        response_data["text"]=rootdir.name
        response_data["state"]= {'opened':True }

        dirlist = Directory.objects.filter(parent=rootdir)
        for unit in dirlist:
            child_data = {}
            child_data["id"]=str(unit.id)
            child_data["text"]=unit.name
            child_data["children"]=True

            child_list.append(child_data)

        response_data["children"]=child_list
    else:
        child_list=[]
        dirId = int(id)
        dirlist = Directory.objects.filter(parent_id=dirId)
        for unit in dirlist:
            child_data = {}
            child_data["id"]=str(unit.id)
            child_data["text"]=unit.name
            child_data["children"]=True

            child_list.append(child_data)

        response_data=child_list

    #print json.dumps(response_data)

    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url="/login/")
def ziliao_anquanjiancha(request):
    return render_to_response('TaskAndFlow/filemanager/anquanjiancha.html', RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/")
def ziliao_checkexist(request):
    response_data = {}
    response_data["issuc"] = 'false' 
    response_data["isexist"] = 'false' 
    try:
        filename=request.GET.get('filename', '')
        uploaddir=request.GET.get('uploaddir', 1)
        docRelatedir = request.GET.get('docRelatedir', '')
        print docRelatedir
        print uploaddir
        filename = getfilerealname(filename)
        if docRelatedir:
            dirtree = getdirtree(uploaddir)
            docRelatedir='/'.join(docRelatedir.split('/')[:-1])
            path = 'upload'+dirtree+docRelatedir+"/"
            print path
            if Document.objects.filter(shortname=filename,filepath=path).count()>0:
                doc = Document.objects.filter(shortname=filename,filepath=path)[0]
                response_data["filename"] = filename
                response_data["version"] = str(doc.version) if doc.version else str(doc.createtime)
                response_data["isexist"] = 'true'
        else:
            if Document.objects.filter(shortname=filename,docdirectory=uploaddir).count()>0:
                doc = Document.objects.filter(shortname=filename,docdirectory=uploaddir)[0]
                response_data["filename"] = filename
                response_data["version"] = str(doc.version) if doc.version else str(doc.createtime)
                response_data["isexist"] = 'true'

        response_data["issuc"] = 'true' 
    except:
        traceback.print_exc()


    return HttpResponse(json.dumps(response_data), content_type="application/json")

 
@login_required(login_url="/login/")
def ziliao_filehisverison(request):
    fileId=int(request.GET.get('fileId', ''))
    doc = Document.objects.get(id=fileId)
    print doc.docdirectory.all()
    list_items=Document.objects.filter(shortname=doc.shortname,docdirectory=doc.docdirectory.all())

    return render_to_response('TaskAndFlow/filemanager/hisversion.html', RequestContext(request,locals()))



@login_required(login_url="/login/")
def ziliao_dirdownload(request):
    response_data = {}
    response_data["issuc"] = 'false' 
    try:
        dirId=request.GET.get('dirId', None)
        dirtree = getdirtree(dirId)

        rootpath=settings.UPLOAD_DIR
        path = rootpath+dirtree
        print path
        tmppath = rootpath+"tmp/"
        print tmppath
        if not os.path.exists(tmppath):
            os.makedirs(tmppath)

        uuid_file_name = str(uuid1())+ ".zip"
        output_filename = tmppath+uuid_file_name

        make_zip(path, output_filename)
      
        response_data["url"] = "/upload/tmp/"+uuid_file_name
        response_data["issuc"] = 'true' 
    except:
        traceback.print_exc()
        response_data["error"] = '打包出错！' 


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def ziliao_editproperty(request):
    majorList=UserMajor.objects.all()
    curMajorId = getUserMajor(request.user)
    return render_to_response('TaskAndFlow/filemanager/editmessage.html', RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/")
def ziliao_fileproperty(request):
    response_data={}
    response_data["issuc"]="false"
    if request.method == 'GET':
        try:
            fileId=request.GET.get('fileId', None)
            doc = Document.objects.get(id=fileId)
            relateList = Doc2Relate.objects.filter(document_id=fileId)
            for  each  in relateList:
                each.relateinfo = GetRelateTypeInfo(each.relatetype, each.relateid)
            response_data["docinfo"] = objtojson(doc)
            response_data["relateList"] = objtojson(relateList)
            response_data["issuc"]="true"
        except Exception, e:
            traceback.print_exc()
            response_data["error"] = "获取文件信息失败！"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == 'POST':
        try:
            fileId=request.POST.get('fileId', None)
            addedGJs = eval(request.POST.get('addedGJs', '[]'))  # 关联元素
            deletedGJs = eval(request.POST.get('deletedGJs', '[]'))  # 关联元素
            remark=request.POST.get('remark', '')
            print addedGJs
            Doc2Relate_list_to_insert = []

            docId = int(fileId)
            for ys in addedGJs:
                if ys["typetable"]=='空间结构':
                    kjys = ys["relatedid"].split('_')
                    kjty = kjys[0]
                    kjid = kjys[1]
                    if kjty == 'unitprj':
                        kjty = u'单位工程'
                    elif kjty == 'floor':
                        kjty = u'楼层'
                    elif 'zone' in kjty:
                        kjty = u'分区'
                    Doc2Relate_list_to_insert.append(Doc2Relate(relatetype=kjty, relateid=int(kjid),creator=request.user, document_id=docId))
                elif ys["typetable"]=='分类信息':
                    kjys = ys["relatedid"].split('_')
                    kjty = kjys[0]
                    kjid = kjys[1]
                    if kjty == 'major':
                        kjty = u'专业'
                    elif kjty == 'type':
                        kjty = u'构件类型'
                    Doc2Relate_list_to_insert.append(Doc2Relate(relatetype=kjty, relateid=int(kjid),creator=request.user, document_id=docId))
                else:
                    Doc2Relate_list_to_insert.append(Doc2Relate(relatetype=ys["typetable"], relateid=ys["relatedid"],creator=request.user, document_id=docId))
            Doc2Relate.objects.bulk_create(Doc2Relate_list_to_insert)


            for ys in deletedGJs:
                Doc2Relate.objects.filter(relatetype=ys["typetable"], relateid=ys["relatedid"], document_id=docId).delete()

            doc = Document.objects.get(id=docId)
            doc.remark = remark
            doc.save()

            response_data["issuc"]="true"

        except:
            traceback.print_exc()
            response_data["error"] = "保存失败！"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
@login_required(login_url="/login/")
def ziliao_previewfile(request):
    if request.method == 'GET':
        return render_to_response('TaskAndFlow/filemanager/viewcad.html', RequestContext(request,locals()))
    elif request.method == 'POST':
        response_data={}
        response_data["issuc"]="false"
        try:
            fileId=request.POST.get('fileId', None)
            doc = Document.objects.get(id=fileId)
            if doc.previewfile:
                response_data["url"] = u"/upload/%s" % (doc.previewfile,)
                response_data["issuc"]="true"

        except:
            traceback.print_exc()
            response_data["error"] = "保存失败！"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
