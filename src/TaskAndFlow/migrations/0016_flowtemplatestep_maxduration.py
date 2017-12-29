# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0015_auto_20160617_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowtemplatestep',
            name='maxDuration',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\xb7\xa5\xe6\x9c\x9f'),
            preserve_default=True,
        ),
    ]
