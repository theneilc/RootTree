# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0010_auto_20140913_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
