from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.core.context_processors import request
from django.http import HttpResponseRedirect
from UserPrjConfig.models import *
from TaskAndFlow.utility import checkMobile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import urllib,traceback
import json,datetime,random


@login_required(login_url="/login/") 
@csrf_exempt       
def addRoleAuths(request):
    response_data = {}
    response_data["issuc"] = False
    try:
        role = request.POST.get('role', '')
        auths = eval(request.POST.get('auths', '[]'))

        auth_list_to_insert = list()
        for each in auths:
            auth_list_to_insert.append(RoleAuthor(role_id=int(role), auth_id=int(each)))
        RoleAuthor.objects.bulk_create(auth_list_to_insert)

        response_data["issuc"] = True
    except Exception as e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
   
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/") 
@csrf_exempt       
def delRoleAuths(request):
    response_data = {}
    response_data["issuc"] = False
    try:
        role = request.POST.get('role', '')
        auths = eval(request.POST.get('auths', '[]'))

        RoleAuthor.objects.filter(role_id=int(role), auth_id__in=auths).delete()

        response_data["issuc"] = True
    except Exception as e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
   
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/") 
@csrf_exempt       
def delProjectUsers(request):
    response_data = {}
    response_data["issuc"] = False
    try:
        users = eval(request.POST.get('users', '[]'))

        UserRoles.objects.filter(user_id__in=users).delete()
        UserDivision.objects.filter(user_id__in=users).delete()

        response_data["issuc"] = True
    except Exception as e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
   
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/login/") 
@csrf_exempt       
def addUserRoles(request):
    response_data = {}
    response_data["issuc"] = False
    try:
        userid = request.POST.get('userid', '')
        roles = eval(request.POST.get('roles', '[]'))

        role_list_to_insert = list()
        for each in roles:
            role_list_to_insert.append(UserRoles(user_id=int(userid), role_id=int(each)))
        UserRoles.objects.bulk_create(role_list_to_insert)

        response_data["issuc"] = True
    except Exception as e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
   
    return HttpResponse(json.dumps(response_data), content_type="application/json")
