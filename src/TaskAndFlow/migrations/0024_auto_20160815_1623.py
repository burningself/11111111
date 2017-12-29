# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0023_auto_20160724_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='filetype',
            field=models.CharField(default=b'image/jpeg', max_length=120, verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='msprojectid',
            field=models.CharField(max_length=40, verbose_name=b'', blank=True),
            preserve_default=True,
        ),
    ]
