# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0014_auto_20160614_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbstatus',
            name='pbtype',
            field=models.ForeignKey(verbose_name=b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b', blank=True, to='TaskAndFlow.PBType', null=True),
            preserve_default=True,
        ),
    ]
