# -*- coding: utf-8 -*-
'''
Created on 2016年4月16日
多数据路由配置
@author: pgb
'''
from django.db import models
from django.db import router

class appdb(object):
 
    def db_for_read(self, model, **hints):
        #该方法定义读取时从哪一个数据库读取
        return self.__app_router(model)
 
    def db_for_write(self, model, **hints):
        #只允许写项目自己的数据库
        return self.__app_router(model)
        if model._meta.app_label == 'TaskAndFlow':
            return 'pms'
        elif model._meta.app_label in ('UserAndPrj','admin','auth','contenttypes','messages','sessions'):
            return 'ems'
        return 'pms'
 
    def allow_relation(self, obj1, obj2, **hints):
        #该方法用于判断传入的obj1和obj2是否允许关联，可用于多对多以及外键
        #同一个应用同一个数据库
        app_list = ('UserAndPrj', 'TaskAndFlow','Assist','Admin','admin','auth','contenttypes','messages','sessions','SpaceManager','VehicleManager','UserPrjConfig')
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        #允许关联
        elif obj1._meta.app_label in app_list and obj2._meta.app_label in app_list:
            return True
        else:
            return None
 
 
    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'TaskAndFlow':
            return db == 'pms'
        return None
 
    #添加一个私有方法用来判断模型属于哪个应用，并返回应该使用的数据库
    def __app_router(self, model):
        if model._meta.app_label in ('UserAndPrj',):
            return 'ems'
        elif model._meta.app_label in ('Admin','TaskAndFlow','Assist','SpaceManager','VehicleManager','UserPrjConfig'):
            return 'pms'
        elif model._meta.app_label in ('admin','auth','contenttypes','messages','sessions'):
            return 'ems'
        else :
            return 'default'


class CrossDbForeignKey(models.ForeignKey):
    def validate(self, value, model_instance):
        if self.rel.parent_link:
            return
        super(models.ForeignKey, self).validate(value, model_instance)
        if value is None:
            return

        # Here is the trick, get db relating to fk, not to root model
        using = router.db_for_read(self.rel.to, instance=model_instance)

        qs = self.rel.to._default_manager.using(using).filter(
                **{self.rel.field_name: value}
             )
        qs = qs.complex_filter(self.rel.limit_choices_to)
        if not qs.exists():
            raise exceptions.ValidationError(self.error_messages['invalid'] % {
                'model': self.rel.to._meta.verbose_name, 'pk': value})