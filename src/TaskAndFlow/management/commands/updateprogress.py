# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from Scc4PM.settings import DATABASES
from TaskAndFlow.models import *
from TaskAndFlow.utility_taskmanager import *
import os,MySQLdb, memcache, datetime, traceback
from django.db import transaction

class Command(BaseCommand):
    def handle(self, *args, **options): 
        updateprogressinfo()
        setprogressinfo()
        return

def updateprogressinfo():
    try:
        print DATABASES['pms']['NAME']
        conn = MySQLdb.connect(host=DATABASES['pms']['HOST'],
                               user=DATABASES['pms']['USER'],
                               passwd=DATABASES['pms']['PASSWORD'],
                               db=DATABASES['pms']['NAME'],
                               port=DATABASES['pms']['PORT'])
        cur =conn.cursor()
        cur.callproc('calcTaskProgress',())
        conn.commit()
        cur.close()
        conn.close();
    except:
        traceback.print_exc()
        pass

def setprogressinfo():
    calcProjectTaskProgressInfo()