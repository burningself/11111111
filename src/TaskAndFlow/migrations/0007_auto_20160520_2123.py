# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0006_auto_20160520_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttask',
            name='parentid',
            field=models.ForeignKey(verbose_name=b'\xe7\x88\xb6\xe8\x8a\x82\xe7\x82\xb9', blank=True, to='TaskAndFlow.ProjectTask', null=True),
            preserve_default=True,
        ),
    ]
