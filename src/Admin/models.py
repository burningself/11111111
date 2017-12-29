# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Projectmenu(models.Model):
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=64, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,verbose_name='父菜单')
    url = models.CharField(max_length=256)
    param = models.CharField(max_length=256, blank=True)
    isrecord = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=32, blank=True)
    seq = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'taskandflow_projectmenu'

class ProjectmenuMobile(models.Model):
    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=64, blank=True)
    color = models.CharField(max_length=32, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,verbose_name='父菜单')
    url = models.CharField(max_length=256)
    param = models.CharField(max_length=256, blank=True)
    isrecord = models.IntegerField(blank=True, null=True)
    seq = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'taskandflow_projectmenu_mobile'

class AdminFunctionCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    icon = models.CharField(max_length=64, blank=True)
    color = models.CharField(max_length=16, blank=True)
    isrecord = models.IntegerField(blank=True, null=True,default=1)

    class Meta:
        managed = False
        db_table = 'admin_systemfunction_category'

class AdminFunction(models.Model):
    name = models.CharField(max_length=64,unique=True)
    icon = models.CharField(max_length=64, blank=True)
    category = models.ForeignKey(AdminFunctionCategory, blank=True, null=True)
    url = models.CharField(max_length=256)
    param = models.CharField(max_length=256, blank=True)
    isrecord = models.IntegerField(blank=True, null=True,default=1)

    class Meta:
        managed = False
        db_table = 'admin_systemfunction'