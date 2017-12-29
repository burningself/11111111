# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import TaskAndFlow.models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0026_auto_20161026_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pushmessage',
            name='touser',
            field=TaskAndFlow.models.CrossDbForeignKey(related_name='touser', verbose_name=b'\xe6\x8e\xa5\xe6\x94\xb6\xe4\xba\xba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
