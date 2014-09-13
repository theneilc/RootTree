# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0004_auto_20140913_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='uuid',
            field=models.CharField(max_length=32),
        ),
    ]
