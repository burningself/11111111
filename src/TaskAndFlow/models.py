# -*- coding: utf-8 -*-
'''
Created on 2016年4月10日
项目任务和流程数据库模型
@author: pgb
'''
from django.db import models
from UserAndPrj.models import *
from UserPrjConfig.models import *
from Assist.models import *
from django.template.defaultfilters import default
from django.core import exceptions
from django.db import models
from Scc4PM.dbsetings import CrossDbForeignKey
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




#构件场地管理------------------------------------------
class FactoryArea(models.Model):
    '''场地表'''
    number=models.CharField(max_length=60,verbose_name='场地编号')
    area=models.FloatField(verbose_name='面积',null=True,blank=True)
    length=models.FloatField(verbose_name='长度',null=True,blank=True)
    width=models.FloatField(verbose_name='宽度',null=True,blank=True)
    elevation=models.ForeignKey('Elevation',verbose_name='标高',null=True) 
    elementid=models.CharField(max_length=60,verbose_name='ElementID',null=True,blank=True)
    uniqueid=models.CharField(max_length=60,verbose_name='uniqueID',null=True,blank=True)
    total=models.FloatField(verbose_name='总数量',null=True,blank=True)
    description=models.CharField(max_length=200,blank=True,verbose_name='描述')
    def __str__(self):
        return self.number
    class Meta:
        verbose_name = '场地'
        verbose_name_plural = '场地' 


