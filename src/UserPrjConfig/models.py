# -*- coding: utf-8 -*-
'''
Created on 2017年11月28日
用户权限数据库模型
@author: pgb
'''
from django.db import models
from Scc4PM.dbsetings import CrossDbForeignKey


class Role(models.Model):
    '''用户角色表'''
    name=models.CharField(max_length=60,unique=True,verbose_name='用户角色')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'

    def roleAuthors(self):
        return RoleAuthor.objects.filter(role_id=self)

class Author(models.Model):
    '''用户权限表'''
    name = models.CharField(max_length=60,unique=True,verbose_name='权限')
    permdict = models.CharField(max_length=512,verbose_name='权限字典')
    classify = models.CharField(max_length=60,verbose_name='权限类别',blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '用户权限'
        verbose_name_plural = '用户权限'

class RoleAuthor(models.Model):
    '''用户角色权限表'''
    role= models.ForeignKey(Role,verbose_name='角色')
    auth = models.ForeignKey(Author,verbose_name='权限')
    class Meta:
        unique_together = ( ("role", "auth"), )
        verbose_name = '用户角色权限'
        verbose_name_plural = '用户角色权限'



class UserRoles(models.Model):
    '''用户-项目-角色表'''
    user=CrossDbForeignKey('UserAndPrj.User',verbose_name='用户',related_name='userroles')
    role=models.ForeignKey(Role,verbose_name='角色')

    class Meta:
        unique_together = ( ("user", "role"), )
        verbose_name = '用户-项目-角色'
        verbose_name_plural = '用户-项目-角色'


class Division(models.Model):
    '''参建方表'''
    name=models.CharField(max_length=60,unique=True,verbose_name='名称')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '参建方'
        verbose_name_plural = '参建方'


class UserDivision(models.Model):
    '''用户-项目-参建方'''
    user=CrossDbForeignKey('UserAndPrj.User',verbose_name='用户',related_name='userdivisions')
    division=models.ForeignKey(Division,verbose_name='参建方')

    class Meta:
        unique_together = ( ("user", "division"), )
        verbose_name = '用户-项目-参建方'
        verbose_name_plural = '用户-项目-参建方'


class Feedback(models.Model):
    submittime=models.DateTimeField(auto_now_add=True,verbose_name='提交时间')
    content=models.CharField(max_length=400,verbose_name='内容')
    submitor=CrossDbForeignKey('UserAndPrj.User',verbose_name='提交人')
    def __str__(self):
        return self.content
    class Meta:
        verbose_name = '使用反馈'
        verbose_name_plural = '使用反馈'



class NoticeCategory(models.Model):
    '''通知分类表'''
    typetag = models.CharField(max_length=60,verbose_name='分类')
    subtypetag = models.CharField(max_length=60,verbose_name='子分类')

    class Meta:
        unique_together = ( ("typetag", "subtypetag"), )
        verbose_name = '通知分类表'
        verbose_name_plural = '通知分类表'

class NoticeTemplate(models.Model):
    '''通知模板表'''
    category= models.ForeignKey(NoticeCategory,verbose_name='所属分类')
    title = models.CharField(max_length=120,verbose_name='标题')
    content = models.CharField(max_length=512,verbose_name='内容')
    extendparam = models.CharField(max_length=1024,verbose_name='扩展参数')
    isopen = models.BooleanField(default=True,verbose_name='是否开启')
    class Meta:
        verbose_name = '通知模板表'
        verbose_name_plural = '通知模板表'

class NoticeSlot(models.Model):
    '''通知词槽表'''
    tag = models.CharField(max_length=60,verbose_name='标题')
    info = models.CharField(max_length=120,verbose_name='内容')
    example = models.CharField(max_length=120,verbose_name='示例')
    typetag = models.CharField(max_length=60,verbose_name='分类')
    subtypetag = models.CharField(max_length=60,verbose_name='子分类',blank=True, null=True)
    isenable = models.BooleanField(default=True,verbose_name='是否启用')
    class Meta:
        verbose_name = '通知词槽表'
        verbose_name_plural = '通知词槽表'