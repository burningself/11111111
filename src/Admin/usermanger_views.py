# -*- coding: utf-8 -*-

import traceback
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt


from UserAndPrj.models import *
from TaskAndFlow.models import *
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
import json,datetime,random
from dss.Serializer import serializer as objtojson
from Scc4PM.settings import UPLOAD_DIR,CURRENT_PROJECT_ID

@login_required(login_url="/login/")  
def usermanager_vue(request):
    return render_to_response('xadmin/usermanager/user.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def addusers_vue(request):
    return render_to_response('xadmin/usermanager/addusers.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def guideusers_vue(request):
    return render_to_response('xadmin/usermanager/guideusers.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def editRole_vue(request):
    return render_to_response('xadmin/usermanager/editRoleLimit.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def batchUser_vue(request):
    return render_to_response('xadmin/usermanager/batchUser.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
def divisionManage_vue(request):
    return render_to_response('xadmin/usermanager/divisionManage.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
def companyManage_vue(request):
    return render_to_response('xadmin/usermanager/companyManager.html', RequestContext(request,locals()))

@login_required(login_url="/login/")
def majorManage_vue(request):
    return render_to_response('xadmin/usermanager/majorManager.html', RequestContext(request,locals()))
    
@login_required(login_url="/login/")  
def componentType_vue(request):
    return render_to_response('xadmin/usermanager/componentType.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def typeMeeting_vue(request):
    return render_to_response('xadmin/usermanager/typeMeeting.html', RequestContext(request,locals()))
     
@login_required(login_url="/login/")  
def qualityAccept_vue(request):
    return render_to_response('xadmin/usermanager/qualityAccept.html', RequestContext(request,locals()))

@login_required(login_url="/login/")  
def procedureAccept_vue(request):
    return render_to_response('xadmin/usermanager/procedureAccept.html', RequestContext(request,locals()))
