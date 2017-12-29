# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from Scc4PM.settings import CURRENT_PROJECT_ID
from Assist.utility import zhouqiHuiyiCreate
from TaskAndFlow.utility import *
from TaskAndFlow.utility_technical import *
from TaskAndFlow.hazard_from_task import hazard_diary
from TaskAndFlow.utility_pbtype_timecheck import pbtype_timecheck
from TaskAndFlow.utility_filemanager import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        zhouqiHuiyiCreate()
        hazard_diary()
        pbtype_timecheck()
        
        #transdwg2ocfdiary()

        urllib2_util_technical()
        return
