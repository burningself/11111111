# -*- coding: utf-8 -*-
from django.db import models
from UserAndPrj.models import *
from Scc4PM.dbsetings import CrossDbForeignKey

class PactFenbao(models.Model):
    """专业分包"""
    name = models.CharField(max_length=64,blank=False,verbose_name='分包名称')
    code = models.CharField(max_length=64,blank=False,verbose_name='编号')
    parent_code = models.CharField(max_length=64,blank=False,verbose_name='父类')
    price = models.DecimalField(max_digits=11,decimal_places=3,blank=False,verbose_name='单价')
    unit = models.CharField(max_length=64,blank=False,verbose_name='单位')
    pact = models.ForeignKey('Pact',blank=True, null=True,verbose_name='关联的预算')
    designBqs = models.FloatField(blank=True,verbose_name='设计量')
    isphysical = models.IntegerField(blank=False,default=0,verbose_name='1表示是实物量，0为非实物量')
    class Meta:
        managed = False
        db_table = 'business_sc_bqitem'

class PactSpace(models.Model):
    """预算空间表"""
    name = models.CharField(max_length=64,blank=False)
    order_no = models.IntegerField(blank=False,default=0,verbose_name='空间排序')
    insert_dt = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'business_pact_space'

class PactSpaceRate(models.Model):
    """预算费率表"""
    name = models.CharField(max_length=64,blank=False)
    num = models.CharField(max_length=64,blank=False,verbose_name='序号')
    money = models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0)
    rate = models.FloatField(blank=True,default=0,verbose_name='费率')
    pact = models.ForeignKey('Pact',blank=True, null=True)
    parent_id = models.IntegerField(default=0,verbose_name='父级')
    canadd = models.IntegerField(default=0,verbose_name='否是可以添加（1：是，0：否）')
    calc_method = models.CharField(max_length=256,blank=False,verbose_name='费率计算接口')
    class Meta:
        managed = False
        db_table = 'business_pact_space_rate'

class PactLabour(models.Model):
    name = models.CharField(max_length=64,blank=False)
    unit = models.CharField(max_length=64,blank=False)
    tax = models.DecimalField(max_digits=10,decimal_places=2,blank=True,verbose_name='税金')
    taxprice = models.DecimalField(max_digits=10,decimal_places=2,blank=True,verbose_name='含税单价')
    untaxprice = models.DecimalField(max_digits=10,decimal_places=2,blank=True,verbose_name='不含税单价')
    amount = models.FloatField(blank=True,verbose_name='数量')
    pact = models.ForeignKey('Pact',blank=True, null=True)
    isphysical = models.IntegerField(blank=False,default=0,verbose_name='1表示是实物量，0为非实物量')
    class Meta:
        managed = False
        db_table = 'business_labourpact_bqitem'


class Pact(models.Model):
    """合同/预算表"""
    name = models.CharField(max_length=64,blank=False)
    cess = models.CharField(max_length=64,blank=False,verbose_name='税率')
    pactcode = models.CharField(max_length=64,blank=False,verbose_name='编号')
    description = models.CharField(max_length=512,blank=False,verbose_name='描述')
    type = models.ForeignKey('PactType', blank=True, null=True,verbose_name='预算/合同类型（1：总承包合同或预算，2：劳务分包，3：材料采购合同，4：租赁合同5：专业分包）')
    major = CrossDbForeignKey(UserMajor, blank=True, null=True,verbose_name='专业')
    cooperation = CrossDbForeignKey(Company, blank=True, null=True,verbose_name='单位')
    hostuser = CrossDbForeignKey(User, blank=True, null=True,verbose_name='操作用户id')
    insert_dt = models.DateTimeField(blank=True, null=True)
    space = models.ForeignKey(PactSpace, blank=True, null=True,verbose_name='空间')
    budgetcont_type = models.IntegerField(blank=True, null=True,default=False,verbose_name='预算内容(1:分部分项合计。2：措施项目合计。3：其他项目合计。)')
    is_self = models.IntegerField(blank=True, null=True,default=False,verbose_name='否是自行（1：是-自行，2：否-分包）')
    locked = models.IntegerField(blank=True, null=True,default=0,verbose_name='锁定（1：已锁定，0：未锁定）')
    class Meta:
        managed = False
        db_table = 'business_pact'

