# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('UserAndPrj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPageTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe6\xa8\xa1\xe6\x9d\xbf\xe5\x90\x8d\xe7\xa7\xb0')),
            ],
            options={
                'verbose_name': '\u6a21\u677f\u540d\u79f0-\u5c55\u793a\u6a21\u5757',
                'verbose_name_plural': '\u6a21\u677f\u540d\u79f0-\u5c55\u793a\u6a21\u5757',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x8f\xaf\xe5\xae\x9a\xe5\x88\xb6\xe9\xa1\xb5\xe9\x9d\xa2')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubPageModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\xad\x90\xe6\xa8\xa1\xe5\x9d\x97')),
                ('parent', models.ForeignKey(verbose_name=b'\xe5\x8f\xaf\xe5\xae\x9a\xe5\x88\xb6\xe9\xa1\xb5\xe9\x9d\xa2', to='UserAndPrj.PageModel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template', models.CharField(max_length=60, verbose_name=b'\xe6\xa8\xa1\xe6\x9d\xbf\xe5\x90\x8d\xe7\xa7\xb0')),
                ('is_active', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x90\xaf\xe7\x94\xa8')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237-\u914d\u7f6e\u6a21\u677f',
                'verbose_name_plural': '\u7528\u6237-\u914d\u7f6e\u6a21\u677f',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='custompagetemplate',
            name='subPageConfig',
            field=models.ForeignKey(verbose_name=b'\xe5\xb1\x95\xe7\xa4\xba\xe6\xa8\xa1\xe5\x9d\x97', to='UserAndPrj.SubPageModel'),
            preserve_default=True,
        ),
    ]
