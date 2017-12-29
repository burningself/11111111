# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from Scc4PM.settings import CURRENT_PROJECT_ID
from TaskAndFlow.models import *
from TaskAndFlow.utility_filemanager import *
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options): 
        updatefileinfo()
        return

def updatefileinfo():
    doclist = Document.objects.all()
    for doc in doclist:
        if doc.docdirectory.all():
            movefiletoDir(doc, doc.docdirectory.all()[0])
