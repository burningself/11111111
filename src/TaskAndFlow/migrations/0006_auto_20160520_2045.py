# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0005_precastbeam_lvmdbid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectModels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('modelfile', models.FileField(upload_to=b'', verbose_name=b'\xe6\xa8\xa1\xe5\x9e\x8b\xe6\x96\x87\xe4\xbb\xb6')),
            ],
            options={
                'verbose_name': '\u9879\u76ee\u6a21\u578b',
                'verbose_name_plural': '\u9879\u76ee\u6a21\u578b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='precastbeam',
            name='curfactoryarea',
            field=models.ForeignKey(verbose_name=b'\xe5\xbd\x93\xe5\x89\x8d\xe5\x9c\xba\xe5\x9c\xb0', blank=True, to='TaskAndFlow.FactoryArea', null=True),
            preserve_default=True,
        ),
    ]
