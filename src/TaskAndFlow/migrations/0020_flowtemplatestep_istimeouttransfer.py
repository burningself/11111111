# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0019_auto_20160702_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowtemplatestep',
            name='istimeouttransfer',
            field=models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xb6\x85\xe6\x97\xb6\xe6\xb5\x81\xe8\xbd\xac'),
            preserve_default=True,
        ),
    ]