class PactType(models.Model):
    """合同类型表"""
    name = models.CharField(max_length=64,blank=False)
    class Meta:
        managed = False
        db_table = 'business_pact_type'

class PactRelatefile(models.Model):
    """合同/预算附件表"""
    pact = models.ForeignKey(Pact, blank=True, null=True)
    file = models.ForeignKey('TaskAndFlow.Document', blank=True, null=True)
    file_type = models.IntegerField(blank=True, null=True,default=False,verbose_name='文件类型（1：清单，2：其他）')
    pact_type = models.IntegerField(blank=True, null=True,default=False,verbose_name='同合类型（1：总包合同，2：分包合同，3：劳务合同）')
    class Meta:
        managed = False
        db_table = 'business_pact_relatedfile'

class BqItem(models.Model):
    """清单目录项/分部分项合计"""
    BQItem_Code = models.CharField(max_length=64,blank=False,verbose_name='清单编号')
    no = models.IntegerField(blank=True,null=True,verbose_name='execl中序号')
    chapterID = models.CharField(max_length=64,blank=True,verbose_name='目录id')
    BQItemName = models.CharField(max_length=64,blank=True,verbose_name='清单名称')
    BQItemUnit = models.CharField(max_length=32,blank=True,verbose_name='单位')
    designBqs = models.FloatField(blank=True,verbose_name='设计量')
    buildBqs = models.FloatField(blank=True,verbose_name='建设量')
    finishBqs = models.FloatField(blank=True,verbose_name='完成量')
    allunitrate = models.DecimalField(max_digits=32,decimal_places=2,blank=True,verbose_name='综合单价')
    allrate = models.DecimalField(max_digits=32,decimal_places=2,blank=True,verbose_name='合价')
    ispriceLocked = models.IntegerField(default=0,verbose_name='是否锁定单价（1：是，0：否）')
    laborPrice = models.FloatField(max_length=32,blank=True,verbose_name='人工价')
    MaterialPrice = models.FloatField(max_length=32,blank=True,verbose_name='材料价')
    MachinePrice = models.FloatField(max_length=32,blank=True,verbose_name='机械价')
    insert_dt = models.DateTimeField(blank=True, null=True)
    pact = models.ForeignKey(Pact, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_bq_item'

class RtItem(models.Model):
    """定额条目"""
    RQItem_Code = models.CharField(max_length=64,blank=False,verbose_name='编号')
    RT_Item_Name = models.CharField(max_length=64,blank=False,verbose_name='名称')
    RT_Chapter_ID = models.CharField(max_length=64,blank=True,verbose_name='目录id')
    unit = models.CharField(max_length=32,blank=True,verbose_name='单位')
    BQ_Item = models.ForeignKey(BqItem,blank=True, null=True,verbose_name='关联的清单')
    quantities = models.FloatField(blank=True,verbose_name='设计量')
    buildquantities = models.FloatField(blank=True,verbose_name='施工量')
    unitprice = models.DecimalField(max_digits=32,decimal_places=2,blank=True,verbose_name='单价')
    totalprice = models.DecimalField(max_digits=32,decimal_places=2,blank=True,verbose_name='总价')
    LaborPrice = models.DecimalField(max_digits=32,decimal_places=2,blank=True)
    MaterialPrice = models.CharField(max_length=32,blank=True)
    MachinePrice = models.CharField(max_length=32,blank=True)

    class Meta:
        managed = False
        db_table = 'business_rt_item'

class RtItemResource(models.Model):
    """本地库工料机表"""
    resourcename = models.CharField(max_length=64,blank=False,verbose_name='工料机名称')
    unit = models.CharField(max_length=64,blank=True,verbose_name='单位')
    Code = models.CharField(max_length=32,blank=True,verbose_name='编号')
    type = models.IntegerField(blank=True,verbose_name='资源类型（1：人工，2：材料，3：机械）')
    Price = models.DecimalField(max_digits=32,decimal_places=3,blank=True,verbose_name='价格')

    class Meta:
        managed = False
        db_table = 'business_rt_item_resource'

class RtItemResourceRelate(models.Model):
    """定额工料机关联表"""
    rtitem = models.ForeignKey(RtItem,blank=False,verbose_name='关联的定额')
    RTContentAmount = models.FloatField(blank=True,verbose_name='默认含量，工料机的量/系数')
    RTActualAmount = models.FloatField(blank=True,verbose_name='实际含量，工料机的量/系数')
    type = models.IntegerField(blank=True,verbose_name='资源类型（1：人工，2：材料，3：机械）')
    resource = models.ForeignKey('RtItemResource',blank=True)
    spect = models.CharField(max_length=64,blank=True,verbose_name='规格')
    amount = models.FloatField(blank=True,verbose_name='数量，实际的量=系数×对应定额量')
    class Meta:
        managed = False
        db_table = 'business_rt_item_resource_relate'

class RtItemResourceThoundRelate(models.Model):
    """2000定额工料机 """
    rtitem = models.ForeignKey(RtItem,blank=False)
    RTContentAmount = models.FloatField(blank=True,verbose_name='默认含量，工料机的量/系数')
    RTActualAmount = models.FloatField(blank=True,verbose_name='实际含量，工料机的量/系数')
    type = models.IntegerField(blank=True,verbose_name='资源类型（1：人工，2：材料，3：机械）')
    resource = models.ForeignKey(RtItemResource,blank=True)
    spect = models.CharField(max_length=64,blank=True,verbose_name='规格')
    amount = models.FloatField(blank=True,verbose_name='数量，实际的量=系数×对应定额量')
    class Meta:
        managed = False
        db_table = 'business_rt_item_resource_twothound_relate'

class BqItemResourceRelate(models.Model):
    """清单工料机关联表"""
    bqitem = models.ForeignKey('BqItem',blank=False)
    BQTActualAmount = models.FloatField(blank=True,verbose_name='实际含量/系数')
    resource_type = models.IntegerField(blank=True,verbose_name='资源类型（1：人工，2：材料，3：机械）')
    resource = models.ForeignKey('RtItemResource',blank=True)
    class Meta:
        managed = False
        db_table = 'business_bq_item_resource_relate'

class SrcmodelFile(models.Model):
    """模型源文件表"""
    source_filename = models.CharField(max_length=255,blank=True)
    ifc_filename = models.CharField(max_length=255,blank=True)
    class Meta:
        managed = False
        db_table = 'taskandflow_srcmodel_file'


class Budget(models.Model):
    '''施工预算条目表（对应revit量）'''
    name = models.CharField(max_length=64,blank=True,verbose_name='名称')
    srcmodel = models.ForeignKey(SrcmodelFile,blank=True,verbose_name='对应构件')
    doc = models.ForeignKey('TaskAndFlow.Document', blank=True, null=True,verbose_name='文件id')
    description = models.CharField(max_length=256,blank=True,verbose_name='描述')

    class Meta:
        managed = False
        db_table = 'business_budget'


class CalRelation(models.Model):
    """计算规则表"""
    category = models.CharField(max_length=255,blank=True,verbose_name='类别')
    name = models.CharField(max_length=255,blank=True,verbose_name='名称')
    valueUnit = models.CharField(max_length=255,blank=True,verbose_name='产值单位')
    costUnit = models.CharField(max_length=255,blank=True,verbose_name='成本单位')
    differParam = models.CharField(max_length=255,blank=True,verbose_name='区分条件')
    bqItem = models.ForeignKey(BqItem,blank=True,verbose_name='关联的清单id', null=True)
    SCItem = models.ForeignKey(PactFenbao,blank=True,verbose_name='关联的分包清单id', null=True)
    lpItem = models.ForeignKey(PactLabour,blank=True,null=True,verbose_name='关联的劳务分包')
    toTaskOrder = models.IntegerField(blank=True,default=0,verbose_name='关联的是分建成本，则toTaskOrder为0，如果关联的是任务单，则toTaskOrder为1,0：false,1：true')
    class Meta:
        managed = False
        db_table = 'business_calc_relation'


class ComponentQuantities(models.Model):
    '''施工预算表'''
    code = models.CharField(max_length=255,blank=True,verbose_name='编号')
    name = models.CharField(max_length=255,blank=True,verbose_name='项目名称')
    description = models.CharField(max_length=255,blank=True,verbose_name='描述')
    filename = models.CharField(max_length=255,blank=True,verbose_name='文件名')
    valueQuantity = models.FloatField(blank=True,verbose_name='预算工程量')
    costQuantity = models.FloatField(blank=True,verbose_name='成本工程量')
    calcRelation_id = models.IntegerField(blank=True,verbose_name='计算需求id')
    precastbeam_id = models.IntegerField(blank=True,verbose_name='构件id')
    can_update = models.IntegerField(blank=True,default=1)
    budget = models.ForeignKey('Budget',blank=True,verbose_name='施工预算id')
    bqitem = models.ForeignKey(BqItem,blank=True,verbose_name='施工预算id')
    class Meta:
        managed = False
        db_table = 'business_component_quantities'

class ScChapter(models.Model):
    """分包定额章节表"""
    name = models.CharField(max_length=255,blank=True,verbose_name='章节名称')
    pact = models.ForeignKey(Pact, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'business_sc_chapter'


class Report(models.Model):
    """产值报表"""
    name = models.CharField(max_length=64,blank=True,verbose_name='名称')
    report_time = models.DateTimeField(auto_now_add=False,verbose_name='报表创建时间')
    start_time = models.DateTimeField(auto_now_add=False,verbose_name='开始时间')
    end_time = models.DateTimeField(auto_now_add=False,verbose_name='结束时间')
    locked = models.IntegerField(blank=True,default=0,verbose_name='是否锁定（1：是，0：否）')
    pact = models.ForeignKey('Pact',blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'business_report'

class ReportBqitem(models.Model):
    """产值报告清单表"""
    code = models.CharField(max_length=255,blank=True,verbose_name='清单编码')
    name = models.CharField(max_length=255,blank=True,verbose_name='清单名称')
    unit = models.CharField(max_length=255,blank=True,verbose_name='单位')
    quantity = models.FloatField(blank=True,verbose_name='工程量')
    isLocked = models.IntegerField(blank=True,default=0,verbose_name='是否锁定（1：是，0：否）')
    unitprice = models.DecimalField(max_digits=11,decimal_places=2,blank=False,verbose_name='单价')
    report = models.ForeignKey(Report,blank=True,null=True,verbose_name='关联的报告')
    bq = models.ForeignKey(BqItem,blank=True,null=True,verbose_name='关联的清单')
    class Meta:
        managed = False
        db_table = 'business_report_bq_item'

class ReportRtitem(models.Model):
    """产值报告定额表"""
    code = models.CharField(max_length=255,blank=True,verbose_name='定额编码')
    name = models.CharField(max_length=255,blank=True,verbose_name='定额名称')
    unit = models.CharField(max_length=255,blank=True,verbose_name='单位')
    quantity = models.FloatField(blank=True,verbose_name='工程量')
    unitprice = models.FloatField(blank=True,verbose_name='单价')
    reportbq = models.ForeignKey(ReportBqitem,blank=True,null=True,verbose_name='关联的报告清单')
    rtitem = models.ForeignKey(RtItem,blank=True,null=True,verbose_name='关联的定额')
    class Meta:
        managed = False
        db_table = 'business_report_rt_item'

class ReportCostItem(models.Model):
    """产值报告成本表"""
    name = models.CharField(max_length=255,blank=True,verbose_name='成本名称')
    report = models.ForeignKey(Report,blank=True,null=True,verbose_name='关联的报告')
    unit = models.CharField(max_length=255,blank=True,verbose_name='单位')
    quanlity = models.FloatField(blank=True,verbose_name='工程量')
    unitprice = models.FloatField(blank=True,verbose_name='单价')
    chapter = models.ForeignKey(ScChapter,blank=True,null=True,verbose_name='关联的定额章节（四建设）')
    sc = models.ForeignKey(PactFenbao,blank=True,null=True,verbose_name='关联的分包清单')
    rate = models.FloatField(blank=True,verbose_name='费率')
    ratedescription = models.CharField(max_length=64,blank=True,verbose_name='基数说明')
    money = models.DecimalField(max_digits=11,decimal_places=2,blank=False,verbose_name='金额')
    class Meta:
        managed = False
        db_table = 'business_report_cost_item'

class ReportResItem(models.Model):
    """产值报告资源汇总表"""
    code = models.CharField(max_length=255,blank=True,verbose_name='编码')
    name = models.CharField(max_length=255,blank=True,verbose_name='名称')
    unit = models.CharField(max_length=255,blank=True,verbose_name='单位')
    amount = models.FloatField(blank=True,verbose_name='总量')
    unitprice = models.FloatField(blank=True,verbose_name='单价')
    resource = models.ForeignKey(RtItemResource,blank=True,null=True,verbose_name='关联的资源')
    report = models.ForeignKey(Report,blank=True,null=True,verbose_name='关联的报告')
    report_rtitem = models.ForeignKey(ReportRtitem,blank=True,null=True,verbose_name='关联的定额')
    class Meta:
        managed = False
        db_table = 'business_report_res_item'

class ReportResThoundItem(models.Model):
    """产值报告2000定额工料机表"""
    code = models.CharField(max_length=255,blank=True,verbose_name='编码')
    name = models.CharField(max_length=255,blank=True,verbose_name='名称')
    unit = models.CharField(max_length=255,blank=True,verbose_name='单位')
    amount = models.FloatField(blank=True,verbose_name='总量')
    unitprice = models.FloatField(blank=True,verbose_name='单价')
    resource = models.ForeignKey(RtItemResource,blank=True,null=True,verbose_name='关联的资源')
    report = models.ForeignKey(Report,blank=True,null=True,verbose_name='关联的报告')
    report_rtitem = models.ForeignKey(ReportRtitem,blank=True,null=True,verbose_name='关联的定额')
    class Meta:
        managed = False
        db_table = 'business_report_res_twothound_item'


class TaskOrderPhysical(models.Model):
    '''实物量任务单表'''
    name = models.CharField(max_length=64,blank=True,verbose_name='名称')
    unit = models.CharField(max_length=64,blank=True,verbose_name='单位')
    company = models.ForeignKey("UserAndPrj.Company",blank=True,verbose_name='分包单位')
    major = models.ForeignKey("UserAndPrj.UserMajor",blank=True,verbose_name='专业')
    issuing_time = models.DateTimeField(auto_now_add=False,verbose_name='开具时间')
    quantities = models.FloatField(blank=True,null=True,verbose_name='数量')
    pact_price = models.DecimalField(max_digits=10,decimal_places=2,blank=False,verbose_name='合同价格')
    sc = models.ForeignKey(PactLabour,blank=True,null=True,verbose_name='关联的分包清单')
    totalprice = models.DecimalField(max_digits=10,decimal_places=2,blank=False,verbose_name='总价')
    description = models.TextField(verbose_name='备注')
    report = models.ForeignKey(Report,blank=True,null=True,verbose_name='关联的报告')
    class Meta:
        managed = False
        db_table = 'business_taskorder_physical'

'''非实物量任务单表'''
class TaskOrderNophysical(models.Model):
    content = models.CharField(max_length=64,blank=True,verbose_name='内容')
    worktype = models.CharField(max_length=64,blank=True,verbose_name='工种类型')
    unit = models.CharField(max_length=64,blank=True,verbose_name='单位')
    company = models.ForeignKey("UserAndPrj.Company",blank=True,verbose_name='分包单位')
    professional = models.ForeignKey("UserAndPrj.UserMajor",blank=True,verbose_name='专业')
    issuing_time = models.DateTimeField(auto_now_add=False,verbose_name='开具时间')
    quantities = models.FloatField(blank=True,null=True,verbose_name='数量')
    workprice = models.DecimalField(max_digits=10,decimal_places=2,blank=False,verbose_name='合同价格')
    sc = models.ForeignKey(PactLabour,blank=True,null=True,verbose_name='关联的分包清单')
    totalprice = models.DecimalField(max_digits=10,decimal_places=2,blank=False,verbose_name='总价')
    description = models.TextField(verbose_name='备注')
    report = models.ForeignKey(Report,blank=True,null=True,verbose_name='关联的报告')
    class Meta:
        managed = False
        db_table = 'business_taskorder_no_physical'

class CostSeparate(models.Model):
    '''分建成本'''
    pro_code = models.CharField(max_length=64,blank=True,verbose_name='项目编号')
    pro_name = models.CharField(max_length=64,blank=True,verbose_name='项目名称')
    unit = models.CharField(max_length=64,blank=True,verbose_name='单位')
    quantities = models.FloatField(blank=True,null=True,verbose_name='数量')
    price = models.DecimalField(max_digits=10,decimal_places=2,blank=False,verbose_name='单价')
    money = models.DecimalField(max_digits=10,decimal_places=2,blank=False,verbose_name='合价')
    report = models.ForeignKey(Report,blank=True,null=True,verbose_name='关联的报告')
    sc = models.ForeignKey(PactFenbao,blank=True,null=True,verbose_name='关联的分包清单')
    company = models.ForeignKey("UserAndPrj.Company",blank=True,verbose_name='分包单位')
    class Meta:
        managed = False
        db_table = 'business_cost_separate'


class TaskOrderFile(models.Model):
    '''任务单附件表'''
    taskorder = models.ForeignKey("TaskOrderPhysical",blank=True,verbose_name='任务单id')
    doc = models.ForeignKey("TaskAndFlow.Document",blank=True,verbose_name='任务单附件')

    class Meta:
        managed = False
        db_table = 'business_taskorder_file'

class PactFenbaoYusuan(models.Model):
    """分包、预算关联关系表"""
    yusuan = models.ForeignKey(Pact, blank=True, null=True,related_name="yusuan",verbose_name='预算id')
    fenbao = models.ForeignKey(Pact, blank=True, null=True,related_name="fenbao",verbose_name='预算id')
    class Meta:
        managed = False
        db_table = 'business_pact_fenbao'

class ReportRate(models.Model):
    """报表费率"""
    name = models.CharField(max_length=64,blank=False,verbose_name='名称')
    num = models.CharField(max_length=64,blank=False,verbose_name='序号')
    time = models.CharField(max_length=64,blank=False,verbose_name='日期，指报表的时间')
    money = models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0,verbose_name='金额')
    rate = models.FloatField(blank=True,default=0,verbose_name='费率')
    report = models.ForeignKey(Report,blank=True, null=True)
    parent_id = models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = 'business_report_rate'


class OtherItem(models.Model):
    """其他项目合计"""
    no = models.IntegerField(blank=True,null=True,verbose_name='execl中编号')
    other_item_name = models.CharField(max_length=255,blank=True,verbose_name='清单名称')
    other_item_unit = models.CharField(max_length=255,blank=True,verbose_name='单位')
    design_bqs = models.FloatField(blank=True,verbose_name='设计量')
    alunitrate = models.FloatField(blank=True,verbose_name='综合单价')
    allrate = models.FloatField(blank=True,verbose_name='合价')
    percent_labour = models.FloatField(max_length=32,blank=True,verbose_name='人工费含量')
    insert_dt = models.DateTimeField(blank=True, null=True)
    pact = models.ForeignKey(Pact, blank=True, null=True)
    parent_id = models.IntegerField(blank=True,verbose_name='父级')

    class Meta:
        managed = False
        db_table = 'business_other_item'

class OtherItemRate(models.Model):
    """其他项目合计费率"""
    name = models.CharField(max_length=64,blank=False,verbose_name='名称')
    num = models.CharField(max_length=64,blank=False,verbose_name='序号')
    money = models.DecimalField(max_digits=10,decimal_places=2,blank=True,default=0,verbose_name='金额')
    rate = models.FloatField(blank=True,default=0,verbose_name='费率')
    pact = models.ForeignKey(Pact,blank=True, null=True)
    parent_id = models.IntegerField(default=0)
    canadd = models.IntegerField(default=0,verbose_name='是否可以添加')
    calc_method = models.CharField(max_length=256,blank=False,verbose_name='费率计算接口')

    class Meta:
        managed = False
        db_table = 'business_other_item_rate'
