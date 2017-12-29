# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import TaskAndFlow.models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmstatusrecord',
            name='actor',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='constructionmachine',
            name='responsunit',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe8\xb4\x9f\xe8\xb4\xa3\xe5\x8d\x95\xe4\xbd\x8d', blank=True, to='UserAndPrj.Company', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='directory',
            name='creator',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='doc2relate',
            name='creator',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='creator',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventstepoperation',
            name='actor',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe6\x93\x8d\xe4\xbd\x9c\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flowstepuser',
            name='user',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flowtemplate',
            name='major',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', to='UserAndPrj.UserMajor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hazard',
            name='major',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', to='UserAndPrj.UserMajor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hazard',
            name='responsunit',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe8\xb4\x9f\xe8\xb4\xa3\xe5\x8d\x95\xe4\xbd\x8d', to='UserAndPrj.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hazardstatusrecord',
            name='actor',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=TaskAndFlow.models.CrossDbForeignKey(related_name='receiver', verbose_name=b'\xe6\x8e\xa5\xe6\x94\xb6\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=TaskAndFlow.models.CrossDbForeignKey(related_name='sender', verbose_name=b'\xe5\x8f\x91\xe8\xb5\xb7\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notice',
            name='sender',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe5\x8f\x91\xe8\xb5\xb7\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pbstatusrecord',
            name='actor',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pbtype',
            name='major',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', to='UserAndPrj.UserMajor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='precastbeam',
            name='elementid',
            field=models.CharField(max_length=60, null=True, verbose_name=b'ElementID', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='precastbeam',
            name='revitfilename',
            field=models.CharField(max_length=60, null=True, verbose_name=b'Revit\xe6\x96\x87\xe4\xbb\xb6\xe5\x90\x8d', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='precastbeam',
            name='uniqueid',
            field=models.CharField(max_length=60, null=True, verbose_name=b'uniqueID', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='constructionunit',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe6\x96\xbd\xe5\xb7\xa5\xe5\x8d\x95\xe4\xbd\x8d', blank=True, to='UserAndPrj.Company', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='major',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', blank=True, to='UserAndPrj.UserMajor', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taskstatusrecord',
            name='actor',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user2cmstatus',
            name='user',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user2hazardstatus',
            name='user',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user2pbstatus',
            name='user',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user2taskstatus',
            name='user',
            field=TaskAndFlow.models.CrossDbForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
