# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-05 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0015_auto_20160901_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='text',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
