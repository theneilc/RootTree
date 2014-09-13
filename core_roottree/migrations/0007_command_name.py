# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0006_auto_20140913_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='name',
            field=models.CharField(default=b'Unnamed Command', max_length=50),
            preserve_default=True,
        ),
    ]
