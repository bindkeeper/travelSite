# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-17 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0008_auto_20160917_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='arrival_lat',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='arrival_lng',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]
