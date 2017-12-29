# -*- coding: utf-8 -*-

import os,time,random, sys, datetime, calendar, traceback
import memcache
import urllib2,json
from Scc4PM import settings
from TaskAndFlow.models import *
from UserAndPrj.models import *
from TaskAndFlow.utility import createWXUser
from UserPrjConfig.models import UserRoles

def getPrjImage(prj):
    backimg = "/images/loginbg.jpg"
    backimg = prj.projecturl+backimg
    return backimg

def CreateOneUser(username,contract,truename,is_admin,company,major,division,password,roles):
    if is_admin:
        user = User.objects.create_superuser(username, password = password)
    else:
        user = User.objects.create_user(username, password = password)

    user.contract = contract
    user.truename = truename
    user.company_id = int(company)
    user.major_id = int(major)
    user.save()

    role_list_to_insert = list()
    for each in roles:
        role_list_to_insert.append(UserRoles(user=user, role_id=int(each)))
    UserRoles.objects.bulk_create(role_list_to_insert)

    UserDivision.objects.create(user=user, division_id=int(division))

    if user.contract:
        createWXUser(user.truename,user.contract,user.company.name)