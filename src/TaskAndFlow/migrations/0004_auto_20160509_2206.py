# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0003_auto_20160509_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='pbstatusrecord',
            name='isactive',
            field=models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x9c\x89\xe6\x95\x88'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pbstatusrecord',
            unique_together=set([]),
        ),
    ]
