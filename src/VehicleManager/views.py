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
from UserAndPrj.models import *
from VehicleManager.models import *
from TaskAndFlow.utility_filemanager import *
from TaskAndFlow.utility import *
from dss.Serializer import serializer as objtojson
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
from Scc4PM.settings import CURRENT_PROJECT_ID
from django.conf import settings
from Scc4PM.settings import UPLOAD_DIR
import datetime, json,base64,codecs
from UserPrjConfig.permissions import *


def getVehicleDir():
    savedir = Directory.objects.get(name="车辆管理",islock=True)
    return savedir

def saveBase64Img(imagedata,plate,customname=""):
    imagedata  = base64.b64decode(imagedata) 
       
    path=settings.UPLOAD_DIR
    curdate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print curdate
    filename = u"%s_%s%s.jpg" % (plate,curdate,customname)
    file_path_name = path + filename

    destination = open(file_path_name, 'wb+')
    destination.write(imagedata)
    destination.close()

    
    doc = Document()
    doc.name = filename
    doc.shortname = filename
    doc.filepath = u"upload/"
    doc.creator_id=1
    doc.filesize = len(imagedata)
    doc.filetype = "image/jpeg"
    doc.doctype='normal'
    doc.save()

    Vehicledir = getVehicleDir()        
    if Vehicledir:
        doc.docdirectory.add(Vehicledir)
        movefiletoDir(doc,Vehicledir)
    return doc


@csrf_exempt
def upload_wentong(request):
    response_data = {}
    response_data["res"] = 'fail'
    try:
        if request.method == 'POST':
            print request.body.decode("gb2312").encode("utf-8")
            req = json.loads(request.body.decode("gb2312").encode("utf-8"))
            AlarmInfoPlateDict = req["AlarmInfoPlate"]
            
            plate = AlarmInfoPlate()
            plate.channel = AlarmInfoPlateDict["channel"]
            plate.devicename = AlarmInfoPlateDict["deviceName"]
            plate.license = AlarmInfoPlateDict["result"]["PlateResult"]["license"]
            plate.direction = AlarmInfoPlateDict["result"]["PlateResult"]["direction"]
            plate.platecolor = AlarmInfoPlateDict["result"]["PlateResult"]["platecolor"]
            plate.channel = AlarmInfoPlateDict["result"]["PlateResult"]["direction"]
            plate.recotime = AlarmInfoPlateDict["result"]["PlateResult"]["recotime"]
            plate.parkdoor = AlarmInfoPlateDict["ParkDoor"]
            plate.cartype = AlarmInfoPlateDict["result"]["PlateResult"]["CarType"]
            
            if plate.license:
                plate.imageplate = saveBase64Img(AlarmInfoPlateDict["result"]["PlateResult"]["imageFragmentFile"],plate.license,u"")
            plate.image = saveBase64Img(AlarmInfoPlateDict["result"]["PlateResult"]["imageFile"],plate.license,u"全景")
            plate.save()

            response_data["res"] = 'sucess'
    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
@check_permission
def vehiclemgr_index(request):
    if checkMobile(request):
        templateName = 'VehicleManager/carmanage.html'
    else:
        templateName = 'VehicleManager/carmanage.html'
    return render_to_response(templateName, RequestContext(request, locals()))


def carinfocount(request):
    response_data = {}
    response_data["res"] = 'fail'
    try:
        startTime = datetime.datetime.strptime(str(datetime.date.today()) + " 00:00:01",'%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(str( datetime.date.today()) + " 23:59:59",'%Y-%m-%d %H:%M:%S')
        response_data["todaytotal"] = AlarmInfoPlate.objects.filter(recotime__range=(startTime,endTime)).count()
        response_data["curenttotal"] = AlarmInfoPlate.objects.filter(recotime__range=(startTime,endTime)).values('license').distinct().count()
        typemap={}
        for each in AlarmInfoPlate.objects.filter(recotime__range=(startTime,endTime)):
            cartype = "其他"
            try:
                cartype = Vehicle.objects.get(plate=each.license).cartype
            except Exception as e:
                pass 
            if typemap .has_key(cartype):
                typemap[cartype]+=typemap[cartype]
            else:
                typemap[cartype]=1

        print typemap
        response_data["typecount"] = [ {"type":key,"value":typemap[key]} for key in typemap]

        companymap = {}
        for each in AlarmInfoPlate.objects.filter(recotime__range=(startTime,endTime)):
            company = "其他"
            try:
                company = Vehicle.objects.get(plate=each.license).company.name
            except Exception as e:
                pass 
            if companymap .has_key(company):
                companymap[company]+=typemap[company]
            else:
                companymap[company]=1
        response_data["companycount"] =  [ {"type":key,"value":companymap[key]} for key in companymap]

        response_data["res"] = 'sucess'
    except Exception, e:
        traceback.print_exc()
        response_data['error'] = '%s' % e

    return HttpResponse(json.dumps(response_data), content_type="application/json")


