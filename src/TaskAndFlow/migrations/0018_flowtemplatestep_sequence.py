# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0017_auto_20160623_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowtemplatestep',
            name='sequence',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\xba\x8f\xe5\x8f\xb7'),
            preserve_default=True,
        ),
    ]
