# -*- coding: utf-8 -*-

from TaskAndFlow.models import *
import datetime
import traceback

def hazard_from_yestoday():
    day = datetime.date.today()
    day1 = day + datetime.timedelta(-1)
    # 不复制从任务来的危险源
    # beforeha = Hazardevent.objects.filter(his_date=day1).exclude(name__contains='来自任务:') 

    # 复制从任务来的危险源
    beforeha = Hazardevent.objects.filter(his_date=day1).exclude(curstatus__statusname=u'关闭') 
    for each in beforeha:
        print each.curstatus.statusname
        newha = Hazardevent.objects.create(hazard_code=each.hazard_code,name=each.name,major=each.major,curstatus=each.curstatus,
                                        remarks=each.remarks,relatedele_type=each.relatedele_type,relatedele_id=each.relatedele_id,
                                        relatedspace_type=each.relatedspace_type,relatedspace_id=each.relatedspace_id,
                                        ownerlist=each.ownerlist,duration=each.duration+1,his_date=day)

def hazard_from_task():
    pts = ProjectTaskHazard.objects.filter(projecttask__planstart__lte=datetime.date.today(),projecttask__planfinish__gte=datetime.date.today())
    print pts
    for each in pts:
        try:
            describ = u'来自任务:'+each.projecttask.name
            hardcode = each.hazard_code
            default_curstatus = HazardStatus.objects.all()[0].id
            if each.relatedspace_id:
                kjty = each.relatedspace_type
                kjid = each.relatedspace_id
                #查询昨天是否有该危险源
                day1 = datetime.date.today() + datetime.timedelta(-1)
                beforeha = Hazardevent.objects.filter(his_date=day1,hazard_code=hardcode,relatedspace_type=kjty,relatedspace_id=int(kjid))

                if(len(beforeha)>0):
                    duration = 0 
                    if beforeha[0].curstatus.statusname==u"关闭":
                        ProjectTaskHazard.objects.filter(id=each.id).delete()
                    else:
                        duration=beforeha[0].duration+1
                        newha = Hazardevent.objects.create(hazard_code=hardcode,name=describ,duration=duration,
                            curstatus_id=beforeha[0].curstatus_id,relatedspace_type=kjty,relatedspace_id=int(kjid),his_date=datetime.date.today())

                else:
                    newha = Hazardevent.objects.create(hazard_code=hardcode,name=describ,duration=1,
                        curstatus_id=default_curstatus,relatedspace_type=kjty,relatedspace_id=int(kjid),his_date=datetime.date.today())
            else:
                day1 = datetime.date.today() + datetime.timedelta(-1)
                beforeha = Hazardevent.objects.filter(his_date=day1,hazard_code=hardcode,relatedspace_id__isnull=True)

                if(len(beforeha)>0):
                    duration = 0 
                    if beforeha[0].curstatus.statusname==u"关闭":
                        ProjectTaskHazard.objects.filter(id=pts.id).delete()
                    else:
                        duration=beforeha[0].duration+1
                        newha = Hazardevent.objects.create(hazard_code=hardcode,name=describ,duration=duration,
                            curstatus_id=beforeha[0].curstatus_id,his_date=datetime.date.today())
                else:
                    newha = Hazardevent.objects.create(hazard_code=hardcode,name=describ,duration=1,
                        curstatus_id=default_curstatus,his_date=datetime.date.today())
        except:
            traceback.print_exc()
            print u"危险源数据重复"


def hazard_diary():
    hazard_from_yestoday()
    hazard_from_task()

