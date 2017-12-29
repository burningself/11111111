# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0008_factoryposition_areaowner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='precastbeam',
            name='curfactoryarea',
        ),
        migrations.AddField(
            model_name='precastbeam',
            name='curfactoryposition',
            field=models.ForeignKey(verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe5\x9c\xba\xe5\x9c\xb0\xe4\xbb\x93\xe4\xbd\x8d', blank=True, to='TaskAndFlow.FactoryPosition', null=True),
            preserve_default=True,
        ),
    ]
