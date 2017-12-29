# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0009_auto_20160521_1245'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectModels',
        ),
        migrations.AddField(
            model_name='unitproject',
            name='modelfile',
            field=models.FileField(upload_to=b'', null=True, verbose_name=b'\xe6\xa8\xa1\xe5\x9e\x8b\xe6\x96\x87\xe4\xbb\xb6', blank=True),
            preserve_default=True,
        ),
    ]
