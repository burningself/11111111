#coding: utf-8
from django.contrib import admin
from TaskAndFlow.models import *


# Register your models here.
class FactoryAreaAdmin(admin.ModelAdmin):
    list_display = ('number','total','description',)

class FactoryPositionAdmin(admin.ModelAdmin):
    list_display = ('number','name','area','description',)

class UnitProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ElevationAdmin(admin.ModelAdmin):
    list_display = ('name','level','unitproject',)
    
class PBMaterialAdmin(admin.ModelAdmin):
    list_display = ('name','specification','size',)
    
class PBTypeAdmin(admin.ModelAdmin):
    list_display = ('name','major','isprebuilt',)
    
class PBStatusAdmin(admin.ModelAdmin):
    list_display = ('statusname','factoryarea','pbtype','nextstatus',)
    
class PrecastBeamAdmin(admin.ModelAdmin):
    list_display = ('guid','number','pbtype','task','parentguid','curstatus')
    
class User2PBStatusAdmin(admin.ModelAdmin):
    list_display = ('user','status',)
    
class PBStatusRecordAdmin(admin.ModelAdmin):
    list_display = ('status','precastbeam','actor','factoryposition','time')
    
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('statusname','tasktype','nextstatus',)
    
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('name','parentid','planstart','planfinish','percentage')
    
class User2TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('user','status',)
    
class TaskStatusRecordAdmin(admin.ModelAdmin):
    list_display = ('status','task','actor','time',)
    
class FlowTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class FlowTemplateAdmin(admin.ModelAdmin):
    list_display = ('name','major','flowtype','describe',)
    
class FlowTemplateStepAdmin(admin.ModelAdmin):
    list_display = ('name','template','isautotransfer',)
    
class FlowStepUserAdmin(admin.ModelAdmin):
    list_display = ('user','flowstep','isactor',)
    
class ActorTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class FlowStepOperationAdmin(admin.ModelAdmin):
    list_display = ('name','flowstep','actortype','nextflowstep',)
    
class projecteventAdmin(admin.ModelAdmin):
    list_display = ('template','number','relatedmonitoringelement','describe',)
    
class EventstepAdmin(admin.ModelAdmin):
    list_display = ('flowstep','projectevent','starttime','endtime',)
    
class EventStepOperationAdmin(admin.ModelAdmin):
    list_display = ('flowstepoper','eventstep','oprtime','actor',)
    
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent','createtime','creator',)
    
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name','createtime','filepath',)
    
class Doc2RelateAdmin(admin.ModelAdmin):
    list_display = ('document','relatetype','creator','createtime',)
    
class CMTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class CMStatusAdmin(admin.ModelAdmin):
    list_display = ('statusname','cmtype','nextstatus',)

class ConstructionMachineAdmin(admin.ModelAdmin):
    list_display = ('name','number','cmtype','curstatus',)
    
class User2CMStatusAdmin(admin.ModelAdmin):
    list_display = ('user','status',)
    
class CMStatusRecordAdmin(admin.ModelAdmin):
    list_display = ('status','constructionmachine','actor','time',)
    
class HazardTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class HazardStatusAdmin(admin.ModelAdmin):
    list_display = ('statusname','nextstatus',)
    
class HazardAdmin(admin.ModelAdmin):
    list_display = ('name','number','hazardtype','relatetype','curstatus',)
    
class User2HazardStatusAdmin(admin.ModelAdmin):
    list_display = ('user','status',)
    
    
class MessageTypeAdmin(admin.ModelAdmin):
    list_display = ('name','priority',)
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ('receiver','message','sender','relatetype',)
    
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title','message','sender','time',)

class AcceptanceRemindAdmin(admin.ModelAdmin):
    list_display = ('pbstatus','acceptancetype','time_span',)
    list_editable =('acceptancetype','time_span',)

class PbstatusremindAdmin(admin.ModelAdmin):
    list_display = ('pbstatus','next_status','time_span',)
    list_editable =('next_status','time_span',)

admin.site.register(FactoryArea, FactoryAreaAdmin)
admin.site.register(FactoryPosition, FactoryPositionAdmin)
admin.site.register(UnitProject, UnitProjectAdmin)
admin.site.register(Elevation, ElevationAdmin)
admin.site.register(PBMaterial, PBMaterialAdmin)
admin.site.register(PBType, PBTypeAdmin)
admin.site.register(PBStatus, PBStatusAdmin)
admin.site.register(PrecastBeam, PrecastBeamAdmin)
admin.site.register(User2PBStatus, User2PBStatusAdmin)
admin.site.register(PBStatusRecord, PBStatusRecordAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(TaskStatus,TaskStatusAdmin)
admin.site.register(ProjectTask, ProjectTaskAdmin)
admin.site.register(User2TaskStatus, User2TaskStatusAdmin)
admin.site.register(TaskStatusRecord, TaskStatusRecordAdmin)
admin.site.register(FlowType,FlowTypeAdmin)
admin.site.register(FlowTemplate,FlowTemplateAdmin)
admin.site.register(FlowTemplateStep, FlowTemplateStepAdmin)
admin.site.register(FlowStepUser, FlowStepUserAdmin)
admin.site.register(ActorType,ActorTypeAdmin)
admin.site.register(FlowStepOperation, FlowStepOperationAdmin)
admin.site.register(projectevent, projecteventAdmin)
admin.site.register(Eventstep,EventstepAdmin)
admin.site.register(EventStepOperation,EventStepOperationAdmin)
admin.site.register(Directory,DirectoryAdmin)
admin.site.register(Document,DocumentAdmin)
admin.site.register(Doc2Relate,Doc2RelateAdmin)
admin.site.register(CMType,CMTypeAdmin)
admin.site.register(CMStatus,CMStatusAdmin)
admin.site.register(ConstructionMachine,ConstructionMachineAdmin)
admin.site.register(User2CMStatus,User2CMStatusAdmin)
admin.site.register(CMStatusRecord,CMStatusRecordAdmin)
admin.site.register(HazardType,HazardTypeAdmin)
admin.site.register(HazardStatus,HazardStatusAdmin)
admin.site.register(User2HazardStatus,User2HazardStatusAdmin)
admin.site.register(MessageType,MessageTypeAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Notice,NoticeAdmin)
admin.site.register(AcceptanceRemind,AcceptanceRemindAdmin)
admin.site.register(Pbstatusremind,PbstatusremindAdmin)
