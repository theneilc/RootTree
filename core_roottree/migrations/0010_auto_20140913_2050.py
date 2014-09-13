# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0009_auto_20140913_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='command',
            name='expectfile',
        ),
        migrations.AddField(
            model_name='command',
            name='upload_file',
            field=models.URLField(default=False),
            preserve_default=True,
        ),
    ]