class FactoryPosition(models.Model):
    '''场地仓位表'''
    areaowner=models.ForeignKey(FactoryArea,verbose_name='所属场地') 
    name=models.CharField(max_length=60,verbose_name='名称')
    number=models.CharField(max_length=60,verbose_name='编号')
    area=models.FloatField(verbose_name='面积',null=True,blank=True)
    length=models.FloatField(verbose_name='长度',null=True,blank=True)
    width=models.FloatField(verbose_name='宽度',null=True,blank=True)
    description=models.CharField(max_length=200,verbose_name='描述',null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '场地仓位'
        verbose_name_plural = '场地仓位'  


class UnitProject(models.Model):
    '''单位工程表'''
    name=models.CharField(max_length=60,verbose_name='名称')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '单位工程'
        verbose_name_plural = '单位工程'  
    
class Elevation(models.Model):
    '''标高表'''
    name=models.CharField(max_length=60,verbose_name='名称')
    level=models.FloatField(verbose_name='标高',null=True,blank=True) 
    sign=models.CharField(max_length=60,verbose_name='标记',null=True,blank=True)  
    unitproject=models.ForeignKey(UnitProject,verbose_name='单位工程')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '标高'
        verbose_name_plural = '标高'  
        ordering = ['unitproject']

class PBMaterial(models.Model):
    '''构件材料表'''
    MATERIAL_TYPE_CHOICES = (
        ('钢材', '钢材'),
        ('混泥土', '混泥土'),
        ('钢筋', '钢筋'),
    )
    name = models.CharField(max_length=20,choices=MATERIAL_TYPE_CHOICES,verbose_name='类型')
    specification = models.CharField(max_length=30,verbose_name='规格',null=True,blank=True)
    size = models.CharField(max_length=30,verbose_name='材料尺寸',null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '构件材料'
        verbose_name_plural = '构件材料' 
    
class PBType(models.Model):
    '''构件类型表'''
    name=models.CharField(max_length=60,verbose_name='名称')
    material=models.ForeignKey(PBMaterial,verbose_name='材料',null=True)
    major=CrossDbForeignKey(UserMajor,verbose_name='专业',null=True,blank=True)
    classfication_code=models.CharField(max_length=64,verbose_name='分类编码',null=True,blank=True)
    sign=models.CharField(max_length=60,verbose_name='标记',null=True,blank=True)
    familyname=models.CharField(max_length=60,verbose_name='族名称',null=True,blank=True)
    description=models.CharField(max_length=200,verbose_name='描述',null=True,blank=True)
    isprebuilt =models.BooleanField(verbose_name='是否预制',default=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '构件类型'
        verbose_name_plural = '构件类型' 

class StatusCountType(models.Model):
    '''统计类型表'''
    name=models.CharField(max_length=60,verbose_name='类型名称')
    rendercolor=models.CharField(max_length=20)
    sequence = models.IntegerField(verbose_name='序号',default=0)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '统计类型'
        verbose_name_plural = '统计类型'
    
class PBStatus(models.Model):
    '''构件状态表'''
    statusname=models.CharField(max_length=60,verbose_name='状态名称')
    factoryarea=models.ForeignKey(FactoryArea,verbose_name='所属场地',null=True,blank=True,on_delete=models.SET_NULL)
    pbtype=models.ForeignKey(PBType,verbose_name='构件类型',null=True,blank=True,on_delete=models.SET_NULL)
    nextstatus=models.ForeignKey('self',related_name='pbstatus_nextstatus',verbose_name='下一状态',null=True,blank=True,on_delete=models.SET_NULL)
    sequence = models.IntegerField(verbose_name='序号',default=0)
    relatedformtemplate = models.ForeignKey(BiaoDanMuBan, blank=True, null=True)
    relatedflowtemplate = models.ForeignKey('FlowTemplate', blank=True, null=True)
    detailcounttype = models.ForeignKey(StatusCountType,related_name='detailcounttypepb', blank=True, null=True,on_delete=models.SET_NULL)
    roughcounttype = models.ForeignKey(StatusCountType,related_name='roughcounttypepb', blank=True, null=True,on_delete=models.SET_NULL)
    isqualify = models.BooleanField(verbose_name='是否不合格',default=False)
    relatedstatus = models.ForeignKey('self',related_name='pbstatus_relatedstatus', blank=True, null=True)
    iscritical = models.BooleanField(verbose_name='是否完成状态',default=False)
    def __str__(self):
        if self.pbtype:
            return self.pbtype.name+"-"+self.statusname
        else:
            return self.statusname
    class Meta:
        verbose_name = '构件状态'
        verbose_name_plural = '构件状态'
    
class PrecastBeam(models.Model):
    '''构件表'''
    guid=models.CharField(max_length=64,unique=True,verbose_name='GUID')
    revitfilename=models.CharField(max_length=60,verbose_name='Revit文件名',null=True,blank=True)
    elementid=models.CharField(max_length=60,verbose_name='ElementID',null=True,blank=True)
    lvmdbid=models.IntegerField(verbose_name='LvmDbId',null=True,blank=True)
    number=models.CharField(max_length=64,verbose_name='编号')
    pbtype=models.ForeignKey(PBType,verbose_name='构件类型',null=True,blank=True,on_delete=models.SET_NULL)
    curstatus=models.ForeignKey(PBStatus,null=True,blank=True,verbose_name='当前状态',on_delete=models.SET_NULL)
    curstatustime=models.DateTimeField(verbose_name='当前状态时间',blank=True, null=True)
    curstatusdesc=models.CharField(max_length=200,verbose_name='当前状态描述',blank=True,null=True)
    curstatuspercent = models.FloatField(verbose_name='工序完成百分比',blank=True,null=True,default=0)
    weight=models.FloatField(verbose_name='重量',null=True,blank=True)
    volume=models.FloatField(verbose_name='体积',null=True,blank=True)
    width=models.FloatField(verbose_name='宽度',null=True,blank=True)
    height=models.FloatField(verbose_name='高度',null=True,blank=True)
    length=models.FloatField(verbose_name='长度',null=True,blank=True)
    sign=models.CharField(max_length=60,verbose_name='标记',null=True,blank=True)
    elevation=models.ForeignKey(Elevation,verbose_name='楼层',null=True,on_delete=models.SET_NULL)  
    description=models.CharField(max_length=512,verbose_name='描述',blank=True,null=True)
    drawnumber=models.CharField(max_length=60,verbose_name='图纸编号',blank=True,null=True)
    task=models.ForeignKey("ProjectTask",verbose_name='所属任务',null=True,blank=True,on_delete=models.SET_NULL)
    pbpostion=models.CharField(max_length=64,blank=True,null=True,verbose_name='位置字符串')
    parentguid=models.CharField(max_length=64,blank=True,null=True,verbose_name='父构件GUID')
    curfactoryposition=models.ForeignKey(FactoryPosition,verbose_name='当前场地仓位',null=True,blank=True,on_delete=models.SET_NULL)
    parent = models.ForeignKey('self',verbose_name='父构件', blank=True, null=True)
    donepercent = models.FloatField(verbose_name='完成百分比',blank=True,null=True,default=0)
    zone=models.ForeignKey('Zone',verbose_name='区域',null=True,blank=True)

    def __str__(self):
        return self.number
    class Meta:
        verbose_name = '构件'
        verbose_name_plural = '构件'


class User2PBStatus(models.Model):
    '''用户构件状态权限表'''
    user=CrossDbForeignKey(User,verbose_name='用户')
    status=models.ForeignKey(PBStatus,verbose_name='构件状态')
    def __str__(self):
        return self.user.name+self.status
    class Meta:
        unique_together = ( ("user", "status"), )
        verbose_name = '用户构件状态'
        verbose_name_plural = '用户构件状态'
        
class PBStatusRecord(models.Model):
    '''构件状态记录表'''
    status=models.ForeignKey(PBStatus,verbose_name='状态')
    precastbeam=models.ForeignKey(PrecastBeam,verbose_name='构件')
    actor=CrossDbForeignKey(User,verbose_name='用户')
    factoryposition=models.ForeignKey(FactoryPosition,verbose_name='场地仓位',blank=True,null=True)
    time=models.DateTimeField(verbose_name='时间')
    description=models.CharField(max_length=200,verbose_name='描述',blank=True,null=True)
    isactive = models.BooleanField(verbose_name='是否有效',default=True)
    longitude = models.FloatField(verbose_name='经度',blank=True,null=True)
    latitude = models.FloatField(verbose_name='纬度',blank=True,null=True)
    compgroup=models.ForeignKey('CompGroup',verbose_name='关联组',blank=True, null=True) 
    related_form = models.ForeignKey(BiaoDan, blank=True, null=True)
    related_formfile = models.ForeignKey('Document', blank=True, null=True)
    percentage = models.FloatField(verbose_name='完成百分比',blank=True,null=True,default=100)
    class Meta:
        verbose_name = '构件状态记录表'
        verbose_name_plural = '构件状态记录表'


class Pbgroup(models.Model):
    '''构件分组表'''
    number = models.CharField(max_length=64,verbose_name='编号')
    name = models.CharField(max_length=64,verbose_name='组名')
    pbtype = models.ForeignKey(PBType, blank=True, null=True,verbose_name='类型')
    zone = models.ForeignKey('Zone', blank=True, null=True,verbose_name='所属分区')
    curstatus=models.ForeignKey(PBStatus,null=True,blank=True,verbose_name='当前状态')
    curstatustime=models.DateTimeField(verbose_name='当前状态时间')
    class Meta:
        managed = False
        db_table = 'taskandflow_pbgroup'


class Pbgrouprelation(models.Model):
    pbgroup = models.ForeignKey(Pbgroup)
    pb = models.ForeignKey(PrecastBeam)

    class Meta:
        managed = False
        db_table = 'taskandflow_pbgrouprelation'


class Pbstatusremind(models.Model):
    pbstatus = models.ForeignKey(PBStatus,related_name='remind_pbstatus',verbose_name='触发状态')
    next_status = models.ForeignKey(PBStatus,related_name='remind_next_status',verbose_name='下一状态')
    time_span = models.IntegerField(verbose_name='时间间隔（小时）')

    def __str__(self):
        return self.pbstatus.__str__()

    class Meta:
        managed = False
        db_table = 'taskandflow_pbstatusremind'
        verbose_name = '工序验收提醒'
        verbose_name_plural = '工序验收提醒'   



class Pbtypetimedcheck(models.Model):
    '''构件类型定时检查表'''
    name = models.CharField(verbose_name='检查名称',max_length=64, blank=True)
    pbtype = models.ForeignKey(PBType,verbose_name='构件类型')
    task_cycle_type = models.CharField(max_length=12,verbose_name='周期类型')
    task_cycle = models.CharField(max_length=64,verbose_name='周期',null=True,blank=True)
    relatedformtemplate = models.ForeignKey(BiaoDanMuBan,verbose_name='检查表单', blank=True, null=True)
    status_reset_time = models.DateTimeField(verbose_name='重置时间',null=True,blank=True)
    isneedcheck = models.BooleanField(verbose_name='是否待检',default=False)

    class Meta:
        verbose_name = '构件类型定时检查'
        verbose_name_plural = '构件类型定时检查'
        managed = False
        db_table = 'taskandflow_pbtypetimedcheck'

class PbtimedcheckRecord(models.Model):
    '''构件检查记录表'''
    timedcheck=models.ForeignKey(Pbtypetimedcheck,verbose_name='类型检查')
    monitoring = models.ForeignKey('Monitoringelement', blank=True, null=True,verbose_name='监控元素')
    actor=CrossDbForeignKey(User,verbose_name='用户',blank=True,null=True)
    time=models.DateTimeField(verbose_name='时间',blank=True,null=True)
    description=models.CharField(max_length=200,verbose_name='描述',blank=True,null=True)
    related_form = models.ForeignKey(BiaoDan, blank=True, null=True)
    related_formfile = models.ForeignKey('Document', blank=True, null=True)
    status_reset_time = models.DateTimeField(verbose_name='重置时间')
    isneedcheck = models.BooleanField(verbose_name='是否待检',default=True)
    class Meta:
        verbose_name = '构件检查记录表'
        verbose_name_plural = '构件检查记录表'
        db_table = 'taskandflow_pbtimedcheckrecord'

class PbtypeUser(models.Model):
    pbtype = models.ForeignKey(PBType)
    user = CrossDbForeignKey(User)

    class Meta:
        managed = False
        db_table = 'taskandflow_pbtype_user'
        
#任务管理------------------------------------------
class TaskType(models.Model):
    '''任务类型表'''
    name=models.CharField(max_length=60,verbose_name='名称')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '任务类型'
        verbose_name_plural = '任务类型'

        
class TaskStatus(models.Model):
    '''任务状态表'''
    statusname=models.CharField(max_length=60,verbose_name='状态名称')
    tasktype=models.ForeignKey(TaskType,verbose_name='任务类型',null=True,blank=True)
    nextstatus=models.ForeignKey('self',verbose_name='下一状态',null=True,blank=True)
    relatedformtemplate = models.ForeignKey(BiaoDanMuBan, blank=True, null=True)
    relatedflowtemplate = models.ForeignKey('FlowTemplate', blank=True, null=True)
    detailcounttype = models.ForeignKey('StatusCountType',related_name='detailcounttypetask', blank=True, null=True)
    roughcounttype = models.ForeignKey('StatusCountType',related_name='roughcounttypetask', blank=True, null=True)
    def __str__(self):
        return self.statusname
    class Meta:
        verbose_name = '任务状态'
        verbose_name_plural = '任务状态'


class ProjectTask(models.Model):
    '''任务表'''
    msprojectid=models.CharField(max_length=40,blank=True,verbose_name='')
    name = models.CharField(max_length=60,verbose_name='任务名称')
    parentid=models.ForeignKey('self',verbose_name='父节点',null=True,blank=True)
    planstart=models.DateTimeField(verbose_name='计划开始时间')
    planfinish=models.DateTimeField(verbose_name='计划结束时间')
    actualstart=models.DateTimeField(null=True,blank=True,verbose_name='实际开始时间')
    acutalfinish=models.DateTimeField(null=True,blank=True,verbose_name='实际结束时间')
    constructionunit = CrossDbForeignKey(Company,verbose_name='施工单位',null=True,blank=True)
    major=CrossDbForeignKey(UserMajor,verbose_name='专业',null=True,blank=True)
    curstatus=models.ForeignKey(TaskStatus,verbose_name='当前状态',null=True,blank=True)
    percentage=models.FloatField(verbose_name='完成百分比',default=0)
    ismilestone = models.BooleanField(verbose_name='是否里程碑节点',default=False)  
    iskeypath = models.BooleanField(verbose_name='是否关键路径',default=False)
    description=models.CharField(max_length=200,verbose_name='描述',null=True,blank=True)
    type = models.ForeignKey(TaskType,verbose_name='类型')
    taskpath=models.CharField(max_length=256,verbose_name='任务路径',null=True,blank=True)
    relatestatus=models.ForeignKey(PBStatus,verbose_name='关联工序',null=True,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '生产任务'
        verbose_name_plural = '生产任务'

class ProjectTaskHazard(models.Model):
    projecttask = models.ForeignKey(ProjectTask,verbose_name='关联任务',null=True)
    technical = models.ForeignKey('Technical',verbose_name='关联方案',null=True)
    hazard_code = models.CharField(max_length=24, blank=True, null=True)
    relatedspace_type = models.CharField(max_length=60, blank=True)
    relatedspace_id = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'taskandflow_projecttask_hazard'

class User2TaskStatus(models.Model):
    '''用户任务状态权限表'''
    user=CrossDbForeignKey(User,verbose_name='用户')
    status=models.ForeignKey(TaskStatus,verbose_name='任务状态')
    def __str__(self):
        return self.status.name
    class Meta:
        unique_together = ( ("user", "status"), )
        verbose_name = '用户任务状态'
        verbose_name_plural = '用户任务状态'
        

class TaskStatusRecord(models.Model):
    '''任务状态记录表'''
    status=models.ForeignKey(TaskStatus,verbose_name='状态')
    task=models.ForeignKey(ProjectTask,verbose_name='任务')
    actor=CrossDbForeignKey(User,verbose_name='用户')
    time=models.DateTimeField(auto_now_add=True,verbose_name='时间')
    description=models.CharField(max_length=200,verbose_name='描述',blank=True)
    class Meta:
        unique_together = ( ("status", "task"), )
        verbose_name = '任务状态记录'
        verbose_name_plural = '任务状态记录'



class Projectversion(models.Model):
    version_code = models.CharField(max_length=64)
    update_time = models.DateTimeField(auto_now_add=True)
    isworkinigversion = models.BooleanField(default=False)
    label = models.CharField(max_length=64, blank=True)
    update_user = CrossDbForeignKey(User)
    description = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_projectversion'



class Oldprojecttaskbackup(models.Model):
    '''旧任务备份'''
    msprojectid = models.CharField(max_length=40)
    name = models.CharField(max_length=60)
    planstart = models.DateTimeField()
    planfinish = models.DateTimeField()
    actualstart = models.DateTimeField(blank=True, null=True)
    acutalfinish = models.DateTimeField(blank=True, null=True)
    percentage = models.FloatField()
    ismilestone = models.BooleanField(verbose_name='是否里程碑节点',default=False)  
    iskeypath = models.BooleanField(verbose_name='是否关键路径',default=False)
    description=models.CharField(max_length=200,verbose_name='描述',null=True,blank=True)
    parentid=models.ForeignKey('self',verbose_name='父节点',null=True,blank=True)
    constructionunit = CrossDbForeignKey(Company,verbose_name='施工单位',null=True,blank=True)
    major=CrossDbForeignKey(UserMajor,verbose_name='专业',null=True,blank=True)
    curstatus=models.ForeignKey(TaskStatus,verbose_name='当前状态',null=True,blank=True)
    type = models.ForeignKey(TaskType,verbose_name='类型')
    taskpath=models.CharField(max_length=256,verbose_name='任务路径',null=True,blank=True)
    projectversion = models.ForeignKey('Projectversion')
    relatednewtask = models.ForeignKey(ProjectTask, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_oldprojecttaskbackup'


class Projectupdatefiles(models.Model):
    projectversion=models.ForeignKey(Projectversion)
    file = models.ForeignKey('Document')

    class Meta:
        managed = False
        db_table = 'taskandflow_projectupdatefiles'

class Oldprojecttaskpb(models.Model):
    oldprojecttask = models.ForeignKey(Oldprojecttaskbackup)
    pb = models.ForeignKey(PrecastBeam)

    class Meta:
        managed = False
        db_table = 'taskandflow_oldprojecttaskpb'


class Projecttaskrelationtype(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'taskandflow_projecttaskrelationtype'


class Projecttaskrelation(models.Model):
    pretask = models.ForeignKey(ProjectTask,related_name='pretask')
    suctask = models.ForeignKey(ProjectTask,related_name='suctask')
    projecttaskrelationtype = models.ForeignKey('Projecttaskrelationtype')

    class Meta:
        managed = False
        db_table = 'taskandflow_projecttaskrelation'





#流程管理------------------------------------------
class FlowType(models.Model):
    '''流程类型表'''
    name=models.CharField(max_length=60,verbose_name='流程类型名称')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '流程类型'
        verbose_name_plural = '流程类型'
        
class FlowTemplate(models.Model):
    '''流程模板表'''
    name = models.CharField(max_length=60,verbose_name='流程模板名称')
    major = CrossDbForeignKey(UserMajor,verbose_name='专业')
    flowtype = models.ForeignKey(FlowType,verbose_name='流程类型')
    describe = models.CharField(max_length=120,verbose_name='模板描述')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '流程模板'
        verbose_name_plural = '流程模板'
 
class FlowTemplateUser(models.Model):
    '''流程模板浏览者表'''
    template= models.ForeignKey(FlowTemplate,verbose_name='流程模板')
    user = CrossDbForeignKey(User,verbose_name='用户')

    def __str__(self):
        return self.template.name
    class Meta:
        verbose_name = '流程模板浏览者'
        verbose_name_plural = '流程模板浏览者'
        db_table = 'taskandflow_flowtemplate_user'        
        
class FlowTemplateStep(models.Model):
    '''流程模板步骤表'''
    name = models.CharField(max_length=60,verbose_name='流程名称')
    template= models.ForeignKey(FlowTemplate,verbose_name='所属模板',related_name='templateSteps')
    isstartstep = models.BooleanField(verbose_name='是否起始步骤',default=False)  
    isendstep = models.BooleanField(verbose_name='是否结束步骤',default=False)
    isautotransfer = models.BooleanField(verbose_name='是否自动流转',default=True)
    istimeouttransfer = models.BooleanField(verbose_name='是否超时流转',default=True)
    maxDuration = models.IntegerField(verbose_name='工期',default=0)
    sequence = models.IntegerField(verbose_name='序号',default=0)
    relatedformtemplate = models.ForeignKey(BiaoDanMuBan,verbose_name='关联表单',blank=True, null=True)
    defaultcomment = models.CharField(max_length=200,verbose_name='审批意见',blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '流程模板步骤'
        verbose_name_plural = '流程模板步骤'
        

class FlowStepUser(models.Model):
    '''流程模板步骤人员表'''
    user = CrossDbForeignKey(User,verbose_name='用户')
    flowstep= models.ForeignKey(FlowTemplateStep,verbose_name='所属流程步骤')
    isactor = models.BooleanField(verbose_name='是否执行者',default=True) 
#    def __str__(self):
#        return self.name
    class Meta:
        verbose_name = '流程模板步骤人员'
        verbose_name_plural = '流程模板步骤人员'

class ActorType(models.Model):
    '''执行者情况表'''
    name=models.CharField(max_length=60,verbose_name='执行者情况')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '执行者情况'
        verbose_name_plural = '执行者情况'
    
class FlowStepOperation(models.Model):
    '''流程模板步骤操作表'''
    name = models.CharField(max_length=60,verbose_name='操作名称')
    flowstep= models.ForeignKey(FlowTemplateStep,related_name='flowstep',verbose_name='所属流程步骤')
    actortype= models.ForeignKey(ActorType,verbose_name='执行者情况')
    nextflowstep= models.ForeignKey(FlowTemplateStep,related_name='nextflowstep',verbose_name='下一步骤')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '流程模板步骤操作'
        verbose_name_plural = '流程模板步骤操作'

RELATE_TYPE_CHOICES = (
        ('构件', '构件'),
        ('任务', '任务'),
        ('事件', '事件'),
        ('事件步骤操作', '事件步骤操作'),
        ('施工机械', '施工机械'),
        ('流程步骤', '流程步骤'),
        ('重大危险源修改记录', '重大危险源修改记录'),
        ('施工机械状态修改记录', '施工机械状态修改记录'),
        ('构件状态修改记录', '构件状态修改记录'),
        ('任务状态修改记录', '任务状态修改记录'),
        ('危险源事件', '危险源事件'),
    )    

PRIORTITY_CHOICES = (
        (1, '轻微'),
        (5, '一般'),
        (10, '严重'),
    ) 
class projectevent(models.Model):
    '''事件表'''
    number = models.CharField(max_length=60,verbose_name='问题编号')
    title = models.CharField(max_length=120,verbose_name='标题',default='')
    describe = models.CharField(max_length=256,verbose_name='描述')
    deadline = models.DateTimeField(verbose_name='截止时间')
    priority = models.IntegerField(verbose_name='优先级',default=1)
    curflowstep= models.ForeignKey(FlowTemplateStep,verbose_name='当前流程步骤')
    updatetime = models.DateTimeField(verbose_name='更新时间',blank=True, null=True)
    template= models.ForeignKey(FlowTemplate,verbose_name='流程模板')
    voicedoc= models.ForeignKey("Document",verbose_name='声音文档',blank=True, null=True)
    relatedmonitoringelement = models.ForeignKey("Monitoringelement",verbose_name='过程监控元素',blank=True, null=True)
    pbstatus = models.ForeignKey("PBStatus",verbose_name='关联状态',blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间',blank=True, null=True)
    createuser =CrossDbForeignKey(User,verbose_name='创建人',related_name='createuser',blank=True, null=True)
    issave = models.BooleanField(verbose_name='是否保存',default=False)
    saveuser =CrossDbForeignKey(User,verbose_name='保存人',related_name='saveuser',blank=True, null=True)
    savecomment = models.CharField(max_length=200,verbose_name='意见',blank=True, null=True)
    curdealstep = models.IntegerField(verbose_name='处理阶段',default=1) #1:未处理 2：处理中 3：已结束
    extend = models.CharField(max_length=256,verbose_name='扩展参数',blank=True, null=True)

    def __str__(self):
        return self.describe
    class Meta:
        verbose_name = '事件'
        verbose_name_plural = '事件'
        db_table = 'taskandflow_projectevent'
    @staticmethod
    def get_priority_desc(priority):
        priority_desc=''
        for Choices in PRIORTITY_CHOICES:
            if  Choices[0]== priority:
                priority_desc=Choices[1]
                break
        return priority_desc


class ProjecteventElement(models.Model):
    typetable = models.CharField(max_length=96, blank=True)
    relatedid = models.IntegerField(blank=True, null=True)
    event = models.ForeignKey(projectevent, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_projectevent_element'

class Eventstep(models.Model):
    '''事件步骤表'''
    flowstep= models.ForeignKey(FlowTemplateStep,verbose_name='流程步骤')
    projectevent = models.ForeignKey(projectevent,verbose_name='事件')
    starttime = models.DateTimeField(auto_now_add=True,verbose_name='开始时间')
    endtime = models.DateTimeField(verbose_name='完成时间',blank=True, null=True)
    relatedform = models.ForeignKey(BiaoDan, blank=True, null=True)
    formfile = models.ForeignKey('Document', blank=True, null=True)
    class Meta:
        verbose_name = '事件步骤'
        verbose_name_plural = '事件步骤'
    
class EventStepOperation(models.Model):
    '''事件步骤操作表'''
    flowstepoper= models.ForeignKey(FlowStepOperation,verbose_name='流程模板步骤操作',blank=True, null=True)
    eventstep= models.ForeignKey(Eventstep,verbose_name='所属事件步骤')
    oprtime = models.DateTimeField(auto_now_add=True,verbose_name='操作时间')
    actor= CrossDbForeignKey(User,verbose_name='操作人')
    comment = models.CharField(max_length=200,verbose_name='评论',blank=True, null=True)
    def __str__(self):
        return self.comment
    class Meta:
        verbose_name = '事件步骤操作'
        verbose_name_plural = '事件步骤操作'

#文档管理------------------------------------------    
class Directory(models.Model):
    '''目录表'''
    name = models.CharField(max_length=120,verbose_name='名称')
    parent = models.ForeignKey('self',verbose_name='父目录',blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    creator= CrossDbForeignKey(User,verbose_name='创建人')
    islock = models.BooleanField(verbose_name='是否锁定',default=False)
    index = models.SmallIntegerField(blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '目录'
        verbose_name_plural = '目录'


class DirectoryCompany(models.Model):
    directory = models.ForeignKey(Directory)
    company = CrossDbForeignKey(Company)

    class Meta:
        managed = False
        db_table = 'taskandflow_directory_company'


class DirectoryRole(models.Model):
    directory = models.ForeignKey(Directory)
    role = models.ForeignKey(Role)

    class Meta:
        managed = False
        db_table = 'taskandflow_directory_role'


class DirectoryUser(models.Model):
    directory = models.ForeignKey(Directory)
    user = CrossDbForeignKey(User)
    auth = models.IntegerField(verbose_name='权限',default=4)

    class Meta:
        managed = False
        db_table = 'taskandflow_directory_user'

class DirectoryNotifyuser(models.Model):
    directory = models.ForeignKey(Directory)
    notifyuser = CrossDbForeignKey(User)

    class Meta:
        managed = False
        db_table = 'taskandflow_directory_notifyuser'

class Document(models.Model):
    '''文档表'''
    DOCTYPE_CHOICES = (
        ('normal', '常规文档'),
        ('quality', '质量文档'),
        ('technical', '技术方案'),
    )
    name = models.CharField(max_length=120,verbose_name='名称')
    shortname = models.CharField(max_length=60,verbose_name='简称')
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    creator= CrossDbForeignKey(User,verbose_name='创建人')
    version = models.DateTimeField(verbose_name='版本',blank=True, null=True)
    filepath = models.CharField(max_length=128,verbose_name='路径')
    docdirectory= models.ManyToManyField(Directory,verbose_name='所在目录')
    filesize = models.IntegerField(verbose_name='文件大小',default=0)
    filetype = models.CharField(max_length=120,verbose_name='文件类型',default="image/jpeg")
    doctype = models.CharField(max_length=20,choices=DOCTYPE_CHOICES)
    remark = models.CharField(max_length=360,verbose_name='备注',blank=True, null=True)
    previewfile = models.CharField(max_length=120,verbose_name='预览文件',blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档'



class DocumentNotifyuser(models.Model):
    document = models.ForeignKey(Document)
    notifyuser = CrossDbForeignKey(User)

    class Meta:
        managed = False
        db_table = 'taskandflow_document_notifyuser'

class Doc2Relate(models.Model):
    '''文档关联表'''
    document= models.ForeignKey(Document,verbose_name='文档')
    relatetype = models.CharField(max_length=60,verbose_name='关联元素类型',choices=RELATE_TYPE_CHOICES,blank=True, null=True)
    relateid = models.IntegerField(verbose_name='元素编号',blank=True, null=True)
    creator= CrossDbForeignKey(User,verbose_name='关联人')
    createtime = models.DateTimeField(auto_now_add=True,verbose_name='关联时间')
    class Meta:
        verbose_name = '文档关联表'
        verbose_name_plural = '文档关联表'
        

#施工机械管理------------------------------------------    
class CMType(models.Model):
    '''施工机械类型表'''
    name=models.CharField(max_length=60,verbose_name='名称')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '施工机械类型'
        verbose_name_plural = '施工机械类型'

        
class CMStatus(models.Model):
    '''施工机械状态表'''
    statusname=models.CharField(max_length=60,verbose_name='状态名称')
    cmtype=models.ForeignKey(CMType,verbose_name='所属类型',null=True)
    nextstatus=models.ForeignKey('self',verbose_name='下一状态',null=True,blank=True)
    relatedformtemplate = models.ForeignKey(BiaoDanMuBan, blank=True, null=True)
    relatedflowtemplate = models.ForeignKey('Flowtemplate', blank=True, null=True)
    detailcounttype = models.ForeignKey('StatusCountType', related_name='detailcounttypecmstatus',blank=True, null=True)
    roughcounttype = models.ForeignKey('StatusCountType', related_name='roughcounttypecmstatus',blank=True, null=True)
    def __str__(self):
        return self.statusname
    class Meta:
        verbose_name = '施工机械状态'
        verbose_name_plural = '施工机械状态'


class ConstructionMachine(models.Model):
    '''施工机械'''
    name=models.CharField(max_length=64,verbose_name='名称')
    number=models.CharField(max_length=64,unique=True,verbose_name='编号')
    cmtype=models.ForeignKey(CMType,verbose_name='所属类型')
    elementid=models.CharField(max_length=60,verbose_name='ElementID',null=True,blank=True)
    uniqueid=models.CharField(max_length=60,verbose_name='uniqueID',null=True,blank=True)
    postion=models.CharField(max_length=64,verbose_name='位置',null=True,blank=True) 
    responsunit= CrossDbForeignKey(Company,verbose_name='负责单位',null=True,blank=True)
    usage=models.CharField(max_length=120,verbose_name='用途',null=True,blank=True)
    specification = models.CharField(max_length=30,verbose_name='规格',null=True,blank=True)
    high=models.FloatField(verbose_name='高度',null=True,blank=True)
    curstatus=models.ForeignKey(CMStatus,verbose_name='当前状态')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '施工机械'
        verbose_name_plural = '施工机械'


class User2CMStatus(models.Model):
    '''用户施工机械状态权限表'''
    user=CrossDbForeignKey(User,verbose_name='用户')
    status=models.ForeignKey(CMStatus,verbose_name='施工机械状态')
    class Meta:
        unique_together = ( ("user", "status"), )
        verbose_name = '用户施工机械状态'
        verbose_name_plural = '用户施工机械状态'
        

class CMStatusRecord(models.Model):
    '''施工机械状态记录表'''
    status=models.ForeignKey(CMStatus,verbose_name='状态')
    constructionmachine=models.ForeignKey(ConstructionMachine,verbose_name='施工机械')
    actor=CrossDbForeignKey(User,verbose_name='用户')
    time=models.DateTimeField(auto_now_add=True,verbose_name='时间')
    description=models.CharField(max_length=200,verbose_name='描述',null=True,blank=True)
    related_form = models.ForeignKey(BiaoDan, blank=True, null=True)
    related_formfile = models.ForeignKey(Document, blank=True, null=True)
    class Meta:
        unique_together = ( ("status", "constructionmachine"), )
        verbose_name = '施工机械状态记录'
        verbose_name_plural = '施工机械状态记录'


class Cmkeypoint(models.Model):
    '''施工机械控制点'''
    name = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=128, blank=True)
    cm = models.ForeignKey(ConstructionMachine, blank=True, null=True)
    isundercontrol = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_cmkeypoint'

#重大危险源管理------------------------------------------    
class HazardType(models.Model):
    '''重大危险源类型表'''
    name=models.CharField(max_length=60,verbose_name='名称')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '重大危险源类型'
        verbose_name_plural = '重大危险源类型'

        
class HazardStatus(models.Model):
    '''重大危险源状态表'''
    statusname=models.CharField(max_length=60,verbose_name='状态名称')
    nextstatus=models.ForeignKey('self',verbose_name='下一状态',null=True,blank=True)
    relatedformtemplate = models.ForeignKey(BiaoDanMuBan, blank=True, null=True)
    detailcounttype = models.ForeignKey(StatusCountType,related_name='detailcounttypehazard', blank=True, null=True)
    roughcounttype = models.ForeignKey(StatusCountType,related_name='roughcounttypehazard', blank=True, null=True)
    def __str__(self):
        return self.statusname
    class Meta:
        verbose_name = '重大危险源状态'
        verbose_name_plural = '重大危险源状态'

class Hazardlisthistory(models.Model):
    his_date = models.DateField(unique=True)
    title = models.CharField(max_length=128, blank=True)
    is_current = models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'taskandflow_hazardlisthistory'

class Hazardevent(models.Model):
    '''危险源事件'''
    hazard_code = models.CharField(max_length=24, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    major = CrossDbForeignKey(UserMajor, blank=True, null=True)
    curstatus = models.ForeignKey(HazardStatus, blank=True, null=True)
    responsunit = CrossDbForeignKey(Company, blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True, null=True)
    relatedele_type = models.CharField(max_length=60, blank=True, null=True)
    relatedele_id = models.IntegerField(blank=True,  null=True)
    relatedspace_type = models.CharField(max_length=60, blank=True, null=True)
    relatedspace_id = models.IntegerField(blank=True, null=True)
    ownerlist = models.ForeignKey(Hazardlisthistory, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True,verbose_name='持续时间')
    his_date = models.DateField()
    class Meta:
        managed = False
        db_table = 'taskandflow_hazardevent'
        unique_together = ( ("hazard_code", "relatedspace_type","relatedspace_id","his_date"), )


class User2HazardStatus(models.Model):
    '''用户重大危险源状态权限表'''
    user=CrossDbForeignKey(User,verbose_name='用户')
    status=models.ForeignKey(HazardStatus,verbose_name='重大危险源状态')
    def __str__(self):
        return self.status
    class Meta:
        unique_together = ( ("user", "status"), )
        verbose_name = '用户重大危险源状态'
        verbose_name_plural = '用户重大危险源状态'
        

class HazardStatusRecord(models.Model):
    '''重大危险源状态记录表'''
    status=models.ForeignKey(HazardStatus,verbose_name='状态')
    hazard_code = models.CharField(max_length=24, blank=True, null=True,verbose_name='重大危险源')
    actor=CrossDbForeignKey(User,verbose_name='用户')
    time=models.DateTimeField(auto_now_add=True,verbose_name='时间')
    description=models.CharField(max_length=200,verbose_name='描述',blank=True, null=True)
    related_form = models.ForeignKey(BiaoDan, blank=True, null=True)
    related_formfile = models.ForeignKey(Document, blank=True, null=True)
    class Meta:
        unique_together = ( ("status", "hazard_code"), )
        verbose_name = '重大危险源状态记录'
        verbose_name_plural = '重大危险源状态记录'    
        



#消息管理------------------------------------------        
class MessageType(models.Model):
    '''消息类型表'''
    name=models.CharField(max_length=60,verbose_name='名称')
    priority= models.IntegerField(verbose_name='重要性',default=0)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '消息类型'
        verbose_name_plural = '消息类型'


class Message(models.Model):
    '''消息表'''
    receiver=CrossDbForeignKey(User,related_name='receiver',verbose_name='接收人')
    message=models.CharField(max_length=240,verbose_name='内容')
    sender=CrossDbForeignKey(User,related_name='sender',verbose_name='发起人')
    isread = models.BooleanField(verbose_name='是否已读',default=False)
    readtime=models.DateTimeField(auto_now_add=True,verbose_name='读取时间')
    sendtime=models.DateTimeField(auto_now_add=True,verbose_name='发起时间')
    type=models.ForeignKey(MessageType,verbose_name='类型')
    relatetype = models.CharField(max_length=60,verbose_name='关联元素类型',choices=RELATE_TYPE_CHOICES,blank=True, null=True)
    relateid = models.IntegerField(verbose_name='元素编号',blank=True, null=True)
    def __str__(self):
        return self.message
    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'

class Notice(models.Model):
    '''通知表'''
    title=models.CharField(max_length=40,verbose_name='标题')
    message=models.CharField(max_length=400,verbose_name='内容')
    sender=CrossDbForeignKey(User,verbose_name='发起人')
    time=models.DateTimeField(auto_now_add=True,verbose_name='时间')
    expire=models.DateTimeField(verbose_name='过期时间',blank=True, null=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        
class CustomInfo(models.Model):
    '''用户自定义信息表'''
    infotype = models.CharField(max_length=20)
    custominfo = models.CharField(max_length=120,blank=True, null=True)
    def __str__(self):
        return self.infotype
    class Meta:
        verbose_name = '用户自定义信息'
        verbose_name_plural = '用户自定义信息'



class PushMessage(models.Model):
    '''推送消息表'''
    touser=CrossDbForeignKey(User,related_name='touser',verbose_name='接收人',blank=True, null=True)
    title=models.CharField(max_length=120,verbose_name='标题',blank=True, null=True)
    message=models.CharField(max_length=240,verbose_name='内容',blank=True, null=True)
    fromuser=CrossDbForeignKey(User,related_name='fromuser',verbose_name='发起人',blank=True, null=True)
    status = models.IntegerField(verbose_name='状态',blank=True, null=True)
    createtime=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    pushtime=models.DateTimeField(verbose_name='推送时间',blank=True, null=True)
    readtime=models.DateTimeField(verbose_name='读取时间',blank=True, null=True)
    relatetype = models.CharField(max_length=60,verbose_name='关联元素类型',choices=RELATE_TYPE_CHOICES,blank=True, null=True)
    relateid = models.IntegerField(verbose_name='元素编号',blank=True, null=True)
    toparty = models.IntegerField(verbose_name='部门编号',blank=True, null=True)
    totag = models.IntegerField(verbose_name='标签编号',blank=True, null=True)
    agentid = models.IntegerField(verbose_name='应用编号',blank=True, null=True)
    def __str__(self):
        return self.message
    class Meta:
        verbose_name = '推送消息'
        verbose_name_plural = '推送消息'
        

class CompGroupType(models.Model):
    '''分组类型表'''
    name=models.CharField(max_length=40,verbose_name='名称')
    descrition=models.CharField(max_length=200,verbose_name='描述',blank=True, null=True)
    def __str__(self):
        return self.message
    class Meta:
        verbose_name = '分组类型'
        verbose_name_plural = '分组类型'  

class CompGroup(models.Model):
    '''分组表'''
    name=models.CharField(max_length=40,verbose_name='名称')
    descrition=models.CharField(max_length=200,verbose_name='描述',blank=True, null=True)
    pbstatus=models.ForeignKey(PBStatus,verbose_name='关联状态') 
    type=models.ForeignKey(CompGroupType,verbose_name='关联类型',blank=True, null=True) 
    current_count = models.IntegerField(verbose_name='当前扫码数',default=0)
    total_count = models.IntegerField(verbose_name='总数阈值')
    rate = models.IntegerField(verbose_name='目标通过率')
    precastbeam = models.ManyToManyField(PrecastBeam,verbose_name='关联构件')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '分组'
        verbose_name_plural = '分组'       
        


class Acceptance(models.Model):
    '''工序质量验收'''
    name = models.CharField(max_length=128, blank=True,verbose_name='验收工作名称')
    warntime = models.DateTimeField(blank=True, null=True,verbose_name='提醒时间')
    deadline = models.DateTimeField(blank=True, null=True,verbose_name='结束时间')
    status = models.ForeignKey(PBStatus,blank=True, null=True)
    is_finished = models.IntegerField(blank=True, null=True,default=False)
    monitoring = models.ForeignKey('Monitoringelement', blank=True, null=True,verbose_name='关联监控元素')

    class Meta:
        managed = False
        db_table = 'taskandflow_acceptance'


class Acceptanceinfo(models.Model):
    '''质量验收工作信息'''
    relatedspace_type = models.CharField(max_length=64, blank=True)
    relatedspace_id = models.IntegerField(blank=True, null=True)
    finiishedtime = models.DateTimeField(blank=True, null=True)
    acceptuser = CrossDbForeignKey(User, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)#1 未处理,2处理中,3关闭
    acceptancetype= models.ForeignKey('Acceptancetype')
    comment = models.CharField(max_length=200,verbose_name='意见',blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'taskandflow_acceptanceinfo'


class AcceptanceinfoForm(models.Model):
    '''质量验收工作表单关系''' 
    acceptanceinfo = models.ForeignKey(Acceptanceinfo)
    form = models.ForeignKey(BiaoDan, blank=True, null=True)
    formfile = models.ForeignKey(Document, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_acceptanceinfo_form'


class Acceptancetype(models.Model):
    '''质量验收工作类型''' 
    name = models.CharField(max_length=64, blank=True)
    major = CrossDbForeignKey(UserMajor, blank=True, null=True)
    classification_code = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name
        
    class Meta:
        managed = False
        db_table = 'taskandflow_acceptancetype'


class AcceptancetypeFormtmp(models.Model):
    '''质量验收工作类型表单模板关系''' 
    acceptancetype = models.ForeignKey(Acceptancetype)
    formtpl = models.ForeignKey(BiaoDanMuBan, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_acceptancetype_formtmp'

class AcceptanceRemind(models.Model):
    pbstatus = models.ForeignKey(PBStatus,verbose_name='触发状态')
    acceptancetype = models.ForeignKey(Acceptancetype,verbose_name='验收类型')
    time_span = models.IntegerField(verbose_name='时间间隔（小时）')

    def __str__(self):
        return self.pbstatus.__str__()

    class Meta:
        managed = False
        db_table = 'taskandflow_acceptanceremind'
        verbose_name = '质量验收提醒'
        verbose_name_plural = '质量验收提醒'      

class Safetyinspection(models.Model):
    '''安全设施检查'''
    name = models.CharField(max_length=128, blank=True)
    warntime = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    status_id = models.IntegerField(blank=True, null=True)
    is_finished = models.IntegerField(blank=True, null=True)
    monitoring = models.ForeignKey('Monitoringelement', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_safetyinspection'


class Safetyworkinspection(models.Model):
    '''安全工作检查'''
    name = models.CharField(max_length=128, blank=True)
    warntime = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    dir = models.ForeignKey(Directory, blank=True, null=True)
    inspectuser = CrossDbForeignKey(User, blank=True, null=True)
    relatedspace_type = models.CharField(max_length=64, blank=True)
    relatedspace_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_safetyworkinspection'



class Modelfile(models.Model):
    '''模型文件'''
    relatedunitproject = models.ForeignKey(UnitProject)
    relatedmajor = CrossDbForeignKey(UserMajor)
    modelfile = models.CharField(max_length=256)
    iswhole = models.BooleanField(default=False)
    isdefault = models.BooleanField(verbose_name='是否默认加载',default=False)
    selectionmode = models.CharField(max_length=64,verbose_name='选择模式',blank=True, null=True)
    homeview = models.CharField(max_length=200,verbose_name='主视角',blank=True, null=True)
    extdata = models.CharField(max_length=200,verbose_name='扩展数据',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskandflow_modelfile'


class Monitoringelement(models.Model):
    typetable = models.CharField(max_length=96,verbose_name='元素类型')
    relatedid = models.IntegerField(verbose_name='关联元素',default=1)
    qrcode = models.CharField(max_length=128,verbose_name='扫码标签')
    class Meta:
        db_table = 'taskandflow_monitoringelement'



class Zone(models.Model):
    '''分区'''
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=120, blank=True)
    major =CrossDbForeignKey(UserMajor, blank=True, null=True)
    elevations = models.ManyToManyField(Elevation,through = 'ZoneElevation')

    class Meta:
        managed = False
        db_table = 'taskandflow_zone'


class ZoneElevation(models.Model):
    zone = models.ForeignKey(Zone)
    elevation = models.ForeignKey(Elevation)

    class Meta:
        managed = False
        db_table = 'taskandflow_zone_elevation'


class Technical(models.Model):
    '''技术方案'''
    number = models.CharField(max_length=64, blank=True)
    name = models.CharField(max_length=64, blank=True)#名称
    create_date = models.DateField(blank=True, null=True)#计划编制日期
    submit_date = models.DateField(blank=True, null=True)#上报日期
    approve_date = models.DateField(blank=True, null=True)#审批通过日期
    disclosure_date = models.DateField(blank=True, null=True)#交底日期
    hazard_code = models.CharField(max_length=24,null=True)
    comment = models.CharField(max_length=129, blank=True)
    user =CrossDbForeignKey(User)
    status = models.IntegerField(verbose_name='方案状态',default=1)#1未完成，2已上报，3已审批，4已交底

    class Meta:
        managed = False
        db_table = 'taskandflow_technical'


class TechnicalRelateddoc(models.Model):
    technical = models.ForeignKey(Technical)
    relateddoc = models.ForeignKey(Document)

    class Meta:
        managed = False
        db_table = 'taskandflow_technical_relateddoc'




