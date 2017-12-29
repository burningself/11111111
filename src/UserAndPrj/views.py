# Create your views here.
# -*- coding: utf-8 -*-
CODEC = 'utf-8'
import json
from Scc4PM.settings import CURRENT_PROJECT_ID
from django.shortcuts import render
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,Http404
from django.core.context_processors import request
from django.http import HttpResponseRedirect
from django.contrib import auth
from UserAndPrj.forms import *
from UserAndPrj.models import *
from TaskAndFlow.models import *
from TaskAndFlow.utility import checkMobile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import urllib,traceback
from UserAndPrj.utility import *

@login_required(login_url="/login/")  
def user_view(request):
    return render_to_response('common/user.html', RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/")  
def user_project(request):
    try:
        response_data={}
        proList=[]
        user = User.objects.get(name=request.GET.get('username', '') )
        proObjList = user.UserRoles_set.all()

        for each in proObjList:
            tmp={}
            tmp["name"]=each.project.name
            tmp["url"]=each.project.projecturl
            proList.append(tmp)
         
        print  UserRoles.objects.filter(project_id=CURRENT_PROJECT_ID, user_id=user.id)  
        if user and UserRoles.objects.filter(project_id=CURRENT_PROJECT_ID, user_id=user.id):
            response_data["current"] = Project.objects.get(id=CURRENT_PROJECT_ID).projecturl
            response_data["currentName"] = Project.objects.get(id=CURRENT_PROJECT_ID).name
        else:
            response_data["current"] = None
        
        response_data["proList"] = proList
        response_data["status"] = "Succeed"
    except:
        import traceback
        print traceback.print_exc()
#        response_data["current"]="1111111"
        response_data["status"] = "Fail"

    return HttpResponse(json.dumps(response_data), content_type="application/json" )  

@login_required(login_url="/login/")  
def curproject(request):
    try:
        response_data={}
       
        if Project.objects.filter(id=CURRENT_PROJECT_ID):
            #response_data["current"] = Project.objects.get(id=CURRENT_PROJECT_ID).projecturl
            response_data["currentName"] = Project.objects.get(id=CURRENT_PROJECT_ID).name
        else:
            response_data["currentName"] = ''
        
        response_data["status"] = "Succeed"
    except:
        import traceback
        print traceback.print_exc()
        response_data["status"] = "Fail"

    return HttpResponse(json.dumps(response_data), content_type="application/json" )  

def welcome(request):
    try:
        proList=[]
        user = User.objects.get(name=request.GET.get('user', '') )
        proObjList = [ each for each in user.UserRoles_set.all()]
    except:
        proObjList = Project.objects.all()
        
    for each in proObjList:
        tmp={}
        tmp["name"]=each.name
        tmp["url"]=each.projecturl
        proList.append(tmp)
    
    if checkMobile(request):
        return render_to_response('common/welcome.html', RequestContext(request,locals()))
    else:
        return render_to_response('common/welcome.html', RequestContext(request,locals()))

@csrf_exempt
@login_required(login_url="/login/")  
def costomPage(request):
    if request.method == 'GET':
        username = request.GET.get('user', '')
        pro = request.GET.get('pro', '')
        pagePath = request.GET.get('pagePath', '')
        proObj = None if not Project.objects.filter(address=pro) else Project.objects.get(address=pro)
        userObj = None if not User.objects.filter(name=username) else User.objects.get(name=username)
        
        if UserTemplate.objects.filter(user=userObj, pro=proObj, page=pagePath):
#            print UserTemplate.objects.get(user=userObj, pro=proObj, page=pagePath).configData
            return HttpResponse(u'' + UserTemplate.objects.get(user=userObj, pro=proObj, page=pagePath).configData)
        else:
            return HttpResponse(u'Succeed')    
    else:
        username = request.POST.get('user', '')
        pro = request.POST.get('pro', '')
        savename = request.POST.get('savename', '')
        configData = request.POST.get('configData', '')
        pagePath = request.POST.get('pagePath', '')
        
        proObj = None if not Project.objects.filter(address=pro) else Project.objects.get(address=pro)
        userObj = None if not User.objects.filter(name=username) else User.objects.get(name=username)
        
        if userObj and pagePath:
            if UserTemplate.objects.filter(user=userObj, pro=proObj, page=pagePath):
                if configData:
                    UserTemplate.objects.filter(user=userObj, pro=proObj, page=pagePath).update(configData=configData)
                else:
                    UserTemplate.objects.filter(user=userObj, pro=proObj, page=pagePath).delete()
                return HttpResponse(u'Succeed')
            else:
                if configData and UserTemplate.objects.create(name=savename, user=userObj, pro=proObj, configData=configData, page=pagePath, is_active=True ):
                    return HttpResponse(u'Succeed')
    
    return HttpResponse(u'Failed')
          
@csrf_exempt
@login_required(login_url="/login/")  
def changepassword(request):
    if request.method =='POST':
        newpassword1 = request.POST.get('password1', '')
        newpassword2 = request.POST.get('password2', '')
        if newpassword1==newpassword2:
            username = request.POST.get('username', '')
            oldpassword = request.POST.get('oldpass', '')
#            print username, oldpassword, newpassword1, newpassword2
            userinfo = auth.authenticate(name=username, password=oldpassword)
            if userinfo is not None:
                userinfo.set_password(newpassword1)
                userinfo.save()
                return HttpResponse(u'修改成功,请重新登陆！')
            else:
                return HttpResponse(u'原密码检验不通过')
        else:
            return HttpResponse(u'密码输入不一致！')

@csrf_protect
def login(request):
    if checkMobile(request): 
        temName = 'common/login_mobile.html'
    else: 
        temName = 'common/login.html'

    development_units = ['上海建工四建集团有限公司','上海筑众信息科技有限公司']
    if CustomInfo.objects.filter(infotype='development_unit'):
        development_units =eval(CustomInfo.objects.filter(infotype='development_unit')[0].custominfo)
    lunbolist = Document.objects.filter(doctype="lunbo")
    backimg = "/images/main1.jpg"
    docs = Document.objects.filter(doctype='back').order_by("-createtime")
    if docs:
        backimg = "/"+str(docs[0].filepath)+docs[0].name
    logo = "/images/title.png"    
    docs = Document.objects.filter(doctype='logo').order_by("-createtime")
    if docs:
        logo = "/"+str(docs[0].filepath)+docs[0].name


    if request.method == 'GET':
        form = LoginForm() 
        return render_to_response(temName,RequestContext(request,locals()))
    else:
        form = LoginForm(request.POST)
        has_errors = False
        tip=""
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            if not User.objects.extra(where=["binary name=%s"],params=[username]):
                has_errors = True
                tip= "账号密码错误！"
                return render_to_response(temName,RequestContext(request,locals()))
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if UserRoles.objects.filter( user_id=user.id):
                    auth.login(request, user)
                    try:
                        nextpage = urllib.unquote(request.get_full_path().split('next=')[1])
                    except:
                        nextpage = '/index/'

                    return HttpResponseRedirect(nextpage)
                else:
                    has_errors = True
                    tip= "用户没有权限！"
                    return render_to_response(temName, RequestContext(request,locals()))
            else:
                has_errors = True
                tip= "账号密码错误！"
                return render_to_response(temName,RequestContext(request,locals()))
        else:
            has_errors = True
            tip= "信息不全！"
            return render_to_response(temName, RequestContext(request,locals()))
 
@csrf_exempt        
def wslogin(request):
    form = LoginForm(request.POST)
    response_data = {}
    try:
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            if not User.objects.extra(where=["binary name=%s"],params=[username]):
                raise Exception("账号密码错误！")
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                if UserRoles.objects.filter(user_id=user.id):
                    auth.login(request, user)
                else:
                    raise Exception("用户没有权限！")
            else:
                raise Exception("账号密码错误！")
        else:
            raise Exception("信息不全！")
        response_data["res"] = "success"
        response_data["sessionid"] = request.session.session_key
        if request.COOKIES.has_key("csrftoken"):
            response_data["csrftoken"] = request.COOKIES["csrftoken"]
        else:
            response_data["csrftoken"] = "abc123"
    except Exception, e: 
        traceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["res"] = "fail"

   
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def wslogout(request):
    print request.user.name
    response_data = {}
    auth.logout(request)
    response_data['res']='success'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")    
@csrf_exempt  
def resetPassword(request):
    response_data = {}
    response_data["issuc"] = False
    try:
        userid = request.POST.get('userid', None)
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not request.user.is_admin:
            raise Exception("您没有权限重置用户密码！")
            
        if password1 != password2:
            raise Exception("两次密码不一致!")

        user = User.objects.get(id=userid)
        user.set_password(password1)
        user.save()

        response_data["issuc"] = True
    except Exception as e:
        traceback.print_exc()
        response_data['error'] = '%s' % e
   
    return HttpResponse(json.dumps(response_data), content_type="application/json")
             
      

@login_required(login_url="/login/") 
@csrf_exempt       
def createUser(request):
    if request.method == "GET":
        return render_to_response('common/register.html',RequestContext(request))
    
    elif request.method == "POST":
        response_data = {}
        response_data["issuc"] = False
        try:
            username = request.POST.get('username', '')
            contract = request.POST.get('contract', '')
            truename = request.POST.get('truename', '')
            is_admin = eval(request.POST.get('is_admin', 'False'))
            company = request.POST.get('company', None)
            major = request.POST.get('major', None)
            division = request.POST.get('division', None)
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            roles = eval(request.POST.get('roles', '[]'))
            

            print is_admin
            if not request.user.is_admin:
                raise Exception("您没有权限添加用户！")

            if User.objects.filter(name=username):
                raise Exception("用户名已存在！")
                
            if password1 != password2:
                raise Exception("两次密码不一致!")

            if not company:
                raise Exception("公司必须设置!")

            if not major:
                raise Exception("专业必须设置!")

            if not division:
                raise Exception("参建方必须设置!")

            if len(roles)==0:
                raise Exception("角色不能为空!")

            CreateOneUser(username,contract,truename,is_admin,company,major,division,password1,roles)

            response_data["issuc"] = True
        except Exception as e:
            traceback.print_exc()
            response_data['error'] = '%s' % e
   
    return HttpResponse(json.dumps(response_data), content_type="application/json")

        
@login_required(login_url="/login/")  
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def userinfo(request):
    response_data = {}
    try:
        response_data["userinfo"]={}
        response_data["userinfo"]["name"] = request.user.truename
        response_data["userinfo"]["contract"] = request.user.contract
        response_data["userinfo"]["company"] = request.user.company.name
        response_data["userinfo"]["major"] = request.user.major.name
        response_data["userinfo"]["role"]=""
        if UserRoles.objects.filter(user=request.user):
            response_data["userinfo"]["role"] = UserRoles.objects.filter(user=request.user)[0].role.name
        response_data["res"] = "success"
    except Exception, e: 
        traceback.print_exc()
        response_data['error'] = '%s' % e
        response_data["res"] = "fail"
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")  
def introduce(request):
    usercanedit = 'true' if request.user.has_perm("编辑项目信息") else 'false'
    prj = Project.objects.get(id=CURRENT_PROJECT_ID)
    return render_to_response('AboutUs/introducetable.html', RequestContext(request,locals()))
    

@login_required(login_url="/login/")  
def introducetable(request):
    usercanedit = 'true' if request.user.has_perm("编辑项目信息") else 'false'
    prj = Project.objects.get(id=CURRENT_PROJECT_ID)
    return render_to_response('AboutUs/introduce.html', RequestContext(request,locals()))    


@login_required(login_url="/login/")  
def feedback(request):
    if request.method =='POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            feedbackinfo= form.cleaned_data['feedbackinfo']
            UserFeedback.objects.create(name=name,content=feedbackinfo,submitor=request.user)
            
            return HttpResponse('Success')
    return render_to_response('AboutUs/feedback.html', RequestContext(request,locals()))
    
def feedbacks(request):
	name = request.GET.get('name')
	email = request.GET.get('email')
	phone = request.GET.get('phone')
	text = request.GET.get('text')
	response_data={}
	response_data['issuc']='true'
	return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def error_404(request):
    if request.path[-1]=='/':
        return render_to_response('error/error_404.html')
    else:
        print "11111111111111111111111111"
        print request.get_full_path()
        newUrl = request.path+'/?'+request.get_full_path().split('?')[1]
        print newUrl
        return HttpResponseRedirect(newUrl)
 
@csrf_exempt
def error_500(request):
    if request.path[-1]=='/':
        return render_to_response('error/error_500.html')
    else:
        return HttpResponseRedirect(request.path+'/')


def error_403(request):
    if request.path[-1]=='/':
        return render_to_response('error/error_403.html')
    else:
        return HttpResponseRedirect(request.path+'/')



@login_required(login_url="/login/")
def prjusertree(request):
    id=request.GET.get('id', '')

    response_data = {}
    child_list=[]
    
    if UserDivision.objects.all().count()>0:
        prjMemberlist = list(UserRoles.objects.all().values_list("user_id", flat=True).distinct())
        prjCmpList = User.objects.filter(id__in=(prjMemberlist)).values_list("company_id").distinct()

        if id=='#':
            unit_items=Division.objects.all()
            for unit in unit_items:
                child_data = {}
                child_data["id"]="division_"+str(unit.id)
                child_data["text"]=unit.name
                child_data["title"]=unit.name
                child_data["icon"]=False
                child_data["expand"]=False
                child_data["checked"]=False
                
                list_items=[each.user for each in UserDivision.objects.filter(division=unit)]
                sub_child_list=[]
                for item in list_items:
                    sub_child_data = {}
                    sub_child_data["id"]=str(item.id)
                    sub_child_data["text"]=item.truename
                    sub_child_data["title"]=item.truename
                    sub_child_data["icon"]=False
                    sub_child_data["checked"]=False
                    sub_child_list.append(sub_child_data)
                child_data["children"]=sub_child_list
                child_list.append(child_data)
            response_data=child_list
    else:
        prj = Project.objects.get(id=CURRENT_PROJECT_ID)
        prjMemberlist = list(UserRoles.objects.all().values_list("user_id", flat=True).distinct())
        prjCmpList = User.objects.filter(id__in=(prjMemberlist)).values_list("company_id").distinct()

        if id=='#':
            unit_items=Company.objects.filter(id__in=prjCmpList)
            for unit in unit_items:
                child_data = {}
                child_data["id"]="cmp_"+str(unit.id)
                child_data["text"]=unit.name
                child_data["title"]=unit.name
                child_data["icon"]=False
                child_data["expand"]=False
                
                list_items=User.objects.filter(company = unit,id__in=prjMemberlist)
                sub_child_list=[]
                for item in list_items:
                    sub_child_data = {}
                    sub_child_data["id"]=str(item.id)
                    sub_child_data["text"]=item.truename
                    sub_child_data["title"]=item.truename
                    sub_child_data["icon"]=False
                    sub_child_list.append(sub_child_data)
                child_data["children"]=sub_child_list
                child_list.append(child_data)
            response_data=child_list


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required(login_url="/login/")
def companytree(request):
    isAll=request.GET.get('isAll', False)

    response_data = {}
    child_list=[]
    
    companylist = None
    child_data = {}
    if not isAll:
        prj = Project.objects.get(id=CURRENT_PROJECT_ID)
        prjMemberlist = list(UserRoles.objects.all().values_list("user_id", flat=True).distinct())
        prjCmpList = User.objects.filter(id__in=prjMemberlist).values_list("company_id").distinct()
        companylist=Company.objects.filter(id__in=prjCmpList)

        child_data["id"]= 'all'
        child_data["title"]=prj.name
        child_data["expand"]=True
    else:
        companylist=Company.objects.all()
        child_data["id"]= 'all'
        child_data["title"]='智慧建造平台'
        child_data["expand"]=True

    sub_child_list=[]
    for each in companylist:
        sub_child_data = {}
        sub_child_data["id"]=str(each.id)
        sub_child_data["title"]=each.name
        sub_child_list.append(sub_child_data)
    child_data["children"]=sub_child_list
    child_list.append(child_data)    
    response_data=child_list


    return HttpResponse(json.dumps(response_data), content_type="application/json")
