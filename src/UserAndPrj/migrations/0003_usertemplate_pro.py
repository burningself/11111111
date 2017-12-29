# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserAndPrj', '0002_auto_20160422_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertemplate',
            name='pro',
            field=models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe9\xa1\xb9\xe7\x9b\xae', blank=True, to='UserAndPrj.Project', null=True),
            preserve_default=True,
        ),
    ]
