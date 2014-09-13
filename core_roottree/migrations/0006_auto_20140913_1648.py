# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0005_auto_20140913_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientuser',
            name='uuid',
            field=models.CharField(unique=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='developer',
            name='uuid',
            field=models.CharField(unique=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='service',
            name='commandinstance',
            field=models.OneToOneField(related_name=b'command_service', to='core_roottree.CommandInstance'),
        ),
        migrations.AlterField(
            model_name='session',
            name='uuid',
            field=models.CharField(unique=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='task',
            name='commandinstance',
            field=models.OneToOneField(related_name=b'command_task', to='core_roottree.CommandInstance'),
        ),
    ]
