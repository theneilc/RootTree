# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_roottree', '0007_command_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='result',
            new_name='file_url',
        ),
        migrations.AddField(
            model_name='commandinstance',
            name='stdin',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='developer',
            name='company',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='result_url',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=models.CharField(default=b'N', max_length=1, choices=[('N', 'Not Requested'), ('P', 'Pending'), ('C', 'Completed')]),
        ),
    ]
