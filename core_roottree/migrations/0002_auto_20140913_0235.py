# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='expectfile',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='command',
            name='language',
            field=models.CharField(default=b'b', max_length=1),
            preserve_default=True,
        ),
    ]
