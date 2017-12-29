# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0027_auto_20161026_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('descrition', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('current_count', models.IntegerField(default=0, verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe6\x89\xab\xe7\xa0\x81\xe6\x95\xb0')),
                ('total_count', models.IntegerField(verbose_name=b'\xe6\x80\xbb\xe6\x95\xb0\xe9\x98\x88\xe5\x80\xbc')),
                ('rate', models.IntegerField(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe9\x80\x9a\xe8\xbf\x87\xe7\x8e\x87')),
                ('pbstatus', models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.PBStatus')),
                ('precastbeam', models.ManyToManyField(to='TaskAndFlow.PrecastBeam', verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe6\x9e\x84\xe4\xbb\xb6')),
            ],
            options={
                'verbose_name': '\u63a8\u9001\u6d88\u606f',
                'verbose_name_plural': '\u63a8\u9001\u6d88\u606f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompGroupType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('descrition', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u5206\u7ec4\u7c7b\u578b',
                'verbose_name_plural': '\u5206\u7ec4\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='compgroup',
            name='type',
            field=models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe7\xb1\xbb\xe5\x9e\x8b', blank=True, to='TaskAndFlow.CompGroupType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pbstatusrecord',
            name='compgroup',
            field=models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe7\xbb\x84', blank=True, to='TaskAndFlow.CompGroup', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pushmessage',
            name='message',
            field=models.CharField(max_length=240, null=True, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9', blank=True),
            preserve_default=True,
        ),
    ]
