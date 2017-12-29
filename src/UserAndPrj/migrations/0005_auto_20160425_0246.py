# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserAndPrj', '0004_userfeedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custompagetemplate',
            name='subPageConfig',
        ),
        migrations.DeleteModel(
            name='CustomPageTemplate',
        ),
        migrations.RemoveField(
            model_name='subpagemodel',
            name='parent',
        ),
        migrations.DeleteModel(
            name='SubPageModel',
        ),
        migrations.RemoveField(
            model_name='usertemplate',
            name='template',
        ),
        migrations.AddField(
            model_name='usertemplate',
            name='configData',
            field=models.CharField(default=None, max_length=200, verbose_name=b'\xe6\xa8\xa1\xe6\x9d\xbf \xe4\xbf\xa1\xe6\x81\xaf'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usertemplate',
            name='name',
            field=models.CharField(default=None, max_length=40, verbose_name=b'\xe6\xa8\xa1\xe6\x9d\xbf\xe5\x90\x8d\xe7\xa7\xb0'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usertemplate',
            name='page',
            field=models.CharField(default=None, max_length=200, verbose_name=b'\xe9\xa1\xb5\xe9\x9d\xa2\xe5\x90\x8d\xe7\xa7\xb0'),
            preserve_default=True,
        ),
    ]
