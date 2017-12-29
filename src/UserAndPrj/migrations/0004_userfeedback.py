# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('UserAndPrj', '0003_usertemplate_pro'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('submittime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x8f\x90\xe4\xba\xa4\xe6\x97\xb6\xe9\x97\xb4')),
                ('content', models.CharField(max_length=400, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('prj', models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe9\xa1\xb9\xe7\x9b\xae', blank=True, to='UserAndPrj.Project', null=True)),
                ('submitor', models.ForeignKey(verbose_name=b'\xe6\x8f\x90\xe4\xba\xa4\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4f7f\u7528\u53cd\u9988',
                'verbose_name_plural': '\u4f7f\u7528\u53cd\u9988',
            },
            bases=(models.Model,),
        ),
    ]
