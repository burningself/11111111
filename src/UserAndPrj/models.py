# -*- coding: utf-8 -*-
'''
Created on 2016年4月9日
用户和项目数据库模型
@author: pgb
'''
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from Scc4PM.settings import CURRENT_PROJECT_ID
from UserPrjConfig.models import *

class UserManager(BaseUserManager):

    def create_user(self, name, password=None):
        user = self.model(name=name,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None):
        user = self.create_user(name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserMajor(models.Model):
    '''用户专业表'''
    name=models.CharField(max_length=60,unique=True,verbose_name='专业名称')
    classfication_code = models.CharField(max_length=64,  blank=True, null=True,verbose_name='分类编码')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '用户专业'
        verbose_name_plural = '用户专业'

class Company(models.Model):
    '''企业表'''
    name = models.CharField(max_length=60,unique=True,verbose_name='名称')
    parent = models.ForeignKey('self',blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '企业'
        verbose_name_plural = '企业'

class User(AbstractBaseUser):
    '''用户表'''
    name = models.CharField(max_length=100, unique=True,verbose_name='用户名')
    contract=models.CharField(max_length=40,verbose_name='联系方式', blank=True,null=True)
    truename=models.CharField(max_length=20,verbose_name='实际姓名', blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    is_admin = models.BooleanField(default=False,verbose_name='是否超级管理员')
    company=models.ForeignKey(Company,verbose_name='所属企业', blank=True,null=True)
    major=models.ForeignKey(UserMajor,verbose_name='专业', blank=True,null=True)
    del_flag=models.BooleanField(default=False,verbose_name="删除标记")

    objects = UserManager()

    USERNAME_FIELD = 'name'

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.truename

    def get_username(self):
        return self.truename

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        rolelist = UserRoles.objects.filter(user_id=self).values_list('role_id', flat=True)
        if rolelist and RoleAuthor.objects.filter(role_id__in=rolelist,auth__name=perm):
                return True
        else:
            return False

        return True

    def has_module_perms(self, app_label):
        return True

    def reset_psw(self,str):
        self.set_password(str)

    @property
    def is_staff(self):
        return self.is_admin

    def userPrjRoles(self):
        return UserRoles.objects.filter(user_id=self)


class Project(models.Model):
    '''项目'''
    name=models.CharField(max_length=60,verbose_name='项目名称')
    address=models.CharField(max_length=120,verbose_name='项目地址')
    area=models.FloatField(verbose_name='建筑面积')
    cost=models.FloatField(verbose_name='工程造价')
    type=models.CharField(max_length=60,verbose_name='工程类型')
    manager=models.ForeignKey(User,related_name='manager',verbose_name='项目经理')
    engineer=models.ForeignKey(User,related_name='engineer',verbose_name='工程师')
    economist=models.ForeignKey(User,related_name='economist',verbose_name='经济师')
    productionmanager=models.ForeignKey(User,related_name='productionmanager',verbose_name='生产经理')
    constrator=models.ForeignKey(Company,related_name='constrator',verbose_name='建设单位')
    builder=models.ForeignKey(Company,related_name='builder',verbose_name='施工单位')
    supervisor=models.ForeignKey(Company,related_name='supervisor',verbose_name='监理单位')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    projecturl=models.URLField(max_length=120,verbose_name='项目网址')
    acronym=models.CharField(max_length=60,verbose_name='工程简称',default=None,null=True)
    appid = models.IntegerField(verbose_name='企业号应用编号',blank=True, null=True)
    secretid = models.CharField(max_length=200,verbose_name='企业号应用号密匙',blank=True, null=True)
    corpid = models.CharField(max_length=200,verbose_name='企业号编号',blank=True, null=True)
    wxsecret = models.CharField(max_length=200,verbose_name='企业微信通讯录密匙',blank=True, null=True)
    city = models.CharField(max_length=16,verbose_name='城市',blank=True, null=True)
    content = models.CharField(max_length=200000,verbose_name='内容',blank=True, null=True)
    version = models.IntegerField(verbose_name='版本',blank=True, null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'



class PageModel(models.Model):
    ''' 可定制页面'''
    name=models.CharField(max_length=60,verbose_name='可定制页面')
    def __str__(self):
        return self.name

class UserTemplate(models.Model):
    name=models.CharField(max_length=40,verbose_name='模板名称',default=None)
    user=models.ForeignKey(User, verbose_name='用户', blank=True,null=True)
    pro=models.ForeignKey(Project, verbose_name='关联项目',blank=True,null=True)
    page=models.CharField(max_length=200,verbose_name='页面名称',default=None)
    configData=models.CharField(max_length=200,verbose_name='模板 信息',default=None)
    is_active=models.BooleanField(default=False,verbose_name="是否启用")
    def __str__(self):
        return self.pro + ": " + self.user + ": " + self.template
    class Meta:
        verbose_name = '用户-配置模板'
        verbose_name_plural = '用户-配置模板'



class KnowledgeClassfication(models.Model):
    classify_name = models.CharField(max_length=120,verbose_name='分类名称')
    classification_code = models.CharField(max_length=64,unique=True,verbose_name='编码')
    alias_name = models.CharField(max_length=120, blank=True,verbose_name='别称')
    parent = models.ForeignKey('self', blank=True, null=True,verbose_name='父分类')
    rel_cbim_code = models.CharField(max_length=120, blank=True,verbose_name='国家分类体系')
    rel_qb_code = models.CharField(max_length=120, blank=True,verbose_name='对应清单编码')

    class Meta:
        verbose_name = '分类体系'
        verbose_name_plural = '分类体系'
        db_table = 'knowledge_classfication'
    def __str__(self):
        return self.classify_name


class KnowledgeHazardlist(models.Model):
    hazard_code = models.CharField(max_length=24,unique=True,verbose_name='编码')
    hazard_name = models.CharField(max_length=240,verbose_name='名称')
    description = models.CharField(max_length=480, blank=True,verbose_name='说明')
    parent = models.ForeignKey('self', blank=True, null=True,verbose_name='父危险源')
    threshold_value = models.CharField(max_length=64, blank=True,verbose_name='阈值')
    related_property = models.CharField(max_length=64, blank=True,verbose_name='控制属性')
    hazard_grade = models.CharField(max_length=16,verbose_name='等级')
    related_classfication_code = models.CharField(max_length=64,  blank=True, null=True,verbose_name='关联分类条目')
    major = models.ForeignKey(UserMajor, blank=True, null=True,verbose_name='专业')

    class Meta:
        verbose_name = '危险源'
        verbose_name_plural = '危险源知识库'
        db_table = 'knowledge_hazardlist'
    def __str__(self):
        return self.hazard_name

class KnowledgeUnit(models.Model):
    name = models.CharField(max_length=30,blank=True)
    alias = models.CharField(max_length=10,blank=True)
    unittype = models.CharField(max_length=10,blank=True)

    class Meta:
        db_table = 'knowledge_unit'

class KnowledgeRtChapter(models.Model):
    name = models.CharField(max_length=64,blank=True)
    RT_Code_No = models.CharField(max_length=64,blank=True)
    parent = models.ForeignKey("KnowledgeRtChapter",blank=True)
    class Meta:
        db_table = 'knowledge_rt_chapter'

class KnowledgeArea(models.Model):
    name = models.CharField(max_length=64,blank=True)
    class Meta:
        db_table = 'knowledge_area'

class KnowledgeRtCode(models.Model):
    RT_Code_Name = models.CharField(max_length=64,blank=True)
    RT_Code_No = models.CharField(max_length=64,blank=True)
    area = models.ForeignKey("KnowledgeArea",blank=True)
    major = models.ForeignKey("UserMajor",blank=True)
    class Meta:
        db_table = 'knowledge_rt_code'

class KnowledgeRtItem(models.Model):
    ItemNo = models.CharField(max_length=64,blank=True)
    name = models.CharField(max_length=64,blank=True)
    laborprice = models.FloatField(blank=True)
    materialprice = models.FloatField(blank=True)
    machineprice = models.FloatField(blank=True)
    totelprice = models.FloatField(blank=True)
    chapter = models.ForeignKey("KnowledgeRtChapter")
    unit = models.ForeignKey("KnowledgeUnit")
    class Meta:
        db_table = 'knowledge_rt_item'

class KnowledgeRtItemResource(models.Model):
    ItemCode = models.CharField(max_length=64,blank=True)
    name = models.CharField(max_length=128,blank=True)
    ItemCode = models.CharField(max_length=64,blank=True)
    restype = models.CharField(max_length=16,blank=True)
    unit = models.ForeignKey("KnowledgeUnit")
    price = models.FloatField(blank=True)
    class Meta:
        db_table = 'knowledge_rt_item_resource'

class KnowledgeRtItemRelate(models.Model):
    item = models.ForeignKey("KnowledgeRtItem")
    resource = models.ForeignKey("KnowledgeRtItemResource")
    amount = models.FloatField(blank=True)
    class Meta:
        db_table = 'knowledge_rt_item_resource_relate'


class Systemmenu(models.Model):
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=64, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,verbose_name='父菜单')
    url = models.CharField(max_length=256)
    param = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'userandprj_systemmenu'

class SystemfunctionCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    icon = models.CharField(max_length=64, blank=True)
    color = models.CharField(max_length=16, blank=True)

    class Meta:
        managed = False
        db_table = 'userandprj_systemfunction_category'

class Systemfunction(models.Model):
    name = models.CharField(max_length=64,unique=True)
    icon = models.CharField(max_length=64, blank=True)
    category = models.ForeignKey(SystemfunctionCategory, blank=True, null=True)
    url = models.CharField(max_length=256)
    param = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'userandprj_systemfunction'
