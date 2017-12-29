# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0021_auto_20160705_1102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='elevation',
            options={'ordering': ['unitproject'], 'verbose_name': '\u6807\u9ad8', 'verbose_name_plural': '\u6807\u9ad8'},
        ),
        migrations.AlterField(
            model_name='directory',
            name='parent',
            field=models.ForeignKey(verbose_name=b'\xe7\x88\xb6\xe7\x9b\xae\xe5\xbd\x95', blank=True, to='TaskAndFlow.Directory', null=True),
            preserve_default=True,
        ),
    ]
