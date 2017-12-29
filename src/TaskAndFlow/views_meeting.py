# -*- coding: utf-8 -*-
'''

@author: pgb
'''
import traceback
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from TaskAndFlow.utility import *
from UserAndPrj.models import *
from TaskAndFlow.models import *
# from TaskAndFlow.forms import *
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.core import serializers
from _mysql import NULL
import uuid


@login_required(login_url="/login/") 
def meeting_general(request):
    return render_to_response('TaskAndFlow/meetingmanager/meetinggeneral.html', RequestContext(request,locals()))


