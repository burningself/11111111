# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0020_flowtemplatestep_istimeouttransfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstepoperation',
            name='flowstepoper',
            field=models.ForeignKey(verbose_name=b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xa8\xa1\xe6\x9d\xbf\xe6\xad\xa5\xe9\xaa\xa4\xe6\x93\x8d\xe4\xbd\x9c', blank=True, to='TaskAndFlow.FlowStepOperation', null=True),
            preserve_default=True,
        ),
    ]
