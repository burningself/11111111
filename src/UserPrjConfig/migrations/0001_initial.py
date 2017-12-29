# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import Scc4PM.dbsetings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60, verbose_name=b'\xe6\x9d\x83\xe9\x99\x90')),
                ('permdict', models.CharField(max_length=512, verbose_name=b'\xe6\x9d\x83\xe9\x99\x90\xe5\xad\x97\xe5\x85\xb8')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6743\u9650',
                'verbose_name_plural': '\u7528\u6237\u6743\u9650',
            },
        ),
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submittime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x8f\x90\xe4\xba\xa4\xe6\x97\xb6\xe9\x97\xb4')),
                ('content', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('submitor', Scc4PM.dbsetings.CrossDbForeignKey(verbose_name=b'\xe6\x8f\x90\xe4\xba\xa4\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4f7f\u7528\u53cd\u9988',
                'verbose_name_plural': '\u4f7f\u7528\u53cd\u9988',
            },
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237-\u9879\u76ee-\u89d2\u8272',
                'verbose_name_plural': '\u7528\u6237-\u9879\u76ee-\u89d2\u8272',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe8\xa7\x92\xe8\x89\xb2')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u89d2\u8272',
                'verbose_name_plural': '\u7528\u6237\u89d2\u8272',
            },
        ),
        migrations.CreateModel(
            name='UserRoleAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth', models.ForeignKey(verbose_name=b'\xe6\x9d\x83\xe9\x99\x90', to='UserPrjConfig.UserAuthor')),
                ('role', models.ForeignKey(verbose_name=b'\xe8\xa7\x92\xe8\x89\xb2', to='UserPrjConfig.UserRole')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u89d2\u8272\u6743\u9650',
                'verbose_name_plural': '\u7528\u6237\u89d2\u8272\u6743\u9650',
            },
        ),
        migrations.AddField(
            model_name='UserRoles',
            name='role',
            field=models.ForeignKey(verbose_name=b'\xe8\xa7\x92\xe8\x89\xb2', to='UserPrjConfig.UserRole'),
        ),
        migrations.AddField(
            model_name='UserRoles',
            name='user',
            field=Scc4PM.dbsetings.CrossDbForeignKey(related_name='user', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userroleauthor',
            unique_together=set([('role', 'auth')]),
        ),
        migrations.AlterUniqueTogether(
            name='UserRoles',
            unique_together=set([('user', 'role')]),
        ),
    ]
