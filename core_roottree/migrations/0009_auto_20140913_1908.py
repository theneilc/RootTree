# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0008_auto_20140913_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='company',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
