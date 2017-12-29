# -*- coding: utf-8 -*-
'''
Created on 2017年11月21日
权限配置
@author: pgb
'''
from django.core.urlresolvers import resolve
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from UserPrjConfig.models import *
import traceback

# 权限字段对应URL规则，匹配后可操作
# 权限字段名称(models表中定义)，URL列表,请求方法(GET,POST)


def perm_check(*args, **kwargs):
    request = args[0]
    # 反向解析request中url
    current_url = request.path_info
    request_method = request.method
    print "url path_info:",current_url
    matched_flag = False
    matched_perm_key = None
    # 如果正确反解析出了url且其在权限字典中
    authlist = Author.objects.all()
    if current_url is not None and authlist:
        for each in authlist:
            try:
                perm_dic = eval(each.permdict)
                if perm_dic.has_key(current_url) and perm_dic[current_url]==request_method:
                    matched_flag = True
                    matched_perm_key = each.name
                    print 'matched perm ...'
                    break
            except Exception as e:
                pass

        
    else:
        # 如果项目没有配置权限，则全部放过
        return True
    # request请求与权限规则已匹配
    if matched_flag == True:
        perm_str = matched_perm_key
        # 如果用户被授与此权限，返回True，否则返回False
        if request.user.has_perm(perm_str):
            print "[ ------ permission checked -------]"
            return True
        else:
            print "[ ------- no permission -----------]"
            return False
    else:
        print "[ ------ no matched permission ----- ]"
        return True

    return True
 
def check_permission(func):
    def wrapper(*args, **kwargs):
        print "--start check perms",args[0]
        if not perm_check(*args, **kwargs):
            return HttpResponseRedirect('/error_403/')
        return func(*args, **kwargs)
    return wrapper


def check_permission_ajax(func):
    def wrapper(*args, **kwargs):
        print "--start check perms",args[0]
        if not perm_check(*args, **kwargs):
            return HttpResponse(status=403)
        return func(*args, **kwargs)
    return wrapper



