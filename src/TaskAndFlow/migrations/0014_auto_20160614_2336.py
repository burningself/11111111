# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0013_auto_20160529_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusCountType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x90\x8d\xe7\xa7\xb0')),
                ('rendercolor', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': '\u7edf\u8ba1\u7c7b\u578b',
                'verbose_name_plural': '\u7edf\u8ba1\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pbstatus',
            name='counttype',
            field=models.ForeignKey(verbose_name=b'\xe7\xbb\x9f\xe8\xae\xa1\xe7\xb1\xbb\xe5\x9e\x8b', blank=True, to='TaskAndFlow.StatusCountType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pbstatus',
            name='sequence',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\xba\x8f\xe5\x8f\xb7'),
            preserve_default=True,
        ),
    ]
