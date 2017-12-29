# -*- coding: utf-8 -*-
from TaskAndFlow.models import *
import json
import traceback
import datetime
from Scc4PM.settings import *

def getkjname(each):#获取危险源全名
    relateid = each.relatedspace_id
    kjys = "选择空间"
    val="model"
    try:
        if each.relatedspace_type == u'单位工程':
            kjys = UnitProject.objects.get(id=relateid).name
            val = 'unitprj_' + str(each.relatedspace_id)
        elif each.relatedspace_type == u'楼层':
            lc = Elevation.objects.get(id=relateid)
            val = 'floor_' + str(each.relatedspace_id)
            kjys = UnitProject.objects.get(id=lc.unitproject_id).name + lc.name
        elif each.relatedspace_type == u'分区':
            val = 'zone_' + str(each.relatedspace_id)
            kjys = Zone.objects.get(id=relateid).name
        else:
            kjys = '选择空间'
            val = 'model'
    except Exception as e:
        traceback.print_exc()
        pass

    return kjys,val