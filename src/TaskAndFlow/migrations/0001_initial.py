# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserAndPrj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActorType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe6\x89\xa7\xe8\xa1\x8c\xe8\x80\x85\xe6\x83\x85\xe5\x86\xb5')),
            ],
            options={
                'verbose_name': '\u6267\u884c\u8005\u60c5\u51b5',
                'verbose_name_plural': '\u6267\u884c\u8005\u60c5\u51b5',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CMStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statusname', models.CharField(max_length=60, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u65bd\u5de5\u673a\u68b0\u72b6\u6001',
                'verbose_name_plural': '\u65bd\u5de5\u673a\u68b0\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CMStatusRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4')),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('actor', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u65bd\u5de5\u673a\u68b0\u72b6\u6001\u8bb0\u5f55',
                'verbose_name_plural': '\u65bd\u5de5\u673a\u68b0\u72b6\u6001\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CMType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u65bd\u5de5\u673a\u68b0\u7c7b\u578b',
                'verbose_name_plural': '\u65bd\u5de5\u673a\u68b0\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConstructionMachine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('number', models.CharField(unique=True, max_length=64, verbose_name=b'\xe7\xbc\x96\xe5\x8f\xb7')),
                ('elementid', models.CharField(max_length=60, null=True, verbose_name=b'ElementID', blank=True)),
                ('uniqueid', models.CharField(max_length=60, null=True, verbose_name=b'uniqueID', blank=True)),
                ('postion', models.CharField(max_length=64, null=True, verbose_name=b'\xe4\xbd\x8d\xe7\xbd\xae', blank=True)),
                ('usage', models.CharField(max_length=120, null=True, verbose_name=b'\xe7\x94\xa8\xe9\x80\x94', blank=True)),
                ('specification', models.CharField(max_length=30, null=True, verbose_name=b'\xe8\xa7\x84\xe6\xa0\xbc', blank=True)),
                ('high', models.FloatField(null=True, verbose_name=b'\xe9\xab\x98\xe5\xba\xa6', blank=True)),
                ('cmtype', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe7\xb1\xbb\xe5\x9e\x8b', to='TaskAndFlow.CMType')),
                ('curstatus', models.ForeignKey(verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.CMStatus')),
                ('responsunit', models.ForeignKey(verbose_name=b'\xe8\xb4\x9f\xe8\xb4\xa3\xe5\x8d\x95\xe4\xbd\x8d', blank=True, to='UserAndPrj.Company', null=True)),
            ],
            options={
                'verbose_name': '\u65bd\u5de5\u673a\u68b0',
                'verbose_name_plural': '\u65bd\u5de5\u673a\u68b0',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('createtime', models.DateTimeField(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('creator', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(verbose_name=b'\xe7\x88\xb6\xe7\x9b\xae\xe5\xbd\x95', to='TaskAndFlow.Directory')),
            ],
            options={
                'verbose_name': '\u76ee\u5f55',
                'verbose_name_plural': '\u76ee\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Doc2Relate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relatetype', models.CharField(blank=True, max_length=60, null=True, verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe5\x85\x83\xe7\xb4\xa0\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'\xe6\x9e\x84\xe4\xbb\xb6', b'\xe6\x9e\x84\xe4\xbb\xb6'), (b'\xe4\xbb\xbb\xe5\x8a\xa1', b'\xe4\xbb\xbb\xe5\x8a\xa1'), (b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0', b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0'), (b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4', b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4'), (b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8d\xb1\xe9\x99\xa9\xe6\xba\x90\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8d\xb1\xe9\x99\xa9\xe6\xba\x90\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95')])),
                ('relateid', models.IntegerField(null=True, verbose_name=b'\xe5\x85\x83\xe7\xb4\xa0\xe7\xbc\x96\xe5\x8f\xb7', blank=True)),
                ('createtime', models.DateTimeField(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe6\x97\xb6\xe9\x97\xb4')),
                ('creator', models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u6587\u6863\u5173\u8054\u8868',
                'verbose_name_plural': '\u6587\u6863\u5173\u8054\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('shortname', models.CharField(max_length=60, verbose_name=b'\xe7\xae\x80\xe7\xa7\xb0')),
                ('createtime', models.DateTimeField(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('version', models.CharField(max_length=30, null=True, verbose_name=b'\xe7\x89\x88\xe6\x9c\xac', blank=True)),
                ('filepath', models.FileField(upload_to=b'./upload/', verbose_name=b'\xe8\xb7\xaf\xe5\xbe\x84')),
                ('doctype', models.CharField(max_length=20, choices=[(b'normal', b'\xe5\xb8\xb8\xe8\xa7\x84\xe6\x96\x87\xe6\xa1\xa3'), (b'quality', b'\xe8\xb4\xa8\xe9\x87\x8f\xe6\x96\x87\xe6\xa1\xa3'), (b'technical', b'\xe6\x8a\x80\xe6\x9c\xaf\xe6\x96\xb9\xe6\xa1\x88')])),
                ('creator', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
                ('docdirectory', models.ManyToManyField(to='TaskAndFlow.Directory', verbose_name=b'\xe6\x89\x80\xe5\x9c\xa8\xe7\x9b\xae\xe5\xbd\x95')),
            ],
            options={
                'verbose_name': '\u6587\u6863',
                'verbose_name_plural': '\u6587\u6863',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Elevation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('level', models.CharField(max_length=60, null=True, verbose_name=b'\xe6\xa0\x87\xe9\xab\x98', blank=True)),
                ('sign', models.CharField(max_length=60, null=True, verbose_name=b'\xe6\xa0\x87\xe8\xae\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u6807\u9ad8',
                'verbose_name_plural': '\u6807\u9ad8',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Eventstep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('starttime', models.DateTimeField(verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4')),
                ('endtime', models.DateTimeField(null=True, verbose_name=b'\xe5\xae\x8c\xe6\x88\x90\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
            ],
            options={
                'verbose_name': '\u4e8b\u4ef6\u6b65\u9aa4',
                'verbose_name_plural': '\u4e8b\u4ef6\u6b65\u9aa4',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventStepOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('oprtime', models.DateTimeField(verbose_name=b'\xe6\x93\x8d\xe4\xbd\x9c\xe6\x97\xb6\xe9\x97\xb4')),
                ('comment', models.CharField(max_length=200, null=True, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba', blank=True)),
                ('actor', models.ForeignKey(verbose_name=b'\xe6\x93\x8d\xe4\xbd\x9c\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
                ('eventstep', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe4\xba\x8b\xe4\xbb\xb6\xe6\xad\xa5\xe9\xaa\xa4', to='TaskAndFlow.Eventstep')),
            ],
            options={
                'verbose_name': '\u6d41\u7a0b\u6a21\u677f\u6b65\u9aa4\u64cd\u4f5c',
                'verbose_name_plural': '\u6d41\u7a0b\u6a21\u677f\u6b65\u9aa4\u64cd\u4f5c',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FactoryArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=60, verbose_name=b'\xe5\x9c\xba\xe5\x9c\xb0\xe7\xbc\x96\xe5\x8f\xb7')),
                ('area', models.FloatField(null=True, verbose_name=b'\xe9\x9d\xa2\xe7\xa7\xaf', blank=True)),
                ('length', models.FloatField(null=True, verbose_name=b'\xe9\x95\xbf\xe5\xba\xa6', blank=True)),
                ('width', models.FloatField(null=True, verbose_name=b'\xe5\xae\xbd\xe5\xba\xa6', blank=True)),
                ('elementid', models.CharField(max_length=60, null=True, verbose_name=b'ElementID', blank=True)),
                ('uniqueid', models.CharField(max_length=60, null=True, verbose_name=b'uniqueID', blank=True)),
                ('total', models.FloatField(null=True, verbose_name=b'\xe6\x80\xbb\xe6\x95\xb0\xe9\x87\x8f', blank=True)),
                ('description', models.CharField(max_length=200, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('elevation', models.ForeignKey(verbose_name=b'\xe6\xa0\x87\xe9\xab\x98', to='TaskAndFlow.Elevation', null=True)),
            ],
            options={
                'verbose_name': '\u573a\u5730',
                'verbose_name_plural': '\u573a\u5730',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FactoryPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('number', models.CharField(max_length=60, verbose_name=b'\xe7\xbc\x96\xe5\x8f\xb7')),
                ('area', models.FloatField(null=True, verbose_name=b'\xe9\x9d\xa2\xe7\xa7\xaf', blank=True)),
                ('length', models.FloatField(null=True, verbose_name=b'\xe9\x95\xbf\xe5\xba\xa6', blank=True)),
                ('width', models.FloatField(null=True, verbose_name=b'\xe5\xae\xbd\xe5\xba\xa6', blank=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
            options={
                'verbose_name': '\u573a\u5730\u4ed3\u4f4d',
                'verbose_name_plural': '\u573a\u5730\u4ed3\u4f4d',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlowStepOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe6\x93\x8d\xe4\xbd\x9c\xe5\x90\x8d\xe7\xa7\xb0')),
                ('actortype', models.ForeignKey(verbose_name=b'\xe6\x89\xa7\xe8\xa1\x8c\xe8\x80\x85\xe6\x83\x85\xe5\x86\xb5', to='TaskAndFlow.ActorType')),
            ],
            options={
                'verbose_name': '\u6d41\u7a0b\u6a21\u677f\u6b65\u9aa4\u64cd\u4f5c',
                'verbose_name_plural': '\u6d41\u7a0b\u6a21\u677f\u6b65\u9aa4\u64cd\u4f5c',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlowStepUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isactor', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x89\xa7\xe8\xa1\x8c\xe8\x80\x85')),
            ],
            options={
                'verbose_name': '\u6d41\u7a0b\u6a21\u677f\u6b65\u9aa4\u4eba\u5458',
                'verbose_name_plural': '\u6d41\u7a0b\u6a21\u677f\u6b65\u9aa4\u4eba\u5458',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlowTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xa8\xa1\xe6\x9d\xbf\xe5\x90\x8d\xe7\xa7\xb0')),
                ('describe', models.CharField(max_length=120, verbose_name=b'\xe6\xa8\xa1\xe6\x9d\xbf\xe6\x8f\x8f\xe8\xbf\xb0')),
            ],
            options={
                'verbose_name': '\u6d41\u7a0b\u6a21\u677f',
                'verbose_name_plural': '\u6d41\u7a0b\u6a21\u677f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlowTemplateStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe6\xb5\x81\xe7\xa8\x8b\xe5\x90\x8d\xe7\xa7\xb0')),
                ('isstartstep', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xb5\xb7\xe5\xa7\x8b\xe6\xad\xa5\xe9\xaa\xa4')),
                ('isendstep', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe7\xbb\x93\xe6\x9d\x9f\xe6\xad\xa5\xe9\xaa\xa4')),
                ('isautotransfer', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\x87\xaa\xe5\x8a\xa8\xe6\xb5\x81\xe8\xbd\xac')),
                ('template', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe6\xa8\xa1\xe6\x9d\xbf', to='TaskAndFlow.FlowTemplate')),
            ],
            options={
                'verbose_name': '\u6d41\u7a0b\u6a21\u677f\u6b65\u9aa4',
                'verbose_name_plural': '\u6d41\u7a0b\u6a21\u677f\u6b65\u9aa4',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlowType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe6\xb5\x81\xe7\xa8\x8b\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u6d41\u7a0b\u7c7b\u578b',
                'verbose_name_plural': '\u6d41\u7a0b\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hazard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('number', models.CharField(unique=True, max_length=64, verbose_name=b'\xe7\xbc\x96\xe5\x8f\xb7')),
                ('remarks', models.CharField(max_length=120, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('relatetype', models.CharField(blank=True, max_length=60, null=True, verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe5\x85\x83\xe7\xb4\xa0\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'\xe6\x9e\x84\xe4\xbb\xb6', b'\xe6\x9e\x84\xe4\xbb\xb6'), (b'\xe4\xbb\xbb\xe5\x8a\xa1', b'\xe4\xbb\xbb\xe5\x8a\xa1'), (b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0', b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0'), (b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4', b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4'), (b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8d\xb1\xe9\x99\xa9\xe6\xba\x90\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8d\xb1\xe9\x99\xa9\xe6\xba\x90\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95')])),
                ('relateid', models.IntegerField(null=True, verbose_name=b'\xe5\x85\x83\xe7\xb4\xa0\xe7\xbc\x96\xe5\x8f\xb7', blank=True)),
            ],
            options={
                'verbose_name': '\u91cd\u5927\u5371\u9669\u6e90',
                'verbose_name_plural': '\u91cd\u5927\u5371\u9669\u6e90',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HazardStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statusname', models.CharField(max_length=60, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0')),
                ('nextstatus', models.ForeignKey(verbose_name=b'\xe4\xb8\x8b\xe4\xb8\x80\xe7\x8a\xb6\xe6\x80\x81', blank=True, to='TaskAndFlow.HazardStatus', null=True)),
            ],
            options={
                'verbose_name': '\u91cd\u5927\u5371\u9669\u6e90\u72b6\u6001',
                'verbose_name_plural': '\u91cd\u5927\u5371\u9669\u6e90\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HazardStatusRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4')),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('actor', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
                ('hazard', models.ForeignKey(verbose_name=b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8d\xb1\xe9\x99\xa9\xe6\xba\x90', to='TaskAndFlow.Hazard')),
                ('status', models.ForeignKey(verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.HazardStatus')),
            ],
            options={
                'verbose_name': '\u91cd\u5927\u5371\u9669\u6e90\u72b6\u6001\u8bb0\u5f55',
                'verbose_name_plural': '\u91cd\u5927\u5371\u9669\u6e90\u72b6\u6001\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HazardType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u91cd\u5927\u5371\u9669\u6e90\u7c7b\u578b',
                'verbose_name_plural': '\u91cd\u5927\u5371\u9669\u6e90\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=240, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('isread', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe8\xaf\xbb')),
                ('readtime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe8\xaf\xbb\xe5\x8f\x96\xe6\x97\xb6\xe9\x97\xb4')),
                ('sendtime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x8f\x91\xe8\xb5\xb7\xe6\x97\xb6\xe9\x97\xb4')),
                ('relatetype', models.CharField(blank=True, max_length=60, null=True, verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe5\x85\x83\xe7\xb4\xa0\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'\xe6\x9e\x84\xe4\xbb\xb6', b'\xe6\x9e\x84\xe4\xbb\xb6'), (b'\xe4\xbb\xbb\xe5\x8a\xa1', b'\xe4\xbb\xbb\xe5\x8a\xa1'), (b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0', b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0'), (b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4', b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4'), (b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8d\xb1\xe9\x99\xa9\xe6\xba\x90\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8d\xb1\xe9\x99\xa9\xe6\xba\x90\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95'), (b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95', b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xae\xe6\x94\xb9\xe8\xae\xb0\xe5\xbd\x95')])),
                ('relateid', models.IntegerField(null=True, verbose_name=b'\xe5\x85\x83\xe7\xb4\xa0\xe7\xbc\x96\xe5\x8f\xb7', blank=True)),
                ('receiver', models.ForeignKey(related_name='receiver', verbose_name=b'\xe6\x8e\xa5\xe6\x94\xb6\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sender', verbose_name=b'\xe5\x8f\x91\xe8\xb5\xb7\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u6d88\u606f',
                'verbose_name_plural': '\u6d88\u606f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('priority', models.IntegerField(default=0, verbose_name=b'\xe9\x87\x8d\xe8\xa6\x81\xe6\x80\xa7')),
            ],
            options={
                'verbose_name': '\u6d88\u606f\u7c7b\u578b',
                'verbose_name_plural': '\u6d88\u606f\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('message', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4')),
                ('sender', models.ForeignKey(verbose_name=b'\xe5\x8f\x91\xe8\xb5\xb7\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u901a\u77e5',
                'verbose_name_plural': '\u901a\u77e5',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PBMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'\xe9\x92\xa2\xe6\x9d\x90', b'\xe9\x92\xa2\xe6\x9d\x90'), (b'\xe6\xb7\xb7\xe6\xb3\xa5\xe5\x9c\x9f', b'\xe6\xb7\xb7\xe6\xb3\xa5\xe5\x9c\x9f'), (b'\xe9\x92\xa2\xe7\xad\x8b', b'\xe9\x92\xa2\xe7\xad\x8b')])),
                ('specification', models.CharField(max_length=30, null=True, verbose_name=b'\xe8\xa7\x84\xe6\xa0\xbc', blank=True)),
                ('size', models.CharField(max_length=30, null=True, verbose_name=b'\xe6\x9d\x90\xe6\x96\x99\xe5\xb0\xba\xe5\xaf\xb8', blank=True)),
            ],
            options={
                'verbose_name': '\u6784\u4ef6\u6750\u6599',
                'verbose_name_plural': '\u6784\u4ef6\u6750\u6599',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PBStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statusname', models.CharField(max_length=60, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0')),
                ('factoryarea', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x9c\xba\xe5\x9c\xb0', blank=True, to='TaskAndFlow.FactoryArea', null=True)),
                ('nextstatus', models.ForeignKey(verbose_name=b'\xe4\xb8\x8b\xe4\xb8\x80\xe7\x8a\xb6\xe6\x80\x81', blank=True, to='TaskAndFlow.PBStatus', null=True)),
            ],
            options={
                'verbose_name': '\u6784\u4ef6\u72b6\u6001',
                'verbose_name_plural': '\u6784\u4ef6\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PBStatusRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4')),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('actor', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
                ('factoryposition', models.ForeignKey(verbose_name=b'\xe5\x9c\xba\xe5\x9c\xb0\xe4\xbb\x93\xe4\xbd\x8d', blank=True, to='TaskAndFlow.FactoryPosition', null=True)),
            ],
            options={
                'verbose_name': '\u6784\u4ef6\u72b6\u6001\u8bb0\u5f55\u8868',
                'verbose_name_plural': '\u6784\u4ef6\u72b6\u6001\u8bb0\u5f55\u8868',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PBType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('classificationcode', models.CharField(max_length=60, null=True, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb\xe7\xbc\x96\xe7\xa0\x81', blank=True)),
                ('sign', models.CharField(max_length=60, null=True, verbose_name=b'\xe6\xa0\x87\xe8\xae\xb0', blank=True)),
                ('familyname', models.CharField(max_length=60, null=True, verbose_name=b'\xe6\x97\x8f\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('isprebuilt', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\xa2\x84\xe5\x88\xb6')),
                ('major', models.ForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', to='UserAndPrj.UserMajor')),
                ('material', models.ForeignKey(verbose_name=b'\xe6\x9d\x90\xe6\x96\x99', to='TaskAndFlow.PBMaterial', null=True)),
            ],
            options={
                'verbose_name': '\u6784\u4ef6\u7c7b\u578b',
                'verbose_name_plural': '\u6784\u4ef6\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrecastBeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(unique=True, max_length=64, verbose_name=b'GUID')),
                ('revitfilename', models.CharField(max_length=60, verbose_name=b'Revit\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d')),
                ('elementid', models.CharField(max_length=60, verbose_name=b'ElementID')),
                ('uniqueid', models.CharField(max_length=60, verbose_name=b'uniqueID')),
                ('number', models.CharField(unique=True, max_length=64, verbose_name=b'\xe7\xbc\x96\xe5\x8f\xb7')),
                ('weight', models.FloatField(null=True, verbose_name=b'\xe9\x87\x8d\xe9\x87\x8f', blank=True)),
                ('volume', models.FloatField(null=True, verbose_name=b'\xe4\xbd\x93\xe7\xa7\xaf', blank=True)),
                ('width', models.FloatField(null=True, verbose_name=b'\xe5\xae\xbd\xe5\xba\xa6', blank=True)),
                ('high', models.FloatField(null=True, verbose_name=b'\xe9\xab\x98\xe5\xba\xa6', blank=True)),
                ('sign', models.CharField(max_length=60, null=True, verbose_name=b'\xe6\xa0\x87\xe8\xae\xb0', blank=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('drawnumber', models.CharField(max_length=60, null=True, verbose_name=b'\xe5\x9b\xbe\xe7\xba\xb8\xe7\xbc\x96\xe5\x8f\xb7', blank=True)),
                ('pbpostion', models.CharField(max_length=64, null=True, verbose_name=b'\xe4\xbd\x8d\xe7\xbd\xae\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2', blank=True)),
                ('parentguid', models.CharField(max_length=64, null=True, verbose_name=b'\xe7\x88\xb6\xe6\x9e\x84\xe4\xbb\xb6GUID', blank=True)),
                ('curstatus', models.ForeignKey(verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe7\x8a\xb6\xe6\x80\x81', blank=True, to='TaskAndFlow.PBStatus', null=True)),
                ('elevation', models.ForeignKey(verbose_name=b'\xe6\xa5\xbc\xe5\xb1\x82', to='TaskAndFlow.Elevation', null=True)),
                ('pbtype', models.ForeignKey(verbose_name=b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b', blank=True, to='TaskAndFlow.PBType', null=True)),
            ],
            options={
                'verbose_name': '\u6784\u4ef6',
                'verbose_name_plural': '\u6784\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='projectevent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=60, verbose_name=b'\xe7\xbc\x96\xe5\x8f\xb7')),
                ('describe', models.CharField(max_length=120, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('deadline', models.DateTimeField(verbose_name=b'\xe6\x88\xaa\xe6\xad\xa2\xe6\x97\xb6\xe9\x97\xb4')),
                ('priority', models.IntegerField(default=0, verbose_name=b'\xe4\xbc\x98\xe5\x85\x88\xe7\xba\xa7')),
                ('relatetype', models.CharField(max_length=60, verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe5\x85\x83\xe7\xb4\xa0\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('relateid', models.IntegerField(verbose_name=b'\xe5\x85\x83\xe7\xb4\xa0\xe7\xbc\x96\xe5\x8f\xb7')),
                ('curflowstep', models.ForeignKey(verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4', to='TaskAndFlow.FlowTemplateStep')),
                ('template', models.ForeignKey(verbose_name=b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xa8\xa1\xe6\x9d\xbf', to='TaskAndFlow.FlowTemplate')),
            ],
            options={
                'verbose_name': '\u4e8b\u4ef6',
                'verbose_name_plural': '\u4e8b\u4ef6',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msprojectid', models.CharField(max_length=30, verbose_name=b'', blank=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d\xe7\xa7\xb0')),
                ('planstart', models.DateTimeField(verbose_name=b'\xe8\xae\xa1\xe5\x88\x92\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4')),
                ('planfinish', models.DateTimeField(verbose_name=b'\xe8\xae\xa1\xe5\x88\x92\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4')),
                ('actualstart', models.DateTimeField(null=True, verbose_name=b'\xe5\xae\x9e\xe9\x99\x85\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('acutalfinish', models.DateTimeField(null=True, verbose_name=b'\xe5\xae\x9e\xe9\x99\x85\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('percentage', models.FloatField(default=0, verbose_name=b'\xe5\xae\x8c\xe6\x88\x90\xe7\x99\xbe\xe5\x88\x86\xe6\xaf\x94')),
                ('ismilestone', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\x87\x8c\xe7\xa8\x8b\xe7\xa2\x91\xe8\x8a\x82\xe7\x82\xb9')),
                ('iskeypath', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x85\xb3\xe9\x94\xae\xe8\xb7\xaf\xe5\xbe\x84')),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('constructionunit', models.ForeignKey(verbose_name=b'\xe6\x96\xbd\xe5\xb7\xa5\xe5\x8d\x95\xe4\xbd\x8d', blank=True, to='UserAndPrj.Company', null=True)),
            ],
            options={
                'verbose_name': '\u751f\u4ea7\u4efb\u52a1',
                'verbose_name_plural': '\u751f\u4ea7\u4efb\u52a1',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statusname', models.CharField(max_length=60, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81\xe5\x90\x8d\xe7\xa7\xb0')),
                ('nextstatus', models.ForeignKey(verbose_name=b'\xe4\xb8\x8b\xe4\xb8\x80\xe7\x8a\xb6\xe6\x80\x81', blank=True, to='TaskAndFlow.TaskStatus', null=True)),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u72b6\u6001',
                'verbose_name_plural': '\u4efb\u52a1\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskStatusRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4')),
                ('description', models.CharField(max_length=200, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('actor', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.TaskStatus')),
                ('task', models.ForeignKey(verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1', to='TaskAndFlow.ProjectTask')),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u72b6\u6001\u8bb0\u5f55',
                'verbose_name_plural': '\u4efb\u52a1\u72b6\u6001\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u7c7b\u578b',
                'verbose_name_plural': '\u4efb\u52a1\u7c7b\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u5355\u4f4d\u5de5\u7a0b',
                'verbose_name_plural': '\u5355\u4f4d\u5de5\u7a0b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User2CMStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.ForeignKey(verbose_name=b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.CMStatus')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u65bd\u5de5\u673a\u68b0\u72b6\u6001',
                'verbose_name_plural': '\u7528\u6237\u65bd\u5de5\u673a\u68b0\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User2HazardStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.ForeignKey(verbose_name=b'\xe9\x87\x8d\xe5\xa4\xa7\xe5\x8d\xb1\xe9\x99\xa9\xe6\xba\x90\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.HazardStatus')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u91cd\u5927\u5371\u9669\u6e90\u72b6\u6001',
                'verbose_name_plural': '\u7528\u6237\u91cd\u5927\u5371\u9669\u6e90\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User2PBStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.ForeignKey(verbose_name=b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.PBStatus')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6784\u4ef6\u72b6\u6001',
                'verbose_name_plural': '\u7528\u6237\u6784\u4ef6\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User2TaskStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.ForeignKey(verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.TaskStatus')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u4efb\u52a1\u72b6\u6001',
                'verbose_name_plural': '\u7528\u6237\u4efb\u52a1\u72b6\u6001',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='user2taskstatus',
            unique_together=set([('user', 'status')]),
        ),
        migrations.AlterUniqueTogether(
            name='user2pbstatus',
            unique_together=set([('user', 'status')]),
        ),
        migrations.AlterUniqueTogether(
            name='user2hazardstatus',
            unique_together=set([('user', 'status')]),
        ),
        migrations.AlterUniqueTogether(
            name='user2cmstatus',
            unique_together=set([('user', 'status')]),
        ),
        migrations.AlterUniqueTogether(
            name='taskstatusrecord',
            unique_together=set([('status', 'task')]),
        ),
        migrations.AddField(
            model_name='taskstatus',
            name='tasktype',
            field=models.ForeignKey(verbose_name=b'\xe4\xbb\xbb\xe5\x8a\xa1\xe7\xb1\xbb\xe5\x9e\x8b', blank=True, to='TaskAndFlow.TaskType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='curstatus',
            field=models.ForeignKey(verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe7\x8a\xb6\xe6\x80\x81', blank=True, to='TaskAndFlow.TaskStatus', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='major',
            field=models.ForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', blank=True, to='UserAndPrj.UserMajor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='parentid',
            field=models.ForeignKey(verbose_name=b'\xe7\x88\xb6\xe8\x8a\x82\xe7\x82\xb9', to='TaskAndFlow.ProjectTask'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='type',
            field=models.ForeignKey(verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', to='TaskAndFlow.TaskType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='precastbeam',
            name='task',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe4\xbb\xbb\xe5\x8a\xa1', blank=True, to='TaskAndFlow.ProjectTask', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pbstatusrecord',
            name='precastbeam',
            field=models.ForeignKey(verbose_name=b'\xe6\x9e\x84\xe4\xbb\xb6', to='TaskAndFlow.PrecastBeam'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pbstatusrecord',
            name='status',
            field=models.ForeignKey(verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.PBStatus'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pbstatusrecord',
            unique_together=set([('status', 'precastbeam')]),
        ),
        migrations.AddField(
            model_name='pbstatus',
            name='pbtype',
            field=models.ForeignKey(verbose_name=b'\xe6\x9e\x84\xe4\xbb\xb6\xe7\xb1\xbb\xe5\x9e\x8b', to='TaskAndFlow.PBType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='type',
            field=models.ForeignKey(verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', to='TaskAndFlow.MessageType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='hazardstatusrecord',
            unique_together=set([('status', 'hazard')]),
        ),
        migrations.AddField(
            model_name='hazard',
            name='curstatus',
            field=models.ForeignKey(verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.HazardStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='hazardtype',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe7\xb1\xbb\xe5\x9e\x8b', to='TaskAndFlow.HazardType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='major',
            field=models.ForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', to='UserAndPrj.UserMajor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='responsunit',
            field=models.ForeignKey(verbose_name=b'\xe8\xb4\x9f\xe8\xb4\xa3\xe5\x8d\x95\xe4\xbd\x8d', to='UserAndPrj.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flowtemplate',
            name='flowtype',
            field=models.ForeignKey(verbose_name=b'\xe6\xb5\x81\xe7\xa8\x8b\xe7\xb1\xbb\xe5\x9e\x8b', to='TaskAndFlow.FlowType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flowtemplate',
            name='major',
            field=models.ForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', to='UserAndPrj.UserMajor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flowstepuser',
            name='flowstep',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4', to='TaskAndFlow.FlowTemplateStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flowstepuser',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flowstepoperation',
            name='flowstep',
            field=models.ForeignKey(related_name='flowstep', verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4', to='TaskAndFlow.FlowTemplateStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flowstepoperation',
            name='nextflowstep',
            field=models.ForeignKey(related_name='nextflowstep', verbose_name=b'\xe4\xb8\x8b\xe4\xb8\x80\xe6\xad\xa5\xe9\xaa\xa4', to='TaskAndFlow.FlowTemplateStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventstepoperation',
            name='flowstepoper',
            field=models.ForeignKey(verbose_name=b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xa8\xa1\xe6\x9d\xbf\xe6\xad\xa5\xe9\xaa\xa4\xe6\x93\x8d\xe4\xbd\x9c', to='TaskAndFlow.FlowStepOperation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventstep',
            name='flowstep',
            field=models.ForeignKey(verbose_name=b'\xe6\xb5\x81\xe7\xa8\x8b\xe6\xad\xa5\xe9\xaa\xa4', to='TaskAndFlow.FlowTemplateStep'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventstep',
            name='projectevent',
            field=models.ForeignKey(verbose_name=b'\xe4\xba\x8b\xe4\xbb\xb6', to='TaskAndFlow.projectevent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='elevation',
            name='unitproject',
            field=models.ForeignKey(verbose_name=b'\xe5\x8d\x95\xe4\xbd\x8d\xe5\xb7\xa5\xe7\xa8\x8b', to='TaskAndFlow.UnitProject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='doc2relate',
            name='document',
            field=models.ForeignKey(verbose_name=b'\xe6\x96\x87\xe6\xa1\xa3', to='TaskAndFlow.Document'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cmstatusrecord',
            name='constructionmachine',
            field=models.ForeignKey(verbose_name=b'\xe6\x96\xbd\xe5\xb7\xa5\xe6\x9c\xba\xe6\xa2\xb0', to='TaskAndFlow.ConstructionMachine'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cmstatusrecord',
            name='status',
            field=models.ForeignKey(verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', to='TaskAndFlow.CMStatus'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='cmstatusrecord',
            unique_together=set([('status', 'constructionmachine')]),
        ),
        migrations.AddField(
            model_name='cmstatus',
            name='cmtype',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe7\xb1\xbb\xe5\x9e\x8b', to='TaskAndFlow.CMType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cmstatus',
            name='nextstatus',
            field=models.ForeignKey(verbose_name=b'\xe4\xb8\x8b\xe4\xb8\x80\xe7\x8a\xb6\xe6\x80\x81', blank=True, to='TaskAndFlow.CMStatus', null=True),
            preserve_default=True,
        ),
    ]
