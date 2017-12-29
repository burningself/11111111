# -*- coding: utf-8 -*-
'''

@author: pgb
'''
import traceback,datetime,array,calendar
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from UserAndPrj.models import *
from Assist.models import *
from TaskAndFlow.utility_filemanager import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
from Scc4PM.settings import CURRENT_PROJECT_ID
import urllib, urllib2, sys,memcache

def getWeathers():
    newweathers=[]
    if Weather.objects.filter(date__gte=datetime.date.today()).count()>=5:
        for each in Weather.objects.filter(date__gte=datetime.date.today()):
                tmp={}
                tmp["days"]=str(each.date)
                tmp["week"]=each.week
                tmp["weather"]=each.weather
                tmp["temperature"]="%d°C/%d°C" % (each.templow ,each.temphigh)
                newweathers.append(tmp)
    else:
        host = 'http://jisutqybmf.market.alicloudapi.com'
        path = '/weather/query'
        method = 'GET'
        appcode = '31c381b0f18b4d96bca00ecd6759b677'
        city = Project.objects.get(id=CURRENT_PROJECT_ID).city
        querys = 'city='+city
        bodys = {}
        url = host + path + '?' + querys

        request = urllib2.Request(url)
        request.add_header('Authorization', 'APPCODE ' + appcode)
        response = urllib2.urlopen(request)
        content = response.read()
        print "get weather from servers!!!!!"
        weathers = eval(content)
        weathers_to_insert = list()
        if weathers["status"]=="0":
            for each in weathers["result"]["daily"]:
                tmp={}
                tmp["days"]=each["date"]
                tmp["week"]=each["week"]
                tmp["weather"]=each["day"]["weather"]
                tmp["temperature"]=each["night"]["templow"]+"°C/"+each["day"]["temphigh"]+"°C"
                newweathers.append(tmp)
                weathers_to_insert.append(Weather(date=each["date"], week=each["week"],weather=each["day"]["weather"], 
                    templow=each["night"]["templow"],temphigh=each["day"]["temphigh"]))
        Weather.objects.filter(date__gte=newweathers[0]["days"]).delete()
        Weather.objects.bulk_create(weathers_to_insert)

    return newweathers


@login_required(login_url="/login/") 
def loadweather(request):
    response_data = {}
    response_data["issuc"]="false"
    try:
        response_data["result"] = getWeathers()
        response_data["issuc"]="true"
    except Exception, e: 
        traceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["issuc"]="false"
    return HttpResponse(json.dumps(response_data), content_type="application/json")  


