# coding=utf-8
import os,time,random, sys, datetime, calendar, traceback,json

'''比较时间差'''
def Caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    return date2-date1

def CaltimeDay(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])
    return ((date2-date1).days)

'''获取当前时间，format为时间格式'''
def Curr_time(formatstr):
    curr_time = datetime.datetime.now()
    curr_time = str(curr_time.strftime(formatstr))
    return curr_time

'''定义和调用类(无效)'''
class EnvirmentDataUtil:
    def __init__(self):
        self.url = 'http://219.233.250.171:88/index!getProMon.action?gcbh=1222'

    def gerDatas(self):
        ev = requests.get(self.url)
        return ev

'''时间格式json解析'''
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

