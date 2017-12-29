# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0022_auto_20160712_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='islock',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\x94\x81\xe5\xae\x9a'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='filesize',
            field=models.IntegerField(default=0, verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe5\xa4\xa7\xe5\xb0\x8f'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='filetype',
            field=models.CharField(default=b'image/jpeg', max_length=60, verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b'),
            preserve_default=True,
        ),
    ]
