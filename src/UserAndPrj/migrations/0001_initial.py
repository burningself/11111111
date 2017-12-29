# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('parent', models.ForeignKey(blank=True, to='UserAndPrj.Company', null=True)),
            ],
            options={
                'verbose_name': '\u4f01\u4e1a',
                'verbose_name_plural': '\u4f01\u4e1a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe9\xa1\xb9\xe7\x9b\xae\xe5\x90\x8d\xe7\xa7\xb0')),
                ('address', models.CharField(max_length=120, verbose_name=b'\xe9\xa1\xb9\xe7\x9b\xae\xe5\x9c\xb0\xe5\x9d\x80')),
                ('area', models.FloatField(verbose_name=b'\xe5\xbb\xba\xe7\xad\x91\xe9\x9d\xa2\xe7\xa7\xaf')),
                ('cost', models.FloatField(verbose_name=b'\xe5\xb7\xa5\xe7\xa8\x8b\xe9\x80\xa0\xe4\xbb\xb7')),
                ('type', models.CharField(max_length=60, verbose_name=b'\xe5\xb7\xa5\xe7\xa8\x8b\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('projecturl', models.URLField(max_length=120, verbose_name=b'\xe9\xa1\xb9\xe7\x9b\xae\xe7\xbd\x91\xe5\x9d\x80')),
                ('builder', models.OneToOneField(related_name='builder', verbose_name=b'\xe6\x96\xbd\xe5\xb7\xa5\xe5\x8d\x95\xe4\xbd\x8d', to='UserAndPrj.Company')),
                ('constrator', models.OneToOneField(related_name='constrator', verbose_name=b'\xe5\xbb\xba\xe8\xae\xbe\xe5\x8d\x95\xe4\xbd\x8d', to='UserAndPrj.Company')),
            ],
            options={
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('name', models.CharField(unique=True, max_length=100, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('contract', models.CharField(max_length=40, null=True, verbose_name=b'\xe8\x81\x94\xe7\xb3\xbb\xe6\x96\xb9\xe5\xbc\x8f', blank=True)),
                ('truename', models.CharField(max_length=20, null=True, verbose_name=b'\xe5\xae\x9e\xe9\x99\x85\xe5\xa7\x93\xe5\x90\x8d', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('is_admin', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xb6\x85\xe7\xba\xa7\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98')),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth', models.CharField(max_length=60, verbose_name=b'\xe6\x9d\x83\xe9\x99\x90', choices=[(b'\xe6\x9e\x84\xe4\xbb\xb6\xe6\x89\xab\xe7\xa0\x81', b'\xe6\x9e\x84\xe4\xbb\xb6\xe6\x89\xab\xe7\xa0\x81'), (b'\xe6\x89\x93\xe5\x8d\xb0\xe4\xba\x8c\xe7\xbb\xb4\xe7\xa0\x81', b'\xe6\x89\x93\xe5\x8d\xb0\xe4\xba\x8c\xe7\xbb\xb4\xe7\xa0\x81'), (b'\xe4\xbf\xae\xe6\x94\xb9\xe6\xb5\x81\xe7\xa8\x8b\xe6\xa8\xa1\xe6\x9d\xbf', b'\xe4\xbf\xae\xe6\x94\xb9\xe6\xb5\x81\xe7\xa8\x8b\xe6\xa8\xa1\xe6\x9d\xbf'), (b'\xe4\xbf\xae\xe6\x94\xb9\xe7\x8a\xb6\xe6\x80\x81', b'\xe4\xbf\xae\xe6\x94\xb9\xe7\x8a\xb6\xe6\x80\x81')])),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6743\u9650',
                'verbose_name_plural': '\u7528\u6237\u6743\u9650',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserMajor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u4e13\u4e1a',
                'verbose_name_plural': '\u7528\u6237\u4e13\u4e1a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('project', models.ForeignKey(verbose_name=b'\xe9\xa1\xb9\xe7\x9b\xae', to='UserAndPrj.Project')),
            ],
            options={
                'verbose_name': '\u7528\u6237-\u9879\u76ee-\u89d2\u8272',
                'verbose_name_plural': '\u7528\u6237-\u9879\u76ee-\u89d2\u8272',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe8\xa7\x92\xe8\x89\xb2')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u89d2\u8272',
                'verbose_name_plural': '\u7528\u6237\u89d2\u8272',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRoleAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth', models.ForeignKey(verbose_name=b'\xe6\x9d\x83\xe9\x99\x90', to='UserAndPrj.UserAuthor')),
                ('role', models.ForeignKey(verbose_name=b'\xe8\xa7\x92\xe8\x89\xb2', to='UserAndPrj.UserRole')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u89d2\u8272\u6743\u9650',
                'verbose_name_plural': '\u7528\u6237\u89d2\u8272\u6743\u9650',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='UserRoles',
            name='role',
            field=models.ForeignKey(verbose_name=b'\xe8\xa7\x92\xe8\x89\xb2', to='UserAndPrj.UserRole'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='UserRoles',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to='UserAndPrj.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='auth',
            field=models.ManyToManyField(to='UserAndPrj.UserAuthor', null=True, verbose_name=b'\xe6\x9d\x83\xe9\x99\x90', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe4\xbc\x81\xe4\xb8\x9a', blank=True, to='UserAndPrj.Company', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='major',
            field=models.ForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', blank=True, to='UserAndPrj.UserMajor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='economist',
            field=models.OneToOneField(related_name='economist', verbose_name=b'\xe7\xbb\x8f\xe6\xb5\x8e\xe5\xb8\x88', to='UserAndPrj.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='engineer',
            field=models.OneToOneField(related_name='engineer', verbose_name=b'\xe5\xb7\xa5\xe7\xa8\x8b\xe5\xb8\x88', to='UserAndPrj.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='manager',
            field=models.OneToOneField(related_name='manager', verbose_name=b'\xe9\xa1\xb9\xe7\x9b\xae\xe7\xbb\x8f\xe7\x90\x86', to='UserAndPrj.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='productionmanager',
            field=models.OneToOneField(related_name='productionmanager', verbose_name=b'\xe7\x94\x9f\xe4\xba\xa7\xe7\xbb\x8f\xe7\x90\x86', to='UserAndPrj.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.OneToOneField(related_name='supervisor', verbose_name=b'\xe7\x9b\x91\xe7\x90\x86\xe5\x8d\x95\xe4\xbd\x8d', to='UserAndPrj.Company'),
            preserve_default=True,
        ),
    ]
