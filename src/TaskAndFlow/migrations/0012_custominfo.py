# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0011_unitproject_isdefault'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doctype', models.CharField(max_length=20, choices=[(b'pblist', b'pblist')])),
                ('custominfo', models.CharField(max_length=120, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u81ea\u5b9a\u4e49\u4fe1\u606f',
                'verbose_name_plural': '\u7528\u6237\u81ea\u5b9a\u4e49\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
    ]
