# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAndFlow', '0012_custominfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='custominfo',
            old_name='doctype',
            new_name='infotype',
        ),
    ]
