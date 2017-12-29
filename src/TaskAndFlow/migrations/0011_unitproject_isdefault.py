# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0010_auto_20160522_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitproject',
            name='isdefault',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\xbb\x98\xe8\xae\xa4\xe5\x8a\xa0\xe8\xbd\xbd'),
            preserve_default=True,
        ),
    ]
