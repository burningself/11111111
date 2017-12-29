# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0007_auto_20160520_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='factoryposition',
            name='areaowner',
            field=models.ForeignKey(default=1, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x9c\xba\xe5\x9c\xb0', to='TaskAndFlow.FactoryArea'),
            preserve_default=False,
        ),
    ]
