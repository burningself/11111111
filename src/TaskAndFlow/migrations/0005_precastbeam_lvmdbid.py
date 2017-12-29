# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0004_auto_20160509_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='precastbeam',
            name='lvmdbid',
            field=models.IntegerField(null=True, verbose_name=b'LvmDbId', blank=True),
            preserve_default=True,
        ),
    ]
