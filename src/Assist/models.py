# -*- coding: utf-8 -*-
'''
Created on 2017.2.27
潘古兵
@author: pgb
'''
from django.db import models
from UserAndPrj.models import *
from Admin.models import *
from Scc4PM.dbsetings import CrossDbForeignKey

class Meeting(models.Model):
    name = models.CharField(max_length=128, blank=True)
    hostuser = CrossDbForeignKey(User, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True)
    meetingtype = models.ForeignKey('Meetingtype', blank=True, null=True)
    room = models.ForeignKey('Meetingroom', blank=True, null=True)
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    roomname = models.CharField(max_length=64, blank=True)

    class Meta:
        managed = False
        db_table = 'assist_meeting'

class MeetingZhouqi(models.Model):
    name = models.CharField(max_length=128, blank=True)
    hostuser = CrossDbForeignKey(User, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True)
    meetingtype = models.ForeignKey('Meetingtype', blank=True, null=True)
    room = models.ForeignKey('Meetingroom', blank=True, null=True)
    begin_time = models.CharField(max_length=32,blank=True, null=True)
    end_time = models.CharField(max_length=32,blank=True, null=True)
    roomname = models.CharField(max_length=64, blank=True)
    zhouqitype = models.IntegerField(blank=True,null=True,default=1)
    create_time = models.CharField(max_length=64, blank=True)

    class Meta:
        managed = False
        db_table = 'assist_meeting_zhouqi'


class MeetingUser(models.Model):
    meeting = models.ForeignKey(Meeting, blank=True, null=True)
    user = CrossDbForeignKey(User, blank=True, null=True)
    isattend = models.IntegerField(blank=True,null=True,default=0,verbose_name='参与会议状态（1：是，0：未确认，2：不参加）')
    reason = models.CharField(max_length=256, blank=True,verbose_name='原因')

    class Meta:
        managed = False
        db_table = 'assist_meeting_user'

