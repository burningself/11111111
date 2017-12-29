# -*- coding: utf-8 -*-
'''
Created on 2017年10月23日
空间管理相关数据表
@author: pgb
'''
from django.db import models
from UserAndPrj.models import *
from TaskAndFlow.models import *
from Scc4PM.dbsetings import CrossDbForeignKey

class SpaceStatus(models.Model):
    '''空间状态表'''
    name=models.CharField(max_length=64,verbose_name='名称',null=True,blank=True)
    color=models.CharField(max_length=24,verbose_name='颜色',null=True,blank=True)
    substatus=models.IntegerField(verbose_name='子状态',null=True,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '空间状态'
        verbose_name_plural = '空间状态'
        db_table = 'spacemanager_spacestatus'


class Space(models.Model):
    '''空间表'''
    number=models.CharField(max_length=64,verbose_name='编号')
    name=models.CharField(max_length=64,verbose_name='名称')
    boundary=models.CharField(max_length=128,verbose_name='边界',null=True,blank=True)
    thumbnail=models.CharField(max_length=256,verbose_name='布置图地址',null=True,blank=True)
    modelguid=models.CharField(max_length=64,verbose_name='模型GUID',null=True,blank=True)
    lmvdbid=models.IntegerField(verbose_name='模型lmvdbid',null=True,blank=True)
    status = models.ForeignKey(SpaceStatus,verbose_name='状态', blank=True, null=True)
    zone = models.ForeignKey(Zone,verbose_name='所属区域',blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '空间'
        verbose_name_plural = '空间'
        db_table = 'spacemanager_space'

class SpaceAsignment(models.Model):
    '''空间分配表'''
    create_date=models.DateField(verbose_name='创建日期')
    start_date=models.DateField(verbose_name='起始日期')
    end_date=models.DateField(verbose_name='结束日期')
    flowstep=models.IntegerField(verbose_name='当前步骤',default=0)
    applycomment=models.CharField(max_length=256,verbose_name='申请备注',null=True,blank=True)
    approvecomment=models.CharField(max_length=256,verbose_name='批准备注',null=True,blank=True)
    space = models.ForeignKey(Space,verbose_name='空间', blank=True, null=True)
    major = CrossDbForeignKey(UserMajor,verbose_name='专业',blank=True, null=True)
    company = CrossDbForeignKey(Company,verbose_name='公司',blank=True, null=True)
    user = CrossDbForeignKey(User,verbose_name='申请人',blank=True, null=True)
    status = models.ForeignKey(SpaceStatus,verbose_name='空间状态',blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '空间分配'
        verbose_name_plural = '空间分配'
        db_table = 'spacemanager_spaceasignment'


class SpaceIBeacon(models.Model):
    '''IBeacon表'''
    name=models.CharField(max_length=64,verbose_name='名称')
    uuid=models.CharField(max_length=64,verbose_name='编号')
    major=models.CharField(max_length=16,verbose_name='major')
    minor=models.CharField(max_length=16,verbose_name='minor')
    deploytime=models.DateField(verbose_name='部署日期',null=True,blank=True)
    postion=models.CharField(max_length=128,verbose_name='位置',null=True,blank=True)
    space = models.ForeignKey(Space,verbose_name='空间', blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'IBeacon表'
        verbose_name_plural = 'IBeacon表'
        db_table = 'spacemanager_ibeacon'