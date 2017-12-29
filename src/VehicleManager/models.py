# -*- coding: utf-8 -*-
'''
Created on 2017年10月23日
车辆管理相关数据表
@author: pgb
'''
from django.db import models
from UserAndPrj.models import *
from TaskAndFlow.models import *
from Scc4PM.dbsetings import CrossDbForeignKey


class Vehicle(models.Model):
    '''车辆登记信息'''
    plate=models.CharField(max_length=32,verbose_name='车牌',unique=True)
    company=CrossDbForeignKey(Company,verbose_name='所属公司')
    cartype = models.CharField(max_length=16,verbose_name='车型')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '车辆登记信息'
        verbose_name_plural = '车辆登记信息'
        db_table = 'vehiclemanager_vehicle'


class AlarmInfoPlate(models.Model):
    '''车牌识别信息'''
    channel=models.CharField(max_length=16,verbose_name='出入口标志',null=True,blank=True)
    devicename=models.CharField(max_length=64,verbose_name='设备名称',null=True,blank=True)
    license=models.CharField(max_length=32,verbose_name='车牌号')
    direction = models.IntegerField(verbose_name='行驶方向',null=True,blank=True)
    platecolor = models.CharField(max_length=16,verbose_name='车牌颜色',null=True,blank=True)
    recotime=models.DateTimeField(verbose_name='时间',null=True,blank=True)
    image=models.ForeignKey(Document,related_name='image',verbose_name='全景图',null=True,blank=True)
    imageplate=models.ForeignKey(Document,related_name='imageplate',verbose_name='车牌小图',null=True,blank=True)
    parkdoor= models.CharField(max_length=64,verbose_name='门口名称',null=True,blank=True)
    cartype = models.CharField(max_length=16,verbose_name='车型',null=True,blank=True)
    
    def __str__(self):
        return self.license

    class Meta:
        verbose_name = '车牌识别信息'
        verbose_name_plural = '车牌识别信息'
        db_table = 'vehiclemanager_alarminfoplate'