class MeetingZhouqiUser(models.Model):
    meeting = models.ForeignKey(MeetingZhouqi, blank=True, null=True)
    user = CrossDbForeignKey(User, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assist_meeting_zhouqi_user'


class Meetingrelatedfile(models.Model):
    meeting = models.ForeignKey(Meeting, blank=True, null=True)
    file = models.ForeignKey('TaskAndFlow.Document', blank=True, null=True)
    isrecord = models.IntegerField(blank=True, null=True,default=False)

    class Meta:
        managed = False
        db_table = 'assist_meetingrelatedfile'

class MeetingZhouqirelatedfile(models.Model):
    meeting = models.ForeignKey(MeetingZhouqi, blank=True, null=True)
    file = models.ForeignKey('TaskAndFlow.Document', blank=True, null=True)
    isrecord = models.IntegerField(blank=True, null=True,default=False)

    class Meta:
        managed = False
        db_table = 'assist_meeting_zhouqirelatedfile'


class Meetingroom(models.Model):
    number = models.CharField(max_length=64, blank=True)

    class Meta:
        managed = False
        db_table = 'assist_meetingroom'



class Meetingtype(models.Model):
    '''会议类型'''
    name = models.CharField(max_length=64, blank=True)

    class Meta:
        managed = False
        db_table = 'assist_meetingtype'
        verbose_name = '会议类型'
        verbose_name_plural = '会议类型'

    def __str__(self):
        return self.name



# 表单管理
class BiaoDanType(models.Model):
    name = models.CharField(max_length=40,verbose_name='表单类型')
    class Meta:
        db_table = 'taskandflow_formtype'




class BiaoDanMuBan(models.Model):
    name = models.CharField(max_length=40,verbose_name='名称')
    content = models.CharField(max_length=200000,verbose_name='内容')
    creater = CrossDbForeignKey(User,verbose_name='创建人')
    createdate = models.DateTimeField(auto_now=True,verbose_name='创建日期')
    major = CrossDbForeignKey(UserMajor,verbose_name='专业',blank=True, null=True)
    formtype = models.ForeignKey(BiaoDanType,verbose_name='表单类型')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'taskandflow_formtemplet'

class BiaoDan(models.Model):
    name = models.CharField(max_length=40,verbose_name='名称')
    content = models.CharField(max_length=200000,verbose_name='内容')
    creater = CrossDbForeignKey(User,verbose_name='创建人')
    createdate = models.DateTimeField(auto_now=True,verbose_name='创建日期')
    major = CrossDbForeignKey(UserMajor,verbose_name='专业',blank=True, null=True)
    formtype = models.ForeignKey(BiaoDanType,verbose_name='表单类型')
    formtemplet = models.ForeignKey(BiaoDanMuBan,verbose_name='表单模板')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'taskandflow_form'

class Formtag(models.Model):
    tagname = models.CharField(max_length=64, blank=True)
    tag = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_formtag'

class Formtempandformtag(models.Model):
    formtemplet = models.ForeignKey(BiaoDanMuBan,verbose_name='表单模板id')
    formtag = models.ForeignKey(Formtag,verbose_name='数据源id')

    class Meta:
        managed = False
        db_table = 'taskandflow_formtempletandformtag'

class Constructiondiary(models.Model):
    '''施工日记'''
    diary_date = models.DateField(unique=True)
    update_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    name = models.CharField(max_length=64, blank=True)
    user = CrossDbForeignKey(User)
    related_form = models.ForeignKey(BiaoDan, blank=True, null=True)
    file = models.ForeignKey('TaskAndFlow.Document', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_constructiondiary'


class Weekly(models.Model):
    weekly_date = models.DateField()
    update_time = models.DateTimeField()
    name = models.CharField(max_length=64, blank=True)
    user = CrossDbForeignKey(User)
    dir = models.ForeignKey('TaskAndFlow.Directory', blank=True, null=True)
    content = models.CharField(max_length=200000,verbose_name='内容')
    deleteissue = models.CharField(max_length=512,verbose_name='删除的事件')
    file = models.ForeignKey('TaskAndFlow.Document', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'taskandflow_weekly'

class MonthPlan(models.Model):
    '''月度计划'''
    month_date = models.DateField()
    update_time = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    desc = models.CharField(max_length=256, blank=True)
    user = CrossDbForeignKey(User)
    file = models.ForeignKey('TaskAndFlow.Document', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_monthplan'

class Workgoal(models.Model):
    '''工作目标'''
    label = models.CharField(max_length=64, blank=True)
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True)
    user = CrossDbForeignKey(User)

    def __str__(self):
        return self.label

    class Meta:
        managed = False
        db_table = 'taskandflow_workgoal'


class Finishedtasksingoal(models.Model):
    '''工作目标完成任务'''
    workgoal = models.ForeignKey(Workgoal)
    task = models.ForeignKey('TaskAndFlow.ProjectTask')

    class Meta:
        managed = False
        db_table = 'taskandflow_finishedtasksingoal'




class Usershortcut(models.Model):
    user = CrossDbForeignKey(User)
    function = models.ForeignKey(AdminFunction)
    seq = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ( ("user", "function"))
        managed = False
        db_table = 'taskandflow_usershortcut'


class Weather(models.Model):
    date = models.DateField(unique=True, verbose_name="时间")
    week = models.CharField(max_length=16, verbose_name="星期")
    weather = models.CharField(max_length=16, verbose_name="天气")
    temphigh = models.IntegerField(verbose_name="最高温度")
    templow = models.IntegerField(verbose_name="最高温度")
    winddirect = models.CharField(max_length=16, verbose_name="风向",blank=True, null=True)
    windpower = models.CharField(max_length=16, verbose_name="风力",blank=True, null=True)
    class Meta:
        verbose_name = '天气记录'
        verbose_name_plural = '天气记录'

