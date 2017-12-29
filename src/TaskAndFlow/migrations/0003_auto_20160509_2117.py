# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0002_auto_20160508_1554'),
    ]

    operations = [
        migrations.RenameField(
            model_name='precastbeam',
            old_name='high',
            new_name='height',
        ),
        migrations.RemoveField(
            model_name='precastbeam',
            name='uniqueid',
        ),
        migrations.AddField(
            model_name='precastbeam',
            name='length',
            field=models.FloatField(null=True, verbose_name=b'\xe9\x95\xbf\xe5\xba\xa6', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='elevation',
            name='level',
            field=models.FloatField(null=True, verbose_name=b'\xe6\xa0\x87\xe9\xab\x98', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='precastbeam',
            name='number',
            field=models.CharField(max_length=64, verbose_name=b'\xe7\xbc\x96\xe5\x8f\xb7'),
            preserve_default=True,
        ),
    ]
