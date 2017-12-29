# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from TaskAndFlow.models import *

def healthCheck():
    print "healthCheck:"+PushMessage.objects.all()[0].message

scheduler = BackgroundScheduler()
scheduler.add_job(healthCheck, 'interval', seconds=3)

scheduler.start()

## 下面这句加在定时任务模块的末尾...判断是否运行在uwsgi模式下, 然后阻塞mule主线程(猜测).
try:
    import uwsgi
    while True:
        sig = uwsgi.signal_wait()
        print(sig)
except Exception as err:
    pass