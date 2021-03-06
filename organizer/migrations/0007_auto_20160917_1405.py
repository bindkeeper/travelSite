# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-17 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0006_auto_20160916_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='departure_lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='departure_lng',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
    ]
