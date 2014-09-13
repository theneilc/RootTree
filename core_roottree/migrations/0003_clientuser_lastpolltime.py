# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0002_auto_20140913_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientuser',
            name='lastpolltime',
            field=models.DateTimeField(default=datetime.datetime(1901, 1, 1, 0, 0)),
            preserve_default=True,
        ),
    ]
